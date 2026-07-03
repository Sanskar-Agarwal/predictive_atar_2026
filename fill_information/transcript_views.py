"""
Transcript upload endpoint.

Accepts a PDF upload, runs vision-based extraction (extract_data.llm_extract),
and returns the structured subjects/marks as JSON. This is the backend half of
the "upload a transcript to auto-fill the ATAR calculator" feature.

Kept in its own module so it doesn't disturb the existing views.py.
"""

import logging
import os
import tempfile

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from extract_data.llm_extract import extract_transcript

logger = logging.getLogger(__name__)

MAX_BYTES = 25 * 1024 * 1024  # 25 MB guard


@csrf_exempt
def upload_transcript(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Send a POST with the PDF in form field 'transcript'."},
            status=405,
        )

    upload = request.FILES.get("transcript")
    if upload is None:
        return JsonResponse(
            {"error": "No file found. Attach the PDF as form field 'transcript'."},
            status=400,
        )
    if not upload.name.lower().endswith(".pdf"):
        return JsonResponse({"error": "Only PDF files are supported."}, status=400)
    if upload.size > MAX_BYTES:
        return JsonResponse({"error": "File too large (max 25 MB)."}, status=400)

    # pdf2image needs a real path, so spool the upload to a temp file.
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            for chunk in upload.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        result, usage = extract_transcript(tmp_path)
        return JsonResponse(
            {
                "filename": upload.name,
                "region": result.region,
                "grade_format": result.grade_format,
                "subjects": [s.model_dump() for s in result.subjects],
                "notes": result.notes,
                "usage": usage,
            }
        )
    except Exception as exc:  # noqa: BLE001 - surface a clean error to the client
        logger.exception("Transcript extraction failed")
        return JsonResponse({"error": f"Extraction failed: {exc}"}, status=500)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# A minimal browser page for testing the upload locally (no React needed).
_TEST_PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Transcript Upload Test</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 16px}
 h1{font-size:20px} #drop{border:2px dashed #aaa;border-radius:10px;padding:28px;text-align:center;color:#555}
 button{padding:8px 16px;font-size:15px;margin-top:12px;cursor:pointer}
 table{border-collapse:collapse;width:100%;margin-top:18px}
 th,td{border:1px solid #ddd;padding:6px 10px;text-align:left;font-size:14px}
 th{background:#f4f4f4} .meta{color:#666;font-size:13px;margin-top:10px}
 #status{margin-top:14px;font-weight:600}
</style></head>
<body>
 <h1>\U0001F4CF Transcript Upload — local test</h1>
 <p>Select a transcript PDF and click Extract. This calls the local
    <code>/fill_information/upload_transcript/</code> endpoint.</p>
 <input type="file" id="file" accept="application/pdf">
 <div><button id="go">Extract</button></div>
 <div id="status"></div>
 <div id="out"></div>
<script>
const $=s=>document.querySelector(s);
$('#go').onclick=async()=>{
  const f=$('#file').files[0];
  if(!f){$('#status').textContent='Pick a PDF first.';return;}
  $('#status').textContent='Extracting … (this takes a few seconds)';$('#out').innerHTML='';
  const fd=new FormData();fd.append('transcript',f);
  const t0=performance.now();
  try{
    const r=await fetch('/fill_information/upload_transcript/',{method:'POST',body:fd});
    const d=await r.json();
    if(!r.ok){$('#status').textContent='Error: '+(d.error||r.status);return;}
    const secs=((performance.now()-t0)/1000).toFixed(1);
    let h=`<table><tr><th>Subject</th><th>Mark</th><th>Scale</th><th>Source label</th></tr>`;
    for(const s of d.subjects){h+=`<tr><td>${s.subject}</td><td>${s.mark}</td><td>${s.scale}</td><td>${s.source_label||''}</td></tr>`;}
    h+='</table>';
    h+=`<div class="meta">region: <b>${d.region}</b> &middot; format: <b>${d.grade_format}</b> &middot; `+
       `model: ${d.usage.model} &middot; ${d.usage.pages} pages &middot; `+
       `${d.usage.input_tokens} in / ${d.usage.output_tokens} out tokens &middot; ${secs}s</div>`;
    $('#out').innerHTML=h;$('#status').textContent=`Done — ${d.subjects.length} rows.`;
  }catch(e){$('#status').textContent='Request failed: '+e;}
};
</script>
</body></html>"""


def upload_test_page(request):
    """Serve a minimal HTML page for testing transcript upload in a browser."""
    return HttpResponse(_TEST_PAGE)

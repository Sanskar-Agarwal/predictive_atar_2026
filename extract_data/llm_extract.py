"""
Vision-based transcript extraction using the Claude API.

Renders each PDF page to an image, sends the pages to a Claude vision model,
and returns structured JSON (subjects + marks) validated against a schema.

This is a clean reimplementation of the older prototype scripts (gpt4v.py,
gemini.py) with three fixes:
  1. A current model (the old scripts used retired gpt-4-vision-preview).
  2. Enforced structured output (no fragile string-splitting).
  3. A typed schema that mirrors what the ATAR calculator ultimately needs.

Usage:
    from extract_data.llm_extract import extract_transcript
    result, usage = extract_transcript("path/to/transcript.pdf")
"""

import base64
import io
import os
from pathlib import Path
from typing import Literal

import anthropic
from dotenv import load_dotenv
from pdf2image import convert_from_path
from PIL import Image
from pydantic import BaseModel, Field

# Allow very large scanned pages without tripping Pillow's safety limit.
Image.MAX_IMAGE_PIXELS = None

# Load the API key from the project's .env (gitignored). Explicit path so it
# works regardless of the current working directory.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_DPI = 150  # high enough to read scanned tables; tune for cost vs. legibility


# --------------------------------------------------------------------------
# Output schema — what we ask the model to return, validated by pydantic.
# --------------------------------------------------------------------------
class SubjectMark(BaseModel):
    subject: str = Field(description="The subject/course name exactly as written on the transcript.")
    mark: str = Field(description="The mark or grade exactly as shown (e.g. '91', '47/50', 'B', '77').")
    scale: Literal[
        "numerical_percent",      # e.g. 91 (out of 100)
        "numerical_out_of_50",    # e.g. 47/50 (1-unit courses)
        "band_A_E",               # letter grade A–E
        "other",
    ] = Field(description="The numeric/grade scale of this mark.")
    source_label: str = Field(
        description="The document's own wording for THIS mark, e.g. 'Class Mark', "
        "'Trial HSC Examination Mark', 'Grade', 'Raw %'. Empty string if the page gives no label. "
        "This lets a later step choose which mark feeds the ATAR calculation."
    )


class TranscriptExtraction(BaseModel):
    region: str = Field(description="The state/region, e.g. 'NSW'. Use 'UNKNOWN' if not determinable.")
    grade_format: Literal["numerical", "non_numerical", "mixed", "unknown"] = Field(
        description="Whether marks are numbers, A-E bands, or a mix."
    )
    subjects: list[SubjectMark] = Field(
        description="One entry per FINAL subject mark/grade. Ignore noise pages "
        "(cover letters, award certificates, ID scans). May be empty if no usable marks exist."
    )
    notes: str = Field(
        description="Brief note on any extraction problem, e.g. 'document only shows ranks and "
        "per-task feedback, no final subject marks'. Use an empty string if extraction was clean."
    )


EXTRACTION_PROMPT = (
    "You are extracting FINAL subject results from an Australian senior secondary academic "
    "transcript for use in an ATAR calculator. Pages may be scanned or digital, and the document "
    "may include irrelevant pages (cover letters, prize certificates, ID scans) — ignore those.\n\n"
    "Extract ONLY the final/overall mark or grade for each subject — the single value that "
    "represents the student's outcome in that whole subject, on a recognised scale: a percentage, "
    "a mark out of 50 or 100, or an A-E band.\n\n"
    "DO NOT extract any of the following:\n"
    "  - Ranks or positions in a cohort (e.g. '2/17', '4th of 31', anything labelled 'Rank' or "
    "'Position'). A rank is NOT a mark.\n"
    "  - Marks or descriptors for individual assessment TASKS (e.g. a single 'Trial Examination' "
    "task weighted 30%, a 'Depth Study', a 'Speech') — these are components, not the final result.\n"
    "  - Vague qualitative words ('Excellent', 'High', 'Sound', 'Satisfactory') UNLESS that is "
    "genuinely the only formal grade the document assigns to the whole subject.\n\n"
    "If a subject legitimately shows MORE THAN ONE distinct FINAL mark of different kinds (e.g. an "
    "overall class/assessment mark AND an overall trial-exam mark for the entire course), record "
    "each as its own entry. Never record ranks or task components, and never invent marks.\n\n"
    "If a subject — or the whole document — has no usable final mark/grade, do not fabricate one: "
    "omit it and briefly explain the situation in 'notes'."
)


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def render_pdf_to_images(pdf_path: str, dpi: int = DEFAULT_DPI) -> list[str]:
    """Render every page of a PDF to a base64-encoded PNG string."""
    images = convert_from_path(pdf_path, dpi=dpi)
    encoded = []
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        encoded.append(base64.standard_b64encode(buf.getvalue()).decode("utf-8"))
    return encoded


# --------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------
def extract_transcript(
    pdf_path: str,
    model: str = DEFAULT_MODEL,
    dpi: int = DEFAULT_DPI,
    client: anthropic.Anthropic | None = None,
) -> tuple[TranscriptExtraction, dict]:
    """
    Extract structured subject/mark data from a transcript PDF.

    Returns (parsed_result, usage_dict). usage_dict has input/output token counts
    so callers can track cost.
    """
    if client is None:
        client = anthropic.Anthropic()

    page_images = render_pdf_to_images(pdf_path, dpi=dpi)

    content: list[dict] = [
        {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": b64},
        }
        for b64 in page_images
    ]
    content.append({"type": "text", "text": "Extract the subjects and final marks from this transcript."})

    response = client.messages.parse(
        model=model,
        max_tokens=2048,
        thinking={"type": "disabled"},
        system=[{"type": "text", "text": EXTRACTION_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": content}],
        output_format=TranscriptExtraction,
    )

    usage = {
        "model": response.model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "pages": len(page_images),
    }
    return response.parsed_output, usage


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m extract_data.llm_extract <path-to-transcript.pdf>")
        sys.exit(1)

    result, usage = extract_transcript(sys.argv[1])
    print(json.dumps(result.model_dump(), indent=2))
    print("\nusage:", usage)

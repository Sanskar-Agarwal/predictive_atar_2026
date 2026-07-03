"""
Run the vision extractor on a list of transcripts and print a verification-
friendly report, so a human can open each PDF and confirm the marks.

Saves all results to extraction_results.json for later scoring against the
human-confirmed ground truth.

Usage:
    python -m extract_data.verify_run            # runs the default sample set
    python -m extract_data.verify_run <pdf> ...  # runs specific files
"""

import json
import sys
from pathlib import Path

from extract_data.llm_extract import extract_transcript

_ROOT = Path(__file__).resolve().parent.parent

# Default verification set — spans the hard quadrants, weighted toward numerical
# (where a wrong mark does the most damage to a predicted ATAR).
DEFAULT_SET = [
    "extract_data/transcripts/NSW_NUMERICAL/Andrew Erin.pdf",
    "extract_data/transcripts/NSW_NUMERICAL/Agnew Andrei.pdf",
    "extract_data/transcripts/NSW_NUMERICAL/Bob Chen.pdf",
    "extract_data/transcripts/NSW_NUMERICAL/Mehta Aditya.pdf",
    "extract_data/transcripts/NSW_NON_NUMERICAL/Belzycki Nathan.pdf",
    "extract_data/transcripts/NSW_NON_NUMERICAL/Bergheim AIDEN_NSW.pdf",
]

IN_RATE, OUT_RATE = 3 / 1_000_000, 15 / 1_000_000  # Sonnet 4.6 live rates


def main(paths: list[str]) -> None:
    results = {}
    total_cost = 0.0

    for rel in paths:
        pdf = str(_ROOT / rel)
        name = Path(rel).name
        result, usage = extract_transcript(pdf)
        cost = usage["input_tokens"] * IN_RATE + usage["output_tokens"] * OUT_RATE
        total_cost += cost

        print(f"\n{'='*78}")
        print(f"  {name}")
        print(f"  OPEN TO VERIFY:  {pdf}")
        print(f"  region={result.region}  format={result.grade_format}  "
              f"({usage['pages']} pages, ${cost:.4f})")
        print(f"{'-'*78}")
        print(f"  {'SUBJECT':<34}{'MARK':<8}{'SOURCE LABEL'}")
        print(f"  {'-'*72}")
        for s in result.subjects:
            print(f"  {s.subject:<34}{s.mark:<8}{s.source_label}")

        results[name] = {
            "region": result.region,
            "grade_format": result.grade_format,
            "subjects": [s.model_dump() for s in result.subjects],
            "usage": usage,
        }

    out_path = _ROOT / "extract_data" / "extraction_results.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\n{'='*78}")
    print(f"  Saved results -> {out_path}")
    print(f"  Total: {len(paths)} transcripts, ${total_cost:.4f} "
          f"(avg ${total_cost/len(paths):.4f}/transcript)")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args if args else DEFAULT_SET)

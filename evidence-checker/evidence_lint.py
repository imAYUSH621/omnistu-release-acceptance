"""Local release-evidence CSV checks. No network requests or file mutation.
Prepared for Omnistu's educational release acceptance resources with AI assistance.
These checks assess record completeness, not whether evidence or a release is valid.
"""
import argparse
import csv
import io
import json
import sys
from pathlib import Path

FIELDS = ("case_id", "check", "expected", "actual", "status", "owner", "evidence", "reason")


def inspect_csv(text):
    """Return deterministic row/field/code diagnostics; never open evidence links."""
    issues = []
    def add(row, field, code):
        issues.append({"row": row, "field": field, "code": code})
    try:
        reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff"), newline=""), strict=True)
        header = reader.fieldnames
        if header is None:
            add(1, "header", "missing_header")
            return issues
        if len(header) != len(set(header)):
            add(1, "header", "duplicate_column")
            return issues
        missing = [f for f in FIELDS if f not in header]
        extra = [f for f in header if f not in FIELDS]
        for field in missing:
            add(1, field, "missing_column")
        for field in extra:
            add(1, field, "unknown_column")
        if missing or extra:
            return issues
        seen = set()
        count = 0
        for record in reader:
            count += 1
            row = reader.line_num
            # A row points to its final physical CSV line, including multiline fields.
            if None in record or any(v is None for v in record.values()):
                add(row, "row", "column_count")
                continue
            record = {k: v.strip() for k, v in record.items()}
            for field in ("case_id", "check", "expected", "status", "owner"):
                if not record[field]:
                    add(row, field, "required")
            case_id = record["case_id"]
            if case_id:
                if case_id in seen:
                    add(row, "case_id", "duplicate_id")
                seen.add(case_id)
            status = record["status"]
            if status not in ("pass", "fail", "not_run"):
                add(row, "status", "invalid_status")
                continue
            if status in ("pass", "fail"):
                for field in ("actual", "evidence"):
                    if not record[field]:
                        add(row, field, "required_for_observed_result")
            if status == "not_run":
                if not record["reason"]:
                    add(row, "reason", "required_for_not_run")
                if record["actual"] or record["evidence"]:
                    add(row, "status", "not_run_has_result")
            if status == "fail" and not record["reason"]:
                add(row, "reason", "required_for_fail")
        if count == 0:
            add(2, "row", "no_cases")
    except csv.Error:
        add(0, "csv", "malformed_csv")
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args(argv)
    try:
        text = args.csv_file.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        print(json.dumps({"ok": False, "error": type(error).__name__}))
        return 2
    issues = inspect_csv(text)
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

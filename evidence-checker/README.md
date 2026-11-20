# Check the record before calling a release checked

A release checklist can look complete while its rows have no observation or evidence. `evidence_lint.py` is a small, local-only Python checker for that clerical gap. It does not test the application, open links or decide whether a release is safe.

Prepared by Omnistu with AI assistance. All examples are synthetic. No customer project, independent audit or production restore is claimed.

## Run it

Requires Python 3.9 or later and only the standard library. Put the script beside a UTF-8 CSV file, then run:

```sh
python evidence_lint.py example-complete.csv
python evidence_lint.py example-incomplete.csv
python -m unittest -v test_evidence_lint.py
```

The complete example exits `0`. The incomplete example intentionally exits `1` with `required_for_observed_result` for an empty evidence field. File-read or encoding errors exit `2`.

Download the script, tests and examples from this repository's `evidence-checker` folder. The test suite has 19 synthetic regression tests, run locally on 20 November 2026. This is a test count for the checker, not a count of application checks.

## CSV contract

Use these exact column names, once each. Their order can change, but extra columns are rejected to catch misspelled headings.

```csv
case_id,check,expected,actual,status,owner,evidence,reason
```

| Field | Rule |
| --- | --- |
| `case_id` | Required and unique within the file, after trimming whitespace. Case-sensitive. |
| `check` | Required description of what was checked. |
| `expected` | Required expected behavior. |
| `status` | Exactly `pass`, `fail` or `not_run`. |
| `owner` | Required responsible role or name. Do not put personal details in a public example. |
| `actual` | Required for `pass` and `fail`; must be blank for `not_run`. |
| `evidence` | Required for `pass` and `fail`; must be blank for `not_run`. Can be a private evidence reference, not necessarily a public URL. |
| `reason` | Required for `fail` and `not_run`. Optional for `pass`. |

Quoted commas, quoted multiline fields and a UTF-8 BOM are supported through Python's `csv` reader. Blank lines are ignored; a header-only file is not accepted as a completed check record. Diagnostics use the final physical line of a record, so a multiline field can make the diagnostic row differ from its spreadsheet row.

## Interpret the output narrowly

A clean result means the file meets this record-shape contract. It does **not** mean:

- an evidence path exists, a URL opens or its contents support the result;
- screenshots are genuine, logs are complete or a named owner approved anything;
- the stated expected behavior is the right requirement;
- a `pass` is true, or a `not_run` case is safe to defer;
- deployment, backup recovery, security or accessibility has passed.

Keep real evidence private. The checker neither uploads the file nor reads paths named in its evidence cells. Before sharing a CSV, review it for secrets, personal data and customer information. This tool does not sanitize spreadsheet formulas or make a CSV safe to open in every spreadsheet application. It does not impose a size limit; use it only with files appropriate for your machine's memory.

Use a responsible maintainer's judgment for each unresolved check. A complete-looking row can still be wrong.

Background: [Omnistu's codebase handoff checklist](https://omnistu.com/blog/codebase-handoff-checklist/) and the repository's [restore rehearsal evidence worksheet](../restore-rehearsal-evidence.md).

No additional license has been selected. Public source visibility is not a grant of general reuse rights. Check the repository's terms before redistribution.

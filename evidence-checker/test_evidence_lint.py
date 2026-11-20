"""Synthetic regression cases for evidence_lint; run with python -m unittest -v."""
import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from evidence_lint import FIELDS, inspect_csv, main


def make_csv(rows, fields=FIELDS):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(fields)
    writer.writerows(rows)
    return output.getvalue()


GOOD = ["BOOT-01", "Fresh setup", "Starts from written instructions", "Started locally", "pass", "Maintainer", "evidence/setup.txt", ""]


class EvidenceTests(unittest.TestCase):
    def codes(self, rows):
        return {i["code"] for i in inspect_csv(make_csv(rows))}

    def test_complete_pass(self):
        self.assertEqual(inspect_csv(make_csv([GOOD])), [])

    def test_pass_needs_evidence(self):
        row = GOOD.copy(); row[6] = " "
        self.assertIn("required_for_observed_result", self.codes([row]))

    def test_failure_needs_reason(self):
        row = GOOD.copy(); row[4] = "fail"
        self.assertIn("required_for_fail", self.codes([row]))

    def test_failure_with_reason(self):
        row = GOOD.copy(); row[4] = "fail"; row[7] = "Runtime differs"
        self.assertEqual(self.codes([row]), set())

    def test_not_run_with_reason(self):
        row = GOOD.copy(); row[4] = "not_run"; row[3] = ""; row[6] = ""; row[7] = "No test device"
        self.assertEqual(self.codes([row]), set())

    def test_not_run_cannot_claim_result(self):
        row = GOOD.copy(); row[4] = "not_run"; row[7] = "No device"
        self.assertIn("not_run_has_result", self.codes([row]))

    def test_not_run_needs_reason(self):
        row = GOOD.copy(); row[4] = "not_run"; row[3] = ""; row[6] = ""
        self.assertIn("required_for_not_run", self.codes([row]))

    def test_duplicates(self):
        self.assertIn("duplicate_id", self.codes([GOOD, GOOD]))

    def test_missing_owner(self):
        row = GOOD.copy(); row[5] = ""
        self.assertIn("required", self.codes([row]))

    def test_status_is_explicit(self):
        row = GOOD.copy(); row[4] = "PASS"
        self.assertIn("invalid_status", self.codes([row]))

    def test_bom_and_multiline_quotes(self):
        row = GOOD.copy(); row[1] = 'Check "fresh", then\nrestart'
        self.assertEqual(inspect_csv("\ufeff" + make_csv([row])), [])

    def test_missing_column(self):
        self.assertIn("missing_column", {i["code"] for i in inspect_csv("case_id\nA\n")})

    def test_duplicate_header(self):
        self.assertEqual(inspect_csv("x,x\na,b\n")[0]["code"], "duplicate_column")

    def test_unknown_column(self):
        text = make_csv([GOOD + ["extra"]], FIELDS + ("unused",))
        self.assertEqual(inspect_csv(text)[0]["code"], "unknown_column")

    def test_ragged_rows(self):
        self.assertIn("column_count", self.codes([GOOD[:-1]]))
        self.assertIn("column_count", self.codes([GOOD + ["extra"]]))

    def test_empty_file(self):
        self.assertEqual(inspect_csv("")[0]["code"], "missing_header")

    def test_header_only(self):
        self.assertIn("no_cases", self.codes([]))

    def test_malformed_quote(self):
        self.assertEqual(inspect_csv(",".join(FIELDS) + '\n"unterminated')[0]["code"], "malformed_csv")

    def test_cli_statuses(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            path = Path(directory) / "checks.csv"
            path.write_text(make_csv([GOOD]), encoding="utf-8")
            self.assertEqual(main([str(path)]), 0)
            path.write_text("", encoding="utf-8")
            self.assertEqual(main([str(path)]), 1)
            self.assertEqual(main([str(path) + ".absent"]), 2)


if __name__ == "__main__":
    unittest.main()

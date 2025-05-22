import unittest
import json
import os
from migration.migration_server import (
    analyze_code_for_migration,
    generate_migrated_code,
    verify_migration_with_gold_standard,
    log_migration_summary,
)


class TestMigrationServer(unittest.TestCase):
    def setUp(self):
        # Create dummy files for testing
        self.test_dir = "test_migration_files"
        os.makedirs(self.test_dir, exist_ok=True)

        self.original_file_content = "This is a modus-button and a modus-alert."
        self.original_file_path = os.path.join(self.test_dir, "original.txt")
        with open(self.original_file_path, "w") as f:
            f.write(self.original_file_content)

        self.gold_standard_content = "This is a modus-wc-button and a modus-wc-alert."
        self.gold_standard_file_path = os.path.join(self.test_dir, "gold_standard.txt")
        with open(self.gold_standard_file_path, "w") as f:
            f.write(self.gold_standard_content)

        self.migrated_file_path = os.path.join(self.test_dir, "original_migrated.txt")

    def tearDown(self):
        # Clean up dummy files
        if os.path.exists(self.original_file_path):
            os.remove(self.original_file_path)
        if os.path.exists(self.gold_standard_file_path):
            os.remove(self.gold_standard_file_path)
        if os.path.exists(self.migrated_file_path):
            os.remove(self.migrated_file_path)
        if os.path.exists("migration_log.json"):
            os.remove("migration_log.json")
        if os.path.isdir(self.test_dir):
            os.rmdir(self.test_dir)

    def test_analyze_code_for_migration(self):
        with open(self.original_file_path, "r") as f:
            content = f.read()
        report_json = analyze_code_for_migration(content)
        report = json.loads(report_json)
        self.assertEqual(report["status"], "Analysis Complete")
        self.assertIn(
            "modus-button", [c["name"] for c in report["identified_v1_components"]]
        )
        # Test with empty content
        report_json_ne = analyze_code_for_migration("")
        report_ne = json.loads(report_json_ne)
        self.assertEqual(report_ne["status"], "Analysis Complete")

    def test_generate_migrated_code(self):
        with open(self.original_file_path, "r") as f:
            content = f.read()
        # First, analyze the code to get the analysis report as a JSON string
        analysis_report_json = analyze_code_for_migration(content)
        # Now, pass the analysis report JSON string to generate_migrated_code
        report_json = generate_migrated_code(
            content, analysis_report_json=analysis_report_json
        )
        report = json.loads(report_json)
        self.assertEqual(report["status"], "Code Generation Complete")
        self.assertIn("modus-wc-button", report["migrated_file_content"])
        self.assertNotIn("modus-button", report["migrated_file_content"])
        # Test with empty content
        analysis_report_json_ne = analyze_code_for_migration("")
        report_json_ne = generate_migrated_code(
            "", analysis_report_json=analysis_report_json_ne
        )
        report_ne = json.loads(report_json_ne)
        self.assertEqual(report_ne["status"], "Code Generation Complete")

    def test_verify_migration_with_gold_standard(self):
        v1_html = '<modus-button color="primary">Primary</modus-button>'
        v2_html = '<modus-wc-button variant="primary" aria-label="Primary">Primary</modus-wc-button>'
        with open(self.gold_standard_file_path, "r") as f:
            gold_content = f.read()
        # Run verification on the migrated file content
        report_json = verify_migration_with_gold_standard(v2_html, gold_content)
        report = json.loads(report_json)
        self.assertEqual(report["status"], "Verification Complete: Fully Compliant")
        self.assertEqual(report["compliance_status"], "Compliant")
        for check in report["checks"]:
            self.assertTrue(check["result"], f"Check failed: {check}")
        # Now test with a file that still has v1 tag (should be non-compliant)
        report_json_v1 = verify_migration_with_gold_standard(v1_html, gold_content)
        report_v1 = json.loads(report_json_v1)
        self.assertEqual(report_v1["compliance_status"], "Non-Compliant")
        v1_tag_check = next(
            (c for c in report_v1["checks"] if c["check"] == "No v1 tags present"), None
        )
        self.assertIsNotNone(v1_tag_check)
        self.assertFalse(v1_tag_check["result"])

    def test_log_migration_summary(self):
        # Create dummy report data
        analysis_data = {"file_path": "test.txt", "status": "Analyzed"}
        generation_data = {"migrated_file": "test_migrated.txt", "status": "Generated"}
        verification_data = {"compliance_status": "Compliant", "status": "Verified"}

        report_json = log_migration_summary(
            json.dumps(analysis_data),
            json.dumps(generation_data),
            json.dumps(verification_data),
            additional_info="Test successful",
        )
        report = json.loads(report_json)
        self.assertEqual(report["status"], "Logging Complete")
        self.assertTrue(os.path.exists(report["log_file"]))

        # Test with invalid JSON for one of the reports
        report_json_invalid = log_migration_summary(analysis_report_json="invalid json")
        report_invalid = json.loads(report_json_invalid)
        self.assertIn(
            "logging_error", json.loads(open(report_invalid["log_file"]).read())
        )


if __name__ == "__main__":
    unittest.main()

# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceMachineImport(YamlTransactionCase):
    def test_attendance_machine_import(self):
        self.run_yaml_scenario("test_data_attendance_machine_import.yaml")

    def test_ignore_error_line_without_reason_raises(self):
        machine = self.env["attendance_machine"].create(
            {"name": "Ignore Reason Test Machine", "code": "BL0127PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2024-01-28", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "error",
                "error_message": "Sample error for ignore reason test",
            }
        )
        with self.assertRaises(UserError):
            data_line.action_ignore()

    def test_edit_data_wizard_rejects_done_line(self):
        machine = self.env["attendance_machine"].create(
            {"name": "Edit Wizard Done Test Machine", "code": "BL0129PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-07-12", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "done",
                "data": '{"emp": "OLD"}',
            }
        )
        wizard = self.env["attendance_machine_import_data_edit"].create(
            {"data_id": data_line.id, "data": '{"emp": "NEW"}'}
        )
        with self.assertRaises(UserError):
            wizard.action_confirm()

    def test_edit_data_wizard_rejects_invalid_json(self):
        machine = self.env["attendance_machine"].create(
            {"name": "Edit Wizard Invalid JSON Test Machine", "code": "BL0129PY02"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-07-12", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "error",
                "error_message": "Sample error",
                "data": '{"emp": "OLD"}',
            }
        )
        wizard = self.env["attendance_machine_import_data_edit"].create(
            {"data_id": data_line.id, "data": "bukan json"}
        )
        with self.assertRaises(UserError):
            wizard.action_confirm()
        self.assertEqual(data_line.data, '{"emp": "OLD"}')

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

    def test_prepare_attendance_vals_hook(self):
        machine = self.env["attendance_machine"].create(
            {"name": "Prepare Vals Hook Test Machine", "code": "BL0175PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-02-10", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {"import_id": machine_import.id, "sequence": 1}
        )
        employee = self.env["hr.employee"].create(
            {"name": "Prepare Vals Hook Test Employee"}
        )
        working_schedule = self.env["resource.calendar"].search([], limit=1)
        timesheet = (
            self.env["hr.timesheet"]
            .with_user(self.env.ref("base.user_admin"))
            .create(
                {
                    "employee_id": employee.id,
                    "date_start": "2026-02-01",
                    "date_end": "2026-02-28",
                    "working_schedule_id": working_schedule.id,
                }
            )
        )

        # NOTE: this asserts the CORE contract only (base keys present, check_out
        # absent/present as expected). It does not assert exact key equality,
        # because when a glue module (e.g. Operating Unit) is also installed,
        # its override of this hook may legitimately add extra keys (e.g.
        # operating_unit_id) on top of the base contract.
        vals = data_line._prepare_attendance_vals(
            employee, timesheet, "2026-02-10", "2026-02-10 08:00:00"
        )
        self.assertTrue(
            {"employee_id", "date", "check_in", "sheet_id"}.issubset(vals.keys())
        )
        self.assertEqual(vals["employee_id"], employee.id)
        self.assertEqual(vals["sheet_id"], timesheet.id)
        self.assertNotIn("check_out", vals)

        vals_with_checkout = data_line._prepare_attendance_vals(
            employee,
            timesheet,
            "2026-02-10",
            "2026-02-10 08:00:00",
            check_out="2026-02-10 17:00:00",
        )
        self.assertTrue(
            {"employee_id", "date", "check_in", "sheet_id", "check_out"}.issubset(
                vals_with_checkout.keys()
            )
        )
        self.assertEqual(vals_with_checkout["check_out"], "2026-02-10 17:00:00")

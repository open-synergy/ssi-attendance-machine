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

    def test_failed_pending_job_does_not_block_import_done(self):
        machine = self.env["attendance_machine"].create(
            {"name": "BL-0185 Pending Job Test Machine", "code": "BL0185PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-07-14", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "done",
            }
        )
        batch = self.env["queue.job.batch"].get_new_batch("BL-0185 Test Batch")
        job = (
            data_line.with_context(job_batch=batch)
            .with_delay(description="BL-0185 pending job test")
            ._process_attendance()
        )
        # Simulate a job that failed and is orphaned from a stale run: force
        # it to "failed" without ever actually re-running _process_attendance.
        job.db_record().write({"state": "failed"})
        batch.write({"state": "progress"})
        machine_import.write(
            {"state": "queue_done", "done_queue_job_batch_id": batch.id}
        )

        machine_import._try_action_done()

        self.assertEqual(machine_import.state, "done")
        self.assertEqual(job.db_record().state, "done")

    def test_action_open_attendances_returns_scoped_action_window(self):
        """Python murni — pemicu P1 (L-01: action `call` YAML membuang nilai balik
        method, sehingga dict `ir.actions.act_window` tak bisa di-assert dari YAML).

        Memastikan `action_open_attendances` membuka `hr.timesheet_attendance`
        dengan domain terbatas pada `attendance_id` unik milik dokumen ini saja.
        """
        machine = self.env["attendance_machine"].create(
            {"name": "Open Attendances Action Test Machine", "code": "BL18PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-03-12", "machine_id": machine.id}
        )
        employee = self.env["hr.employee"].create(
            {"name": "Open Attendances Action Test Employee"}
        )
        working_schedule = self.env["resource.calendar"].search([], limit=1)
        timesheet = (
            self.env["hr.timesheet"]
            .with_user(self.env.ref("base.user_admin"))
            .create(
                {
                    "employee_id": employee.id,
                    "date_start": "2026-03-01",
                    "date_end": "2026-03-31",
                    "working_schedule_id": working_schedule.id,
                }
            )
        )
        timesheet.with_user(self.env.ref("base.user_admin")).action_open()

        attendance_1 = self.env["hr.timesheet_attendance"].create(
            {
                "employee_id": employee.id,
                "date": "2026-03-12",
                "check_in": "2026-03-12 08:00:00",
                "sheet_id": timesheet.id,
            }
        )
        attendance_2 = self.env["hr.timesheet_attendance"].create(
            {
                "employee_id": employee.id,
                "date": "2026-03-13",
                "check_in": "2026-03-13 08:00:00",
                "sheet_id": timesheet.id,
            }
        )

        # Another import's data line must never leak into this import's domain.
        other_import = self.env["attendance_machine_import"].create(
            {"date": "2026-03-14", "machine_id": machine.id}
        )
        other_attendance = self.env["hr.timesheet_attendance"].create(
            {
                "employee_id": employee.id,
                "date": "2026-03-14",
                "check_in": "2026-03-14 08:00:00",
                "sheet_id": timesheet.id,
            }
        )
        self.env["attendance_machine_import.data"].create(
            {
                "import_id": other_import.id,
                "sequence": 1,
                "state": "done",
                "attendance_id": other_attendance.id,
            }
        )

        self.env["attendance_machine_import.data"].create(
            [
                {
                    "import_id": machine_import.id,
                    "sequence": 1,
                    "state": "done",
                    "attendance_id": attendance_1.id,
                },
                {
                    "import_id": machine_import.id,
                    "sequence": 2,
                    "state": "done",
                    "attendance_id": attendance_2.id,
                },
            ]
        )

        action = machine_import.action_open_attendances()

        self.assertEqual(action["res_model"], "hr.timesheet_attendance")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["view_mode"], "tree,form")
        domain_field, operator, domain_ids = action["domain"][0]
        self.assertEqual(domain_field, "id")
        self.assertEqual(operator, "in")
        self.assertEqual(set(domain_ids), {attendance_1.id, attendance_2.id})
        self.assertNotIn(other_attendance.id, domain_ids)

    def test_sign_value_tokens_keep_blank_tokens(self):
        """Python murni — pemicu P1 (L-01: `action: call` YAML membuang nilai
        balik method, sehingga list token tak bisa di-assert dari YAML).

        `_get_sign_value_tokens` mempertahankan token kosong (blank Row Type
        Column value bisa jadi label check-in/out yang sah), dan nilai tunggal
        tanpa koma menghasilkan satu token identik dengan perilaku lama.
        """
        mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Sign Token Test Mapping",
                "code": "BL20PY01",
                "row_mode": "separate",
                "sign_in_value": ",Lembur Masuk",
                "sign_out_value": "C/Keluar,Lembur Keluar",
            }
        )
        self.assertEqual(mapping._get_sign_value_tokens("in"), ["", "Lembur Masuk"])
        self.assertEqual(
            mapping._get_sign_value_tokens("out"), ["C/Keluar", "Lembur Keluar"]
        )

        single_value_mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Sign Token Single Value Test Mapping",
                "code": "BL20PY02",
                "row_mode": "separate",
                "sign_in_value": "IN",
                "sign_out_value": "OUT",
            }
        )
        self.assertEqual(single_value_mapping._get_sign_value_tokens("in"), ["IN"])
        self.assertEqual(single_value_mapping._get_sign_value_tokens("out"), ["OUT"])

        blank_mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Sign Token Blank Test Mapping",
                "code": "BL20PY03",
                "row_mode": "separate",
            }
        )
        self.assertEqual(blank_mapping._get_sign_value_tokens("in"), [""])
        self.assertEqual(blank_mapping._get_sign_value_tokens("out"), [""])

    def test_exclude_value_tokens_discard_blank_tokens_and_disable_when_empty(self):
        """Python murni — pemicu P1 (L-01: `action: call` YAML membuang nilai
        balik method, sehingga list token tak bisa di-assert dari YAML).

        `_get_exclude_value_tokens` membuang token kosong dan mengembalikan
        list kosong (fitur nonaktif) bila `exclude_column` atau
        `exclude_values` belum diisi.
        """
        mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Exclude Token Test Mapping",
                "code": "BL20PY04",
                "exclude_column": "exception",
                "exclude_values": "Invalid,Mengulang,",
            }
        )
        self.assertEqual(mapping._get_exclude_value_tokens(), ["Invalid", "Mengulang"])

        no_values_mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Exclude Token No Values Test Mapping",
                "code": "BL20PY05",
                "exclude_column": "exception",
            }
        )
        self.assertEqual(no_values_mapping._get_exclude_value_tokens(), [])

        no_column_mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Exclude Token No Column Test Mapping",
                "code": "BL20PY06",
                "exclude_values": "Invalid,Mengulang",
            }
        )
        self.assertEqual(no_column_mapping._get_exclude_value_tokens(), [])

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

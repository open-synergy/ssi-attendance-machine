# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import io
import json

import xlwt
from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceMachineImport(YamlTransactionCase):
    """Cover the ``attendance_machine_import`` document and its lines."""

    def test_attendance_machine_import(self):
        """Run the ``attendance_machine_import`` YAML scenario."""
        self.run_yaml_scenario("test_data_attendance_machine_import.yaml")

    def test_failed_pending_job_does_not_block_import_done(self):
        """A stale ``failed`` job does not block ``_try_action_done``, and
        is left ``failed`` instead of being forced ``done``.

        Pure Python -- trigger P10 (L-09, L-10, L-11: the fixture
        builds a ``queue.job.batch``, calls ``with_delay()`` on the
        underscore-prefixed ``_process_attendance``, and writes
        ``state`` through ``job.db_record()`` -- impossible to
        express in a single ``EVAL:`` expression).

        ``_force_pending_queue_job_done`` only forces jobs in a
        non-terminal state (``pending``/``enqueued``/``started``) to
        ``done``; a ``failed`` job's trail is preserved instead. The
        import still reaches ``done`` because its only data line
        already settled (``state='done'``) -- completion is decided
        from the data lines, not from the queue jobs.
        """
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
        self.assertEqual(job.db_record().state, "failed")

    def test_ignore_error_line_with_failed_job_marks_job_done(self):
        """``_ignore`` forces a ``failed`` linked job to ``done`` instead
        of leaving its failure trail blocking the batch.

        Pure Python -- trigger P10 (L-09, L-10, L-11: the fixture calls
        ``with_delay()`` on the underscore-prefixed
        ``_process_attendance`` and writes ``state`` through
        ``job.db_record()``) and P1 (L-01: ``with_delay()`` returns a
        ``Delayable``, and ``action: call`` discards return values with
        no ``save_as`` on ``call`` to capture one).

        A data line in ``error`` state whose linked job already failed
        is ignored successfully (``ignore_reason`` filled beforehand),
        and the failed job -- not ``done`` and not ``cancelled`` -- is
        forced to ``done`` so it stops blocking the import's batch.
        """
        machine = self.env["attendance_machine"].create(
            {"name": "Ignore Failed Job Test Machine", "code": "BL51PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-08-10", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "error",
                "error_message": "Employee code was not yet registered",
            }
        )
        job = data_line.with_delay(
            description="BL-51 ignore failed job test"
        )._process_attendance()
        job.db_record().write({"state": "failed"})
        data_line.write(
            {
                "queue_job_id": job.db_record().id,
                "ignore_reason": "Employee resigned, safe to ignore",
            }
        )

        data_line.action_ignore()

        self.assertEqual(data_line.state, "ignored")
        self.assertEqual(job.db_record().state, "done")

    def test_retry_with_existing_job_requeues_it_instead_of_creating_new(self):
        """``_retry`` requeues an already-linked job instead of enqueuing
        a second one for the same line.

        Pure Python -- trigger P10 (L-09, L-10, L-11: the fixture calls
        ``with_delay()`` on the underscore-prefixed
        ``_process_attendance`` and writes ``state`` through
        ``job.db_record()``) and P1 (L-01: ``with_delay()`` returns a
        ``Delayable``, and ``action: call`` discards return values with
        no ``save_as`` on ``call`` to capture one).

        A data line in ``error`` state whose ``queue_job_id`` already
        points at a (stale, ``failed``) job keeps that same job on
        retry -- it is requeued to ``pending``, not replaced by a new
        one.
        """
        machine = self.env["attendance_machine"].create(
            {"name": "Retry Existing Job Test Machine", "code": "BL51PY02"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-08-10", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "error",
                "error_message": "Employee code was not yet registered",
            }
        )
        job = data_line.with_delay(
            description="BL-51 retry existing job test"
        )._process_attendance()
        job.db_record().write({"state": "failed"})
        data_line.queue_job_id = job.db_record().id

        data_line.action_retry()

        self.assertEqual(data_line.state, "draft")
        self.assertFalse(data_line.error_message)
        self.assertEqual(data_line.queue_job_id.id, job.db_record().id)
        self.assertEqual(job.db_record().state, "pending")

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
                "employee_column": "employee_id",
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
                "employee_column": "employee_id",
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
                "employee_column": "employee_id",
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
                "employee_column": "employee_id",
                "exclude_column": "exception",
                "exclude_values": "Invalid,Mengulang,",
            }
        )
        self.assertEqual(mapping._get_exclude_value_tokens(), ["Invalid", "Mengulang"])

        no_values_mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Exclude Token No Values Test Mapping",
                "code": "BL20PY05",
                "employee_column": "employee_id",
                "exclude_column": "exception",
            }
        )
        self.assertEqual(no_values_mapping._get_exclude_value_tokens(), [])

        no_column_mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Exclude Token No Column Test Mapping",
                "code": "BL20PY06",
                "employee_column": "employee_id",
                "exclude_values": "Invalid,Mengulang",
            }
        )
        self.assertEqual(no_column_mapping._get_exclude_value_tokens(), [])

    def test_prepare_attendance_vals_hook(self):
        """``_prepare_attendance_vals`` returns the base contract keys.

        Pure Python -- trigger P1 (L-01, L-02: the return value of
        ``_prepare_attendance_vals`` is what is asserted, but
        ``action: call`` discards return values and every YAML
        assert's actual side is a dotted ``getattr`` on a registry
        record).
        """
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

    def test_excel_import_reads_xls_file(self):
        """Read an Excel attendance file through ``action_load_data``.

        Pure Python -- trigger P10 (L-09, L-10, L-11: the fixture
        builds a real binary ``.xls`` file with ``xlwt`` and
        base64-encodes it, which the YAML ``EVAL:`` whitelist cannot
        express -- no loops, no ``import``, so ``base64``/``xlwt`` are
        out of reach).

        Builds an in-memory ``.xls`` file (header + 3 rows, including
        one blank cell and one whole-number cell), then verifies
        ``action_load_data`` reads it through the Excel path: the
        number of ``data_ids`` matches the row count, the blank cell
        reads back as ``""``, and the whole-number cell reads back as
        ``"1499"`` (not ``"1499.0"``).
        """
        book = xlwt.Workbook()
        sheet = book.add_sheet("Sheet1")
        for col, header in enumerate(["employee_id", "code", "remark"]):
            sheet.write(0, col, header)
        sheet.write(1, 0, "EMP001")
        sheet.write(1, 1, 1499)
        sheet.write(1, 2, "first note")
        sheet.write(2, 0, "EMP002")
        # Column 1 intentionally left unwritten -> blank cell in xlrd.
        sheet.write(2, 2, "second note")
        sheet.write(3, 0, "EMP003")
        sheet.write(3, 1, 7)
        # Column 2 intentionally left unwritten -> blank cell in xlrd.

        buffer = io.BytesIO()
        book.save(buffer)
        xls_bytes = buffer.getvalue()

        mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Excel Import Test CSV Mapping",
                "code": "BL25PX01",
                "employee_column": "employee_id",
                "file_format": "excel",
            }
        )
        machine = self.env["attendance_machine"].create(
            {
                "name": "Excel Import Test Machine",
                "code": "BL25PX01A",
                "csv_mapping_id": mapping.id,
            }
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-07-23", "machine_id": machine.id}
        )
        machine_import.attendance_file = base64.b64encode(xls_bytes)

        machine_import.action_load_data()

        self.assertEqual(len(machine_import.data_ids), 3)
        rows = [
            json.loads(line.data) for line in machine_import.data_ids.sorted("sequence")
        ]
        self.assertEqual(rows[0]["employee_id"], "EMP001")
        self.assertEqual(rows[0]["code"], "1499")
        self.assertEqual(rows[1]["code"], "")
        self.assertEqual(rows[2]["remark"], "")

    def test_excel_import_corrupt_file_raises_user_error(self):
        """A corrupt Excel file raises a structured ``UserError``.

        Pure Python -- trigger P10 (L-09, L-10, L-11: the fixture
        needs arbitrary binary bytes that are not a valid
        ``.xls``/``.xlsx``, which the YAML ``EVAL:`` whitelist cannot
        express without real Python).

        A corrupt/non-Excel file with ``file_format="excel"`` raises a
        structured ``UserError``, not a raw ``xlrd`` traceback.
        """
        mapping = self.env["attendance_machine_csv_mapping"].create(
            {
                "name": "Excel Import Corrupt Test CSV Mapping",
                "code": "BL25PX02",
                "employee_column": "employee_id",
                "file_format": "excel",
            }
        )
        machine = self.env["attendance_machine"].create(
            {
                "name": "Excel Import Corrupt Test Machine",
                "code": "BL25PX02A",
                "csv_mapping_id": mapping.id,
            }
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-07-23", "machine_id": machine.id}
        )
        machine_import.attendance_file = base64.b64encode(
            b"not a real xls file \x00\x01\x02\x03"
        )

        with self.assertRaises(UserError):
            machine_import.action_load_data()

    def test_action_open_ignore_wizard_returns_scoped_action_window(self):
        """``action_open_ignore_wizard`` returns a scoped act_window dict.

        Pure Python -- trigger P1 (L-01, L-02: ``action: call`` YAML
        discards the method's return value, and every YAML assert
        target is a dotted ``getattr`` on a registry record, so the
        ``ir.actions.act_window`` dict itself cannot be inspected from
        YAML).

        Builds a data line directly in ``error`` state, without
        running ``action_load_data``, then asserts the wizard action
        points at the ignore-reason wizard model, opens as a dialog,
        and is pre-scoped to this data line via
        ``context["default_data_id"]``.
        """
        machine = self.env["attendance_machine"].create(
            {"name": "Open Ignore Wizard Test Machine", "code": "BL27PY01"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-08-06", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "error",
                "error_message": "Sample error for ignore wizard action test",
            }
        )

        action = data_line.action_open_ignore_wizard()

        self.assertEqual(action["res_model"], "attendance_machine_import_data_ignore")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_data_id"], data_line.id)

    def test_action_open_edit_data_wizard_returns_scoped_action_window(self):
        """``action_open_edit_data_wizard`` returns a scoped act_window.

        Pure Python -- trigger P1 (L-01, L-02: ``action: call`` YAML
        discards the method's return value, and every YAML assert
        target is a dotted ``getattr`` on a registry record, so the
        ``ir.actions.act_window`` dict itself cannot be inspected from
        YAML).

        Builds a data line directly in ``error`` state, without
        running ``action_load_data``, then asserts the wizard action
        points at the edit-data wizard model, opens as a dialog, and
        is pre-scoped to this data line via
        ``context["default_data_id"]``.
        """
        machine = self.env["attendance_machine"].create(
            {"name": "Open Edit Data Wizard Test Machine", "code": "BL27PY02"}
        )
        machine_import = self.env["attendance_machine_import"].create(
            {"date": "2026-08-07", "machine_id": machine.id}
        )
        data_line = self.env["attendance_machine_import.data"].create(
            {
                "import_id": machine_import.id,
                "sequence": 1,
                "state": "error",
                "error_message": ("Sample error for edit data wizard action test"),
                "data": '{"emp": "OLD"}',
            }
        )

        action = data_line.action_open_edit_data_wizard()

        self.assertEqual(action["res_model"], "attendance_machine_import_data_edit")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_data_id"], data_line.id)

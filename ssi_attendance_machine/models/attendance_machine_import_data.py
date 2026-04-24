# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from datetime import datetime

import pytz

from odoo import _, fields, models
from odoo.exceptions import UserError


class AttendanceMachineImportData(models.Model):
    """
    One line per row in the attendance file. Stores the raw JSON row data
    and tracks the resulting hr.timesheet_attendance record created from it.
    """

    _name = "attendance_machine_import.data"
    _description = "Attendance Machine Import - Data"
    _order = "import_id, sequence"

    import_id = fields.Many2one(
        string="# Import",
        comodel_name="attendance_machine_import",
        required=True,
        ondelete="cascade",
        help="The import document this line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Row sequence from the source file.",
    )
    data = fields.Text(
        string="Data",
        help="Raw row data from the attendance file, stored as a JSON object.",
    )
    attendance_id = fields.Many2one(
        string="Attendance",
        comodel_name="hr.timesheet_attendance",
        ondelete="set null",
        help="The timesheet attendance record created from this data line.",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        related="attendance_id.sheet_id.employee_id",
        store=True,
        help="Employee derived from the linked attendance record's timesheet.",
    )

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _get_row_data(self):
        self.ensure_one()
        if not self.data:
            return {}
        try:
            return json.loads(self.data)
        except (ValueError, TypeError):
            return {}

    def _get_mapping(self):
        self.ensure_one()
        return self.import_id.machine_id.csv_mapping_id

    def _find_employee(self, employee_code):
        """Return the hr.employee record matching the given machine employee code."""
        self.ensure_one()
        machine = self.import_id.machine_id
        emp_line = machine.employee_ids.filtered(
            lambda e: (e.employee_code or "").strip() == (employee_code or "").strip()
        )
        if emp_line:
            return emp_line[0].employee_id
        return self.env["hr.employee"]

    def _find_sheet(self, employee, date):
        """Return the open hr.timesheet covering employee on date, or empty recordset."""
        return self.env["hr.timesheet"].search(
            [
                ("employee_id", "=", employee.id),
                ("date_start", "<=", date),
                ("date_end", ">=", date),
                ("state", "=", "open"),
            ],
            limit=1,
        )

    def _parse_datetime(self, value, fmt):
        """Parse a datetime string using the given strptime format string."""
        if not value or not fmt:
            return False
        try:
            return datetime.strptime(value.strip(), fmt.strip())
        except (ValueError, TypeError):
            return False

    def _to_utc(self, naive_dt):
        """Convert a naive datetime (assumed to be in the user's timezone) to UTC."""
        if not naive_dt:
            return False
        tz_name = self.env.user.tz or "UTC"
        try:
            local_tz = pytz.timezone(tz_name)
            local_dt = local_tz.localize(naive_dt, is_dst=None)
            return local_dt.astimezone(pytz.utc).replace(tzinfo=None)
        except Exception:
            return naive_dt

    def _extract_datetime_single(self, row, mapping, direction):
        """
        Extract a datetime value from a single-row mode row.
        direction: 'in' for check-in, 'out' for check-out.
        """
        if mapping.datetime_mode == "combined":
            col = (
                mapping.check_in_column
                if direction == "in"
                else mapping.check_out_column
            )
            if not col:
                return False
            value = row.get(col, "")
            return self._parse_datetime(value, mapping.datetime_format)
        else:
            if direction == "in":
                date_col = mapping.check_in_date_column
                time_col = mapping.check_in_time_column
            else:
                date_col = mapping.check_out_date_column
                time_col = mapping.check_out_time_column
            if not date_col:
                return False
            date_val = row.get(date_col, "")
            time_val = row.get(time_col or "", "")
            combined = (date_val or "").strip() + " " + (time_val or "").strip()
            fmt = (
                (mapping.date_format or "%Y-%m-%d")
                + " "
                + (mapping.time_format or "%H:%M:%S")
            )
            return self._parse_datetime(combined, fmt)

    def _extract_datetime_separate(self, row, mapping):
        """
        Extract a datetime value from a separate-rows mode row.
        """
        if mapping.datetime_mode == "combined":
            col = mapping.datetime_column
            if not col:
                return False
            value = row.get(col, "")
            return self._parse_datetime(value, mapping.datetime_format)
        else:
            date_col = mapping.date_column
            time_col = mapping.time_column
            if not date_col:
                return False
            date_val = row.get(date_col, "")
            time_val = row.get(time_col or "", "")
            combined = (date_val or "").strip() + " " + (time_val or "").strip()
            fmt = (
                (mapping.date_format or "%Y-%m-%d")
                + " "
                + (mapping.time_format or "%H:%M:%S")
            )
            return self._parse_datetime(combined, fmt)

    # -------------------------------------------------------------------------
    # Queue job methods
    # -------------------------------------------------------------------------

    def _process_attendance(self):
        """
        Parse the raw JSON data line and create or update an
        hr.timesheet_attendance record according to the machine's CSV mapping.
        Idempotent: if attendance_id is already set, skip to prevent duplicates on retry.
        """
        self.ensure_one()
        if self.attendance_id:
            return
        mapping = self._get_mapping()
        if not mapping:
            return

        row = self._get_row_data()
        if not row:
            return

        employee_code = str(row.get(mapping.employee_column or "", "")).strip()
        employee = self._find_employee(employee_code)
        if not employee:
            raise UserError(
                _(
                    """
Context: Processing attendance import data line
Document: %s (sequence %s)
Problem: Employee code '%s' is not registered in the machine's employee list
Solution: Register the employee code in the attendance machine configuration,
          correct the data in this line, then retry the queue job"""
                )
                % (self.import_id.name or str(self.import_id.id), self.sequence, employee_code)
            )

        Attendance = self.env["hr.timesheet_attendance"]

        if mapping.row_mode == "single":
            check_in_naive = self._extract_datetime_single(row, mapping, "in")
            check_out_naive = self._extract_datetime_single(row, mapping, "out")
            if not check_in_naive:
                raise UserError(
                    _(
                        """
Context: Processing attendance import data line
Document: %s (sequence %s)
Problem: Could not parse check-in datetime from the data
Solution: Verify the datetime format in the CSV mapping matches the actual data,
          correct the data in this line, then retry the queue job"""
                    )
                    % (self.import_id.name or str(self.import_id.id), self.sequence)
                )

            check_in_utc = self._to_utc(check_in_naive)
            check_out_utc = self._to_utc(check_out_naive) if check_out_naive else False
            att_date = check_in_naive.date()

            sheet = self._find_sheet(employee, att_date)
            if not sheet:
                raise UserError(
                    _(
                        """
Context: Processing attendance import data line
Document: %s (sequence %s)
Problem: No open timesheet found for employee '%s' on date %s
Solution: Create or open a timesheet for this employee covering the date,
          then retry the queue job"""
                    )
                    % (
                        self.import_id.name or str(self.import_id.id),
                        self.sequence,
                        employee.name,
                        att_date,
                    )
                )

            # Look for an existing record with the same employee, date, check_in
            existing = Attendance.search(
                [
                    ("employee_id", "=", employee.id),
                    ("date", "=", att_date),
                    ("check_in", "=", check_in_utc),
                ],
                limit=1,
            )
            if existing:
                if check_out_utc and not existing.check_out:
                    existing.check_out = check_out_utc
                self.attendance_id = existing.id
            else:
                vals = {
                    "employee_id": employee.id,
                    "date": att_date,
                    "check_in": check_in_utc,
                    "sheet_id": sheet.id,
                }
                if check_out_utc:
                    vals["check_out"] = check_out_utc
                att = Attendance.create(vals)
                self.attendance_id = att.id

        elif mapping.row_mode == "separate":
            row_type = str(row.get(mapping.row_type_column or "", "")).strip()
            dt_naive = self._extract_datetime_separate(row, mapping)
            if not dt_naive:
                raise UserError(
                    _(
                        """
Context: Processing attendance import data line
Document: %s (sequence %s)
Problem: Could not parse datetime from the data
Solution: Verify the datetime format in the CSV mapping matches the actual data,
          correct the data in this line, then retry the queue job"""
                    )
                    % (self.import_id.name or str(self.import_id.id), self.sequence)
                )

            dt_utc = self._to_utc(dt_naive)
            att_date = dt_naive.date()

            if row_type == (mapping.sign_in_value or "").strip():
                sheet = self._find_sheet(employee, att_date)
                if not sheet:
                    raise UserError(
                        _(
                            """
Context: Processing attendance import data line
Document: %s (sequence %s)
Problem: No open timesheet found for employee '%s' on date %s
Solution: Create or open a timesheet for this employee covering the date,
          then retry the queue job"""
                        )
                        % (
                            self.import_id.name or str(self.import_id.id),
                            self.sequence,
                            employee.name,
                            att_date,
                        )
                    )

                # Check-in row: create a new attendance record
                existing = Attendance.search(
                    [
                        ("employee_id", "=", employee.id),
                        ("date", "=", att_date),
                        ("check_in", "=", dt_utc),
                    ],
                    limit=1,
                )
                if existing:
                    self.attendance_id = existing.id
                else:
                    att = Attendance.create(
                        {
                            "employee_id": employee.id,
                            "date": att_date,
                            "check_in": dt_utc,
                            "sheet_id": sheet.id,
                        }
                    )
                    self.attendance_id = att.id

            elif row_type == (mapping.sign_out_value or "").strip():
                # Check-out row: find the most recent open attendance for this
                # employee on this date and set check_out
                existing = Attendance.search(
                    [
                        ("employee_id", "=", employee.id),
                        ("date", "=", att_date),
                        ("check_out", "=", False),
                    ],
                    order="check_in desc",
                    limit=1,
                )
                if existing:
                    existing.check_out = dt_utc
                    self.attendance_id = existing.id

    def _cancel_attendance(self):
        """
        Remove the linked hr.timesheet_attendance record and clear the link.
        """
        self.ensure_one()
        if self.attendance_id:
            att = self.attendance_id
            self.attendance_id = False
            att.unlink()

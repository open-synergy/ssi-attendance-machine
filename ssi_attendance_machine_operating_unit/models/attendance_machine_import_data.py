# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceMachineImportData(models.Model):
    """Propagate Operating Unit from the timesheet to created attendances.

    Overrides ``_prepare_attendance_vals`` so attendances created by
    the import inherit the operating unit of their parent
    ``hr.timesheet``, matching the convention used by the UI path
    (the onchange on ``hr.timesheet_attendance`` derives it from
    ``sheet_id``). The employee's operating unit is deliberately not
    used: it can differ from the timesheet's, and using it would
    reintroduce the divergence this glue module fixes.
    """

    _name = "attendance_machine_import.data"
    _inherit = "attendance_machine_import.data"

    def _prepare_attendance_vals(
        self, employee, sheet, att_date, check_in, check_out=False
    ):
        """Attendance created by the import inherits the timesheet's operating unit.

        The core module creates the attendance programmatically, so
        the onchange on ``hr.timesheet_attendance`` never fires and
        the operating unit would otherwise fall back to the default
        one (the operating unit of the user processing the import).
        The timesheet is the sole source of truth for the operating
        unit here -- assigned unconditionally, with no fallback to
        the employee's operating unit or to the mixin's user-based
        default, so a timesheet without an operating unit yields an
        attendance without one too.

        :param employee: hr.employee the attendance belongs to
        :param sheet: hr.timesheet the attendance is linked to;
            guaranteed non-empty by the callers in the core module
        :param att_date: attendance date
        :param check_in: check-in datetime
        :param check_out: check-out datetime, or False when the row
            only carries a sign-in
        :return: vals dict for creating the hr.timesheet_attendance
        """
        _super = super(AttendanceMachineImportData, self)
        vals = _super._prepare_attendance_vals(
            employee, sheet, att_date, check_in, check_out=check_out
        )
        vals["operating_unit_id"] = sheet.operating_unit_id.id
        return vals

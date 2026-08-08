# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceMachineImportData(models.Model):
    """Propagate Operating Unit from employee to created attendances.

    Overrides ``_prepare_attendance_vals`` so attendances created by
    the import inherit the employee's operating unit.
    """

    _name = "attendance_machine_import.data"
    _inherit = "attendance_machine_import.data"

    def _prepare_attendance_vals(
        self, employee, sheet, att_date, check_in, check_out=False
    ):
        """Attendance created by the import inherits the employee's operating unit.

        The core module creates the attendance programmatically, so the
        onchange on hr.timesheet_attendance never fires and the operating
        unit would otherwise fall back to the default one.
        """
        _super = super(AttendanceMachineImportData, self)
        vals = _super._prepare_attendance_vals(
            employee, sheet, att_date, check_in, check_out=check_out
        )
        if employee.operating_unit_id:
            vals["operating_unit_id"] = employee.operating_unit_id.id
        return vals

# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttendanceMachineEmployee(models.Model):
    """
    Maps an employee to an attendance machine along with their machine-specific
    employee code used in the attendance file.
    """

    _name = "attendance_machine.employee"
    _description = "Attendance Machine - Employee"
    _order = "machine_id, sequence"

    machine_id = fields.Many2one(
        string="# Machine",
        comodel_name="attendance_machine",
        required=True,
        ondelete="cascade",
        help="The attendance machine this employee is registered on.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Display sequence.",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        ondelete="restrict",
        help="The employee record in Odoo.",
    )
    employee_code = fields.Char(
        string="Employee Code",
        help=(
            "The employee identifier as recorded in the attendance machine file. "
            "This code is used to match file rows to the employee record."
        ),
    )

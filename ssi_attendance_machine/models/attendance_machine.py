# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttendanceMachine(models.Model):
    """
    Represents a physical attendance machine device.
    Contains the machine's model reference, CSV mapping configuration,
    and the list of employees registered on the machine.
    """

    _name = "attendance_machine"
    _description = "Attendance Machine"
    _inherit = ["mixin.master_data"]

    attendance_model_id = fields.Many2one(
        string="Machine Model",
        comodel_name="attendance_machine_model",
        ondelete="restrict",
        help="The brand/model of this attendance machine device.",
    )
    csv_mapping_id = fields.Many2one(
        string="CSV Mapping",
        comodel_name="attendance_machine_csv_mapping",
        ondelete="restrict",
        help=(
            "The CSV mapping template that defines how attendance data files "
            "from this machine should be parsed."
        ),
    )
    employee_ids = fields.One2many(
        string="Employees",
        comodel_name="attendance_machine.employee",
        inverse_name="machine_id",
        help="List of employees registered on this machine with their machine codes.",
    )

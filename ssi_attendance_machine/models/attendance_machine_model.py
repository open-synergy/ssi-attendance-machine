# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttendanceMachineModel(models.Model):
    """
    Represents a brand/model of an attendance machine device.
    Used as reference data for attendance machines.
    """

    _name = "attendance_machine_model"
    _description = "Attendance Machine Model"
    _inherit = ["mixin.master_data"]

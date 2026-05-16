# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceMachineImport(models.Model):  # pylint: disable=too-few-public-methods
    _name = "attendance_machine_import"
    _inherit = [
        "attendance_machine_import",
        "mixin.single_operating_unit",
    ]

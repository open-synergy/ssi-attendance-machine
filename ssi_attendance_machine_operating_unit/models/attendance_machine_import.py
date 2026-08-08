# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceMachineImport(models.Model):  # pylint: disable=too-few-public-methods
    """Add Operating Unit scoping to attendance machine imports.

    Adds the ``operating_unit_id`` field and its access rules via
    ``mixin.single_operating_unit``.
    """

    _name = "attendance_machine_import"
    _inherit = [
        "attendance_machine_import",
        "mixin.single_operating_unit",
    ]

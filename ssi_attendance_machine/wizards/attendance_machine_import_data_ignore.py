# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AttendanceMachineImportDataIgnore(models.TransientModel):
    """
    Wizard to ignore a single attendance machine import data line with a
    reason, opened from the "Ignore" button on the import data line.
    """

    _name = "attendance_machine_import_data_ignore"
    _description = "Attendance Machine Import Data - Ignore"

    @api.model
    def _default_data_id(self):
        return self.env.context.get("active_id", False)

    data_id = fields.Many2one(
        string="Data Line",
        comodel_name="attendance_machine_import.data",
        required=True,
        default=lambda self: self._default_data_id(),
        help="The import data line that will be ignored.",
    )
    reason = fields.Text(
        string="Reason",
        required=True,
        help="Reason why this data line is ignored.",
    )

    def action_confirm(self):
        for record in self.sudo():
            record._confirm()

    def _confirm(self):
        self.ensure_one()
        self.data_id.write({"ignore_reason": self.reason})
        self.data_id.action_ignore()

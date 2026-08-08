# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AttendanceMachineImportIgnore(models.TransientModel):
    """
    Wizard to bulk-ignore every error data line of an attendance machine
    import document with a single shared reason.
    """

    _name = "attendance_machine_import_ignore"
    _description = "Attendance Machine Import - Bulk Ignore Errors"

    @api.model
    def _default_import_id(self):
        """Default ``import_id`` to the record the wizard opened from.

        :return: ``active_id`` from the context, or ``False``
        """
        return self.env.context.get("active_id", False)

    import_id = fields.Many2one(
        string="# Import",
        comodel_name="attendance_machine_import",
        required=True,
        default=lambda self: self._default_import_id(),
        help="The import document whose error data lines will be ignored.",
    )
    reason = fields.Text(
        string="Reason",
        required=True,
        help="Reason applied to every error data line that gets ignored.",
    )

    def action_confirm(self):
        """Bulk-ignore every error data line with the given reason.

        Delegates to ``_confirm`` under ``sudo``.
        """
        for record in self.sudo():
            record._confirm()

    def _confirm(self):
        """Write ``reason`` and ignore every error line of ``import_id``.

        Sets ``ignore_reason`` on all data lines returned by
        ``_get_error_data``, then calls ``action_ignore`` on each.
        """
        self.ensure_one()
        error_data = self.import_id._get_error_data()
        error_data.write({"ignore_reason": self.reason})
        for data_line in error_data:
            data_line.action_ignore()

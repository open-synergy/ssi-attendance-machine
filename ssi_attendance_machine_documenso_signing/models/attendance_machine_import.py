# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceMachineImport(models.Model):
    """Add Documenso e-signature approval to attendance machine imports.

    Adds the Documenso signing tab/flow via
    ``mixin.documenso_signing_approval`` so the import's approval step
    can be signed through Documenso.
    """

    _name = "attendance_machine_import"
    _inherit = [
        "attendance_machine_import",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True

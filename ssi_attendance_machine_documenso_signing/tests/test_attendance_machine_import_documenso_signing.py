# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceMachineImportDocumensoSigning(YamlTransactionCase):
    """Cover Documenso signing approval on ``attendance_machine_import``."""

    def test_attendance_machine_import_documenso_signing(self):
        """Run the Documenso signing YAML scenario."""
        self.run_yaml_scenario(
            "test_data_attendance_machine_import_documenso_signing.yaml"
        )

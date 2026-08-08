# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceMachineOperatingUnit(YamlTransactionCase):
    """Cover Operating Unit scoping on ``attendance_machine_import``."""

    def test_attendance_machine_operating_unit(self):
        """Run the Operating Unit YAML scenario."""
        self.run_yaml_scenario("test_data_attendance_machine_operating_unit.yaml")

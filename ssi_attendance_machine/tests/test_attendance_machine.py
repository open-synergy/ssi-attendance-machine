# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceMachine(YamlTransactionCase):
    """Cover CRUD and constraints of the ``attendance_machine`` model."""

    def test_attendance_machine(self):
        """Run the ``attendance_machine`` YAML scenario."""
        self.run_yaml_scenario("test_data_attendance_machine.yaml")

# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceMachineImportQueueChannel(YamlTransactionCase):
    """Scenario tests for the ``root.attendance_machine`` queue channel."""

    def test_attendance_machine_import_queue_channel(self):
        """Run the queue channel and job function data scenarios."""
        self.run_yaml_scenario("test_attendance_machine_import_queue_channel.yaml")

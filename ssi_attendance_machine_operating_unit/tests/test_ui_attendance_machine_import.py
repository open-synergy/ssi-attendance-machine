# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceMachineImport(HttpSavepointCase):
    """Tour test for the Operating Unit field on ``attendance_machine_import``.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tour below relies on to
    grant the group the delta assertion depends on.
    """

    @classmethod
    def setUpClass(cls):
        """Grant ``admin`` the multi operating unit group.

        Pre-Condition IK: the Operating Unit field is gated by
        ``groups="operating_unit.group_multi_operating_unit"`` in the
        form view -- without membership, the field is never rendered
        and the delta assertion would never find it. ``admin`` also
        needs at least one operating unit assigned so the field has a
        meaningful (non-empty) allowed set. ``admin`` is already a
        member of ``attendance_machine_import_validator_group`` (see
        ``ssi_attendance_machine/security/res_groups/
        attendance_machine_import.xml``), so the Attendance Machine
        Imports menu is already visible and needs no extra grant here.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        operating_unit_partner = cls.env["res.partner"].create(
            {"name": "Tour Attendance Machine Import OU Partner"}
        )
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Tour Attendance Machine Import Operating Unit",
                "code": "TAMIOU",
                "partner_id": operating_unit_partner.id,
            }
        )
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.admin.id)]}
        )
        cls.admin.sudo().write(
            {
                "assigned_operating_unit_ids": [(4, cls.operating_unit.id)],
                "default_operating_unit_id": cls.operating_unit.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/01-create.md (E1 delta --
        Additional Fields)
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_operating_unit_attendance_machine_import_create",
            login="admin",
        )

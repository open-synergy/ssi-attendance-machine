# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceMachineCsvMapping(HttpSavepointCase):
    """Tour tests for the ``attendance_machine_csv_mapping`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed records visible to the browser session.

    Every tour below only walks the standard path documented as the
    numbered Flow in its IK -- File Format = CSV / Delimited Text, Row
    Mode = Single Row, Datetime Mode = Combined. The conditional field
    combinations documented in ``01-create.md`` (Excel; Separate Rows;
    Separate Datetime; Exclude Column + Exclude Values) validate field
    values, not UI shape, and are out of scope for tour coverage.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed the records the tours use."""
        super().setUpClass()
        # Pre-Condition: the CSV Mappings menu is gated by the
        # "Attendance Machine CSV Mapping" group. Without it the tour dies
        # on its first step -- the menu is never rendered for "admin".
        cls.env.ref(
            "ssi_attendance_machine.attendance_machine_csv_mapping_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})
        cls.mapping_edit = cls.env["attendance_machine_csv_mapping"].create(
            {
                "name": "TOUR-CSVMAP-EDIT",
                "code": "/",
            }
        )
        cls.mapping_delete = cls.env["attendance_machine_csv_mapping"].create(
            {
                "name": "TOUR-CSVMAP-DELETE",
                "code": "/",
            }
        )
        cls.mapping_deactivate = cls.env["attendance_machine_csv_mapping"].create(
            {
                "name": "TOUR-CSVMAP-DEACTIVATE",
                "code": "/",
            }
        )
        cls.mapping_activate = cls.env["attendance_machine_csv_mapping"].create(
            {
                "name": "TOUR-CSVMAP-ACTIVATE",
                "code": "/",
                "active": False,
            }
        )
        cls.mapping_reset_code = cls.env["attendance_machine_csv_mapping"].create(
            {
                "name": "TOUR-CSVMAP-RESET-CODE",
                "code": "TOUR-CSVMAP-RESET-CODE-001",
            }
        )

    def test_create(self):
        """Run the create tour for ``attendance_machine_csv_mapping``.

        IK: docs/attendance_machine_csv_mapping/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_csv_mapping_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``attendance_machine_csv_mapping``.

        IK: docs/attendance_machine_csv_mapping/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_csv_mapping_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``attendance_machine_csv_mapping``.

        IK: docs/attendance_machine_csv_mapping/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_csv_mapping_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``attendance_machine_csv_mapping``.

        IK: docs/attendance_machine_csv_mapping/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_csv_mapping_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``attendance_machine_csv_mapping``.

        IK: docs/attendance_machine_csv_mapping/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_csv_mapping_activate",
            login="admin",
        )

    def test_reset_code(self):
        """Run the reset code tour for ``attendance_machine_csv_mapping``.

        IK: docs/attendance_machine_csv_mapping/06-reset-code.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_csv_mapping_reset_code",
            login="admin",
        )

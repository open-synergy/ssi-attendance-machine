# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceMachine(HttpSavepointCase):
    """Tour tests for the ``attendance_machine`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed records visible to the browser session.

    The create/edit tours only walk the standard path documented as the
    numbered Flow in their IK -- Machine Model and CSV Mapping (both
    optional fields on the Configuration tab) are left empty, same as
    Note. The Employees tab is exercised because the IK documents it as
    the operational prerequisite for attendance file import: employees
    must be listed here with their Employee Code, or their file rows end
    up as an import Error.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed the records the tours use."""
        super().setUpClass()
        # Pre-Condition: the Attendance Machines menu is gated by the
        # "Attendance Machine" group. Without it the tour dies on its
        # first step -- the menu is never rendered for "admin".
        cls.env.ref("ssi_attendance_machine.attendance_machine_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )
        cls.employee_create = cls.env["hr.employee"].create(
            {"name": "TOUR-MACHINE-EMP-CREATE"}
        )
        cls.employee_edit = cls.env["hr.employee"].create(
            {"name": "TOUR-MACHINE-EMP-EDIT"}
        )
        cls.machine_edit = cls.env["attendance_machine"].create(
            {
                "name": "TOUR-MACHINE-EDIT",
                "code": "/",
            }
        )
        cls.machine_delete = cls.env["attendance_machine"].create(
            {
                "name": "TOUR-MACHINE-DELETE",
                "code": "/",
            }
        )
        cls.machine_deactivate = cls.env["attendance_machine"].create(
            {
                "name": "TOUR-MACHINE-DEACTIVATE",
                "code": "/",
            }
        )
        cls.machine_activate = cls.env["attendance_machine"].create(
            {
                "name": "TOUR-MACHINE-ACTIVATE",
                "code": "/",
                "active": False,
            }
        )
        cls.machine_reset_code = cls.env["attendance_machine"].create(
            {
                "name": "TOUR-MACHINE-RESET-CODE",
                "code": "TOUR-RESET-CODE-001",
            }
        )

    def test_create(self):
        """Run the create tour for ``attendance_machine``.

        IK: docs/attendance_machine/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``attendance_machine``.

        IK: docs/attendance_machine/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``attendance_machine``.

        IK: docs/attendance_machine/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``attendance_machine``.

        IK: docs/attendance_machine/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``attendance_machine``.

        IK: docs/attendance_machine/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_activate",
            login="admin",
        )

    def test_reset_code(self):
        """Run the reset code tour for ``attendance_machine``.

        IK: docs/attendance_machine/06-reset-code.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_reset_code",
            login="admin",
        )

# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import json

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceMachineImport(HttpSavepointCase):
    """Tour tests for the ``attendance_machine_import`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to seed
    records visible to the browser session.

    Three scope boundaries are fixed by Keputusan Desain (issue
    open-synergy/ssi-attendance-machine#31) and repeated on the matching
    ``test_*`` docstring and tour comment below:

    - ``01-create``: the tour fills **Date** and **Machine** then Save.
      **Attendance File** is a binary upload, never exercised by this
      tour -- the records used by every other tour below get their
      ``attendance_file``/``data_ids`` content seeded directly through the
      ORM instead of through the **Load Data** button.
    - ``09-finish``: the tour walks the inline row-handling actions on a
      **Queue To Done** record, then asserts the statusbar stays on
      **Queue To Done** -- the ``queue_done`` -> ``done`` transition is
      driven by a ``base.automation`` reacting to queue job completion,
      never a click.
    - ``10-cancel``: the tour stops once the statusbar leaves
      **Draft**/**Waiting for Approval** for **Queue To Cancel** -- the
      ``queue_cancel`` -> ``cancel`` transition is also
      ``base.automation``-driven.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one machine and one pre-condition record per IK tour.

        ``base.user_admin`` is already a member of
        ``attendance_machine_import_validator_group`` (which implies the
        ``User`` and ``Viewer`` groups) via ``ssi_attendance_machine``'s
        security data, so it can open the menu, confirm, approve, reject,
        cancel and restart directly, without extra group setup.

        Each record below gets its own dedicated ``attendance_machine`` so
        the tour can find its row in the list by the **Machine** column --
        ``name`` stays ``"/"`` on every record here (the sequence is only
        assigned on **Done**, see ``_create_sequence_state``), so it cannot
        be used as a row marker.

        Queue processing (``action_queue_done``/``action_queue_cancel``)
        enqueues one job per **Import Data** row via ``with_delay()``. No
        job runner executes in this test environment, so those jobs stay
        pending -- exactly what the ``queue_done``/``queue_cancel``
        pre-conditions need. Where a row's resulting **Done**/**Error**
        state matters (``09-finish``, ``10-cancel``, ``15-ignore-all``),
        ``_process_ignoring_error`` calls ``_process_attendance()``
        directly instead, bypassing the queue entirely. Since issue
        open-synergy/ssi-attendance-machine#51, ``_process_attendance()``
        re-raises after recording the error on the line, so rows
        deliberately seeded with an unregistered employee code (to end
        up **Error**, for the Retry/Edit/Ignore tours) would otherwise
        abort ``setUpClass`` -- ``_process_ignoring_error`` discards that
        expected exception, keeping the resulting ``state``/
        ``error_message`` already written on the line.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        cls.csv_mapping = (
            cls.env["attendance_machine_csv_mapping"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour AMI CSV Mapping",
                    "code": "TOURAMICM",
                    "file_encoding": "utf-8",
                    "delimiter": "comma",
                    "row_mode": "single",
                    "datetime_mode": "combined",
                    "employee_column": "employee_code",
                    "check_in_column": "check_in",
                    "check_out_column": "check_out",
                    "datetime_format": "%Y-%m-%d %H:%M:%S",
                }
            )
        )
        cls.employee_valid = cls.env["hr.employee"].create(
            {"name": "TOUR AMI EMPLOYEE"}
        )
        cls.timesheet = (
            cls.env["hr.timesheet"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": cls.employee_valid.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-01-31",
                    "working_schedule_id": cls.env["resource.calendar"]
                    .search([], limit=1)
                    .id,
                }
            )
        )
        cls.timesheet.with_context(bypass_policy_check=True).action_open()

        # Pre-Condition for the cancel tour: a global-use cancellation
        # reason so it appears in the Select Cancel Reason wizard.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR AMI CANCEL REASON",
                "code": "TOURAMICXL",
                "global_use": True,
            }
        )

        # ── 01-create ──────────────────────────────────────────────────
        # The record itself is created by the tour; only the machine it
        # will select from the Machine field is prepared here.
        cls.machine_create = cls._create_machine("TOUR AMI CREATE MACHINE")

        # ── 02-edit ────────────────────────────────────────────────────
        cls.machine_edit = cls._create_machine(
            "TOUR AMI EDIT MACHINE", with_mapping=True
        )
        cls._register_employee(cls.machine_edit, "EMPVALID")
        cls.import_edit = cls._create_import(cls.machine_edit, "2026-01-10")
        cls.import_edit.write(
            {
                "attendance_file": cls._build_csv_content(
                    [("EMPVALID", "2026-01-10 08:00:00", "2026-01-10 17:00:00")]
                ),
                "attendance_file_name": "tour_edit.csv",
            }
        )
        cls.import_edit.action_load_data()

        # ── 03-delete ──────────────────────────────────────────────────
        cls.machine_delete = cls._create_machine("TOUR AMI DELETE MACHINE")
        cls.import_delete = cls._create_import(cls.machine_delete, "2026-01-11")

        # ── 04-confirm ─────────────────────────────────────────────────
        cls.machine_confirm = cls._create_machine("TOUR AMI CONFIRM MACHINE")
        cls.import_confirm = cls._create_import(cls.machine_confirm, "2026-01-12")

        # ── 05-approve ─────────────────────────────────────────────────
        # One unprocessed data line is seeded before Confirm so that
        # Approve's resulting action_queue_done() finds a non-empty
        # data_ids and enqueues a job -- without it, _set_done_if_no_job()
        # would skip Queue To Done and jump straight to Done.
        cls.machine_approve = cls._create_machine("TOUR AMI APPROVE MACHINE")
        cls.import_approve = cls._create_import(cls.machine_approve, "2026-01-13")
        cls._seed_draft_line(cls.import_approve, "EMPVALID", "2026-01-13 08:00:00")
        cls.import_approve.with_context(bypass_policy_check=True).action_confirm()

        # ── 06-reject ──────────────────────────────────────────────────
        cls.machine_reject = cls._create_machine("TOUR AMI REJECT MACHINE")
        cls.import_reject = cls._create_import(cls.machine_reject, "2026-01-14")
        cls.import_reject.with_context(bypass_policy_check=True).action_confirm()

        # ── 09-finish ──────────────────────────────────────────────────
        # 1 row will resolve to Done, 3 rows use an unregistered employee
        # code and will resolve to Error -- enough Error rows for Retry,
        # Edit Data, Ignore and Retry All Errors to each act on a
        # different row without ever fully resolving the document (it
        # must stay on Queue To Done for the Post-Condition assertion).
        cls.machine_finish = cls._create_machine(
            "TOUR AMI FINISH MACHINE", with_mapping=True
        )
        cls._register_employee(cls.machine_finish, "EMPVALID")
        cls.import_finish = cls._create_import(cls.machine_finish, "2026-01-15")
        line_done = cls._seed_draft_line(
            cls.import_finish, "EMPVALID", "2026-01-15 08:00:00"
        )
        line_retry = cls._seed_draft_line(
            cls.import_finish, "EMPUNKNOWN1", "2026-01-15 08:00:00"
        )
        line_edit = cls._seed_draft_line(
            cls.import_finish, "EMPUNKNOWN2", "2026-01-15 08:00:00"
        )
        line_ignore = cls._seed_draft_line(
            cls.import_finish, "EMPUNKNOWN3", "2026-01-15 08:00:00"
        )
        cls.import_finish.with_context(bypass_policy_check=True).action_confirm()
        cls.import_finish.invalidate_cache()
        cls.import_finish.with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        for line in (line_done, line_retry, line_edit, line_ignore):
            cls._process_ignoring_error(line)

        # ── 10-cancel ──────────────────────────────────────────────────
        # A single row is processed to Done and the document is forced to
        # Done via `_try_action_done` (same helper the base.automation
        # itself calls), giving Cancel a realistic "already Done" record
        # with a real linked attendance to remove.
        cls.machine_cancel = cls._create_machine(
            "TOUR AMI CANCEL MACHINE", with_mapping=True
        )
        cls._register_employee(cls.machine_cancel, "EMPVALID")
        cls.import_cancel = cls._create_import(cls.machine_cancel, "2026-01-16")
        line_cancel = cls._seed_draft_line(
            cls.import_cancel, "EMPVALID", "2026-01-16 08:00:00"
        )
        cls.import_cancel.with_context(bypass_policy_check=True).action_confirm()
        cls.import_cancel.invalidate_cache()
        cls.import_cancel.with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        cls._process_ignoring_error(line_cancel)
        cls.import_cancel._try_action_done()

        # ── 12-restart ─────────────────────────────────────────────────
        # restart_ok grants state in (cancel, reject); reject is reached
        # with a single Confirm + Reject, no data/queue setup required.
        cls.machine_restart = cls._create_machine("TOUR AMI RESTART MACHINE")
        cls.import_restart = cls._create_import(cls.machine_restart, "2026-01-17")
        cls.import_restart.with_context(bypass_policy_check=True).action_confirm()
        cls.import_restart.invalidate_cache()
        cls.import_restart.with_context(
            bypass_policy_check=True
        ).action_reject_approval()

        # ── 13-reset-number ────────────────────────────────────────────
        cls.machine_reset_number = cls._create_machine("TOUR AMI RESET NUMBER MACHINE")
        cls.import_reset_number = cls._create_import(
            cls.machine_reset_number, "2026-01-18"
        )

        # ── 14-restart-approval ────────────────────────────────────────
        # restart_approval_ok only grants the button when the confirmed
        # record has NO approval_template_id yet -- the stalled-without-
        # an-approver scenario the button exists to recover from. The
        # demo approval template matches every record, so it is
        # deactivated for the duration of this one action_confirm() call
        # then reactivated immediately, exactly as the tour itself needs
        # it active when it later clicks Restart Approval Process.
        cls.machine_restart_approval = cls._create_machine(
            "TOUR AMI RESTART APPROVAL MACHINE"
        )
        cls.import_restart_approval = cls._create_import(
            cls.machine_restart_approval, "2026-01-19"
        )
        approval_template = cls.env.ref(
            "ssi_attendance_machine.attendance_machine_import_approval_template"
        ).sudo()
        approval_template.write({"active": False})
        cls.import_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        approval_template.write({"active": True})

        # ── 15-ignore-all-errors ───────────────────────────────────────
        # Both rows use an unregistered employee code, so both resolve to
        # Error and stay unresolved -- the wizard has two rows to act on.
        cls.machine_ignore_all = cls._create_machine(
            "TOUR AMI IGNORE ALL MACHINE", with_mapping=True
        )
        cls.import_ignore_all = cls._create_import(cls.machine_ignore_all, "2026-01-20")
        line_ignore_all_1 = cls._seed_draft_line(
            cls.import_ignore_all, "EMPUNKNOWN4", "2026-01-20 08:00:00"
        )
        line_ignore_all_2 = cls._seed_draft_line(
            cls.import_ignore_all, "EMPUNKNOWN5", "2026-01-20 08:00:00"
        )
        cls.import_ignore_all.with_context(bypass_policy_check=True).action_confirm()
        cls.import_ignore_all.invalidate_cache()
        cls.import_ignore_all.with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        for line in (line_ignore_all_1, line_ignore_all_2):
            cls._process_ignoring_error(line)

    @classmethod
    def _create_machine(cls, name, with_mapping=False):
        """Create an ``attendance_machine`` with a unique, searchable name.

        :param name: unique name used by the tour to find its list row.
        :param with_mapping: link ``cls.csv_mapping`` when the machine's
            records need ``action_load_data``/``_process_attendance`` to
            actually parse rows.
        """
        vals = {"name": name, "code": "/"}
        if with_mapping:
            vals["csv_mapping_id"] = cls.csv_mapping.id
        return cls.env["attendance_machine"].with_user(cls.admin).create(vals)

    @classmethod
    def _register_employee(cls, machine, employee_code):
        """Register ``cls.employee_valid`` on ``machine`` under a code."""
        cls.env["attendance_machine.employee"].create(
            {
                "machine_id": machine.id,
                "employee_id": cls.employee_valid.id,
                "employee_code": employee_code,
            }
        )

    @classmethod
    def _create_import(cls, machine, date):
        """Create a draft ``attendance_machine_import`` for ``machine``."""
        return (
            cls.env["attendance_machine_import"]
            .with_user(cls.admin)
            .create({"date": date, "machine_id": machine.id})
        )

    @classmethod
    def _build_csv_content(cls, rows):
        """Return a base64-encoded single-row-mode attendance CSV.

        :param rows: list of ``(employee_code, check_in, check_out)``
            string tuples, matching ``cls.csv_mapping``'s columns.
        """
        lines = ["employee_code,check_in,check_out"]
        lines += ["{},{},{}".format(*row) for row in rows]
        return base64.b64encode("\n".join(lines).encode("utf-8"))

    @classmethod
    def _seed_draft_line(cls, record, employee_code, check_in):
        """Create one unprocessed ``attendance_machine_import.data`` row.

        Bypasses ``action_load_data`` and the CSV file entirely -- the raw
        JSON a real upload would have produced is written directly, so
        the row is ready for ``action_queue_done`` to enqueue a job for,
        or for ``_process_attendance()`` to be called on directly (see
        :meth:`_seed_draft_line`'s callers).
        """
        return cls.env["attendance_machine_import.data"].create(
            {
                "import_id": record.id,
                "sequence": len(record.data_ids) + 1,
                "data": json.dumps(
                    {"employee_code": employee_code, "check_in": check_in}
                ),
            }
        )

    @classmethod
    def _process_ignoring_error(cls, line):
        """Call ``_process_attendance()``, tolerating an expected failure.

        Since issue open-synergy/ssi-attendance-machine#51,
        ``_process_attendance()`` re-raises after recording the error on
        the line -- exactly what makes the real queue job end up
        ``failed``. These fixtures deliberately process rows with an
        unregistered employee code to seed an **Error** row for the
        Retry/Edit/Ignore/Retry-All-Errors tours; the row already
        carries the resulting ``state``/``error_message`` once
        ``_process_attendance()`` returns or raises, so the exception
        itself is discarded here rather than aborting ``setUpClass``.

        :param line: ``attendance_machine_import.data`` record to
            process
        """
        try:
            line._process_attendance()
        except Exception:  # pylint: disable=broad-except
            pass

    def test_create(self):
        """Run the create tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/01-create.md

        Boundary: the tour fills **Date** and **Machine** then Save --
        **Attendance File** is a binary upload not exercised here (see
        class docstring and Keputusan Desain, issue
        open-synergy/ssi-attendance-machine#31).
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/09-finish.md

        Boundary: the tour walks the inline row-handling actions (Retry,
        Edit Data, Ignore, Retry All Errors, Requeue, Recompute Queue
        Done Result) on a Queue To Done record, then asserts the
        statusbar stays on Queue To Done -- the queue_done -> done
        transition is base.automation-driven, not a click (see class
        docstring and Keputusan Desain, issue
        open-synergy/ssi-attendance-machine#31).
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/10-cancel.md

        Boundary: the tour stops once the statusbar leaves Done for
        Queue To Cancel -- the queue_cancel -> cancel transition is
        base.automation-driven, not a click (see class docstring and
        Keputusan Desain, issue open-synergy/ssi-attendance-machine#31).
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``attendance_machine_import``.

        IK: docs/attendance_machine_import/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour.

        IK: docs/attendance_machine_import/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour.

        IK: docs/attendance_machine_import/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_restart_approval",
            login="admin",
        )

    def test_ignore_all_errors(self):
        """Run the ignore all errors tour.

        IK: docs/attendance_machine_import/15-ignore-all-errors.md

        Boundary: the tour only proves the wizard opens, accepts a
        Reason, and closes back to the form -- it does not assert the
        resulting Error/Ignored counts (unit test territory) nor the
        document's possible side-effect transition to Done (see class
        docstring and Keputusan Desain, issue
        open-synergy/ssi-attendance-machine#31).
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_attendance_machine_import_ignore_all_errors",
            login="admin",
        )

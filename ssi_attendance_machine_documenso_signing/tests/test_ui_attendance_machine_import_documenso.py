# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceMachineImportDocumenso(HttpSavepointCase):
    """Tour test for the ``attendance_machine_import`` Documenso delta."""

    @classmethod
    def setUpClass(cls):
        """Create one attendance machine import already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``attendance_machine_import_validator_group`` (which implies the
        ``User`` group) via ``ssi_attendance_machine``'s security data, so it
        can confirm the record directly, without extra group setup. The
        record is moved to ``confirm`` here in Python
        (``action_confirm()``), not via UI clicks, per Keputusan Desain
        (issue open-synergy/ssi-attendance-machine#30).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        machine_model = (
            cls.env["attendance_machine_model"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour AMI Documenso Model",
                    "code": "TOURAMIDM",
                }
            )
        )
        csv_mapping = (
            cls.env["attendance_machine_csv_mapping"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour AMI Documenso CSV Mapping",
                    "code": "TOURAMIDC",
                    "file_encoding": "utf-8",
                    "delimiter": "comma",
                    "row_mode": "single",
                    "datetime_mode": "combined",
                    "employee_column": "employee_id",
                    "check_in_column": "check_in",
                    "check_out_column": "check_out",
                    "datetime_format": "%Y-%m-%d %H:%M:%S",
                }
            )
        )
        machine = (
            cls.env["attendance_machine"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour AMI Documenso Machine",
                    "code": "TOURAMIDA",
                    "attendance_model_id": machine_model.id,
                    "csv_mapping_id": csv_mapping.id,
                }
            )
        )

        # Pre-Condition IK 05-approve.md (delta): record already Waiting for
        # Approval. The "Standard" approval template used by
        # ssi_attendance_machine demo data has no Documenso Signing Template
        # configured, so the Signature Requests tab is present
        # (``_documenso_signing_create_page = True``) but the base
        # Approve/OK Flow is unaffected -- this tour does not exercise it.
        cls.machine_import_approve = (
            cls.env["attendance_machine_import"]
            .with_user(cls.admin)
            .create(
                {
                    "date": "2026-01-15",
                    "machine_id": machine.id,
                }
            )
        )
        cls.machine_import_approve.with_context(
            bypass_policy_check=True
        ).action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/attendance_machine_import/05-approve.md (E2a delta --
        Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_attendance_machine_documenso_signing_attendance_machine_import_approve",
            login="admin",
        )

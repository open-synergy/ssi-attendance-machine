# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import csv
import hashlib
import io
import json

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class AttendanceMachineImport(models.Model):  # pylint: disable=too-few-public-methods
    """
    Transactional document for importing attendance data from a machine.
    Reads a CSV file, creates raw data lines, then processes them via
    queue jobs to create/update hr.timesheet_attendance records.

    Lifecycle: draft → confirm → queue_done → done
    Cancellation: queue_cancel → cancel
    """

    _name = "attendance_machine_import"
    _description = "Attendance Machine Import"
    _inherit = [
        "mixin.transaction_queue_cancel",
        "mixin.transaction_queue_done",
        "mixin.transaction_confirm",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "action_queue_done"
    _approval_state = "confirm"
    _after_approved_method = "action_queue_done"

    # View auto-insert attributes
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False
    _queue_processing_create_page = True
    _automatically_insert_queue_done_button = False
    _automatically_insert_queue_cancel_button = False

    _queue_to_done_insert_form_element_ok = True
    _queue_to_done_form_xpath = "//group[@name='queue_processing']"

    _queue_to_cancel_insert_form_element_ok = True
    _queue_to_cancel_form_xpath = "//group[@name='queue_processing']"

    _method_to_run_from_wizard = "action_queue_cancel"

    _statusbar_visible_label = "draft,confirm,queue_done,done"

    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "queue_cancel_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "queue_done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_queue_done",
        "dom_done",
        "dom_terminate",
        "dom_queue_cancel",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: fields.Date.today(),
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Import date.",
    )
    machine_id = fields.Many2one(
        string="Machine",
        comodel_name="attendance_machine",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="The attendance machine this import belongs to.",
    )
    attendance_file = fields.Binary(
        string="Attendance File",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="The CSV attendance data file exported from the machine.",
    )
    attendance_file_name = fields.Char(
        string="File Name",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    attendance_file_hash = fields.Char(
        string="File Hash",
        readonly=True,
        copy=False,
        help="SHA-256 hash of the uploaded attendance file. Used to detect duplicate imports.",
    )
    data_ids = fields.One2many(
        string="Import Data",
        comodel_name="attendance_machine_import.data",
        inverse_name="import_id",
        readonly=True,
    )
    num_of_data = fields.Integer(
        string="# Data",
        compute="_compute_num_of_data",
        compute_sudo=True,
        help="Total number of import data lines.",
    )
    num_of_done = fields.Integer(
        string="# Done",
        compute="_compute_num_of_data",
        compute_sudo=True,
        help="Number of import data lines successfully converted into "
        "attendance records.",
    )
    num_of_error = fields.Integer(
        string="# Error",
        compute="_compute_num_of_data",
        compute_sudo=True,
        help="Number of import data lines that failed to be converted "
        "into attendance records.",
    )
    num_of_ignored = fields.Integer(
        string="# Ignored",
        compute="_compute_num_of_data",
        compute_sudo=True,
        help="Number of import data lines excluded from the import.",
    )

    @api.depends("data_ids.state")
    def _compute_num_of_data(self):
        for record in self:
            record.num_of_data = len(record.data_ids)
            record.num_of_done = len(
                record.data_ids.filtered(lambda d: d.state == "done")
            )
            record.num_of_error = len(
                record.data_ids.filtered(lambda d: d.state == "error")
            )
            record.num_of_ignored = len(
                record.data_ids.filtered(lambda d: d.state == "ignored")
            )

    @api.constrains("attendance_file_hash")
    def _check_duplicate_file(self):
        for record in self:
            if not record.attendance_file_hash:
                continue
            duplicate = self.search(
                [
                    ("attendance_file_hash", "=", record.attendance_file_hash),
                    ("id", "!=", record.id),
                    ("state", "!=", "cancel"),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    _(  # pylint: disable=translation-positional-used
                        """
Context: Uploading attendance file
Document: %s
Problem: This file has already been imported (see document: %s)
Solution: Check the existing import or use a different file"""
                    )
                    % (
                        record.name or str(record.id),
                        duplicate.name or str(duplicate.id),
                    )
                )

    def action_load_data(self):  # pylint: disable=too-many-locals
        """
        Delete existing data lines, read the attendance file, and create
        one data line per row with the raw row data stored as JSON.
        """
        self.ensure_one()

        if self.data_ids:
            self.data_ids.unlink()

        if not self.attendance_file:
            return True

        mapping = self.machine_id.csv_mapping_id
        file_content = base64.b64decode(self.attendance_file)
        self.attendance_file_hash = hashlib.sha256(file_content).hexdigest()

        encoding = "utf-8"
        if mapping and mapping.file_encoding:
            encoding = mapping.file_encoding
        content_str = file_content.decode(encoding)

        delimiter = ","
        if mapping:
            delimiter = mapping._get_column_delimiter_character()

        quotechar = '"'
        if mapping and mapping.quotechar:
            quotechar = mapping.quotechar

        offset_row = mapping.offset_row if mapping else 0
        no_header = mapping.no_header if mapping else False
        skip_empty = mapping.skip_empty_lines if mapping else False

        lines_io = io.StringIO(content_str)
        reader = csv.reader(lines_io, delimiter=delimiter, quotechar=quotechar)

        data_vals = []
        headers = None
        seq = 1

        for i, row in enumerate(reader):
            # Skip offset rows from the top
            if i < offset_row:
                continue
            # Skip empty lines
            if skip_empty and not any(cell.strip() for cell in row):
                continue
            # First non-skipped row is the header (if file has header)
            if not no_header and headers is None:
                headers = row
                continue
            # Convert row to dict using header keys, or numeric index
            if headers:
                row_data = dict(zip(headers, row))
            else:
                row_data = {str(j): v for j, v in enumerate(row)}

            data_vals.append(
                {
                    "import_id": self.id,
                    "sequence": seq,
                    "data": json.dumps(row_data),
                }
            )
            seq += 1

        if data_vals:
            self.env["attendance_machine_import.data"].create(data_vals)

        return True

    @ssi_decorator.post_queue_done_action()
    def _01_process_attendance_data_on_queue_done(self):
        self.ensure_one()
        for data_line in self.data_ids:
            description = f"Process attendance import data line ID {data_line.id}"
            job = (
                data_line.with_context(job_batch=self.done_queue_job_batch_id)
                .with_delay(description=_(description))
                ._process_attendance()
            )
            data_line.queue_job_id = job.db_record().id

    @ssi_decorator.post_queue_cancel_action()
    def _01_cancel_attendance_data_on_queue_cancel(self):
        self.ensure_one()
        for data_line in self.data_ids.filtered(lambda d: d.attendance_id):
            description = f"Cancel attendance import data line ID {data_line.id}"
            data_line.with_context(job_batch=self.cancel_queue_job_batch_id).with_delay(
                description=_(description)
            )._cancel_attendance()

    def action_retry_all_error(self):
        for record in self.sudo():
            record._retry_all_error()

    def _retry_all_error(self):
        self.ensure_one()
        for data_line in self._get_error_data():
            data_line.action_retry()

    def _get_error_data(self):
        self.ensure_one()
        return self.data_ids.filtered(lambda d: d.state == "error")

    def _get_unfinished_data(self):
        self.ensure_one()
        return self.data_ids.filtered(lambda d: d.state in ("draft", "error"))

    def _force_pending_queue_job_done(self):
        self.ensure_one()
        for job in self.done_queue_job_ids.filtered(lambda j: j.state != "done"):
            job.button_done()

    def _recompute_queue_done_result(self):
        self.ensure_one()
        self.done_queue_job_batch_id.enqueue()
        self._try_action_done()

    def _try_action_done(self):
        self.ensure_one()
        if self.state != "queue_done":
            return True
        if self._get_unfinished_data():
            return True
        self._force_pending_queue_job_done()
        batch = self.done_queue_job_batch_id
        if batch:
            batch.check_state()
        self.action_done()
        return True

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "queue_done_ok",
            "queue_cancel_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

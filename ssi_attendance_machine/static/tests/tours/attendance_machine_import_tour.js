odoo.define("ssi_attendance_machine.attendance_machine_import_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Attendance Machine
    // Imports. "Timesheets" (level 2, ssi_timesheet.timesheet_menu) has no
    // action of its own but is still rendered as a clickable dropdown
    // section (unlike a doubly-nested actionless submenu, which gets
    // flattened -- see attendance_machine_tour.js for that other case).
    function openAttendanceMachineImportMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Timesheets menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_timesheet.timesheet_menu"]',
            },
            {
                content: "Open the Attendance Machine Imports menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_attendance_machine.attendance_machine_import_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view --
                // the app landing action is also a .o_list_view.
                content: "Attendance Machine Imports list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Attendance Machine Imports)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Open the record whose row is identified by its Machine column --
    // `name` stays "/" on every record here (the sequence is only
    // assigned on Done), so it cannot be used as a row marker.
    function openImportByMachineSteps(machineName) {
        return [
            {
                content: "Open the record (" + machineName + ")",
                trigger: ".o_data_row:contains(" + machineName + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/attendance_machine_import/01-create.md
    //
    // Scope: the tour fills Date and Machine then Save. Attendance File is
    // a binary upload, never exercised here -- see the test file's class
    // docstring and Keputusan Desain, issue
    // open-synergy/ssi-attendance-machine#31.
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineImportMenuSteps(), [
            // ── Flow 2 — Click the New button (14.0: "Create")
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Flow 3 — Fill in the required fields. Date is already
            // filled with today's date by default (left unchanged); only
            // Machine has no default and must be selected.
            {
                content: "Select the Machine",
                trigger: ".o_field_widget[name='machine_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR AMI CREATE MACHINE",
            },
            {
                content: "Pick the machine from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR AMI CREATE MACHINE)",
            },

            // ── Flow 4 — Import Data tab: click Load Data. No Attendance
            // File was uploaded (out of scope, see above), so this is a
            // no-op besides clearing any existing (empty) data lines --
            // exercised here only because it is an inline action of this
            // IK.
            {
                content: "Open the Import Data tab",
                trigger: ".o_notebook .nav-link:contains(Import Data)",
            },
            {
                content: "Click Load Data",
                trigger: ".o_form_view button[name='action_load_data']",
            },

            // ── Flow 5 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Post-Condition — record created and shown in the list
            {
                content: "Back to the Attendance Machine Imports list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machine Imports)",
            },
            {
                content: "New record is displayed in the list",
                trigger: ".o_data_row:contains(TOUR AMI CREATE MACHINE)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine_import/02-edit.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI EDIT MACHINE"),
            [
                // ── Flow 3 — Change Date as needed
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Change Date",
                    trigger: ".o_field_widget[name='date'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 01/12/2026",
                },

                // ── Flow 4 — Import Data tab: click Load Data to discard
                // and re-read the current Attendance File. The
                // Pre-Condition record already has one loaded row.
                {
                    content: "Open the Import Data tab",
                    trigger: ".o_notebook .nav-link:contains(Import Data)",
                },
                {
                    content: "Click Load Data",
                    trigger: ".o_form_view button[name='action_load_data']",
                },

                // ── Flow 5 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/03-delete.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineImportMenuSteps(), [
            // ── Flow 2 — Select the record's checkbox (delete is done
            // from the list view, without opening the record first)
            {
                content: "Select the record's checkbox",
                trigger:
                    ".o_data_row:contains(TOUR AMI DELETE MACHINE) " +
                    ".o_list_record_selector input",
                run: "click",
            },

            // ── Flow 3 — Click Action > Delete
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // Match the exact label so "Archive" is never picked
                // instead.
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // ── Flow 4 — Click OK to confirm
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — record permanently removed
            {
                content: "Deleted record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR AMI DELETE MACHINE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine_import/04-confirm.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI CONFIRM MACHINE"),
            [
                // ── Flow 3 — Click the Confirm button
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — Status changes to Waiting for Approval
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/05-approve.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI APPROVE MACHINE"),
            [
                // ── Flow 3 — Click the Approve button. The Pre-Condition
                // record carries one unprocessed data line, so
                // action_queue_done() enqueues a job and the document
                // lands on Queue To Done rather than skipping straight to
                // Done.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — this is the only pending approval
                // level, so status automatically changes to Queue To
                // Done via action_queue_done().
                {
                    content: "Status is Queue To Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='queue_done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/06-reject.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI REJECT MACHINE"),
            [
                // ── Flow 3 — Click the Reject button
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — Status changes to Rejected
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/09-finish.md
    //
    // Scope: the tour walks the inline row-handling actions on a Queue To
    // Done record, then asserts the statusbar stays on Queue To Done --
    // the queue_done -> done transition is base.automation-driven, not a
    // click. See the test file's class docstring and Keputusan Desain,
    // issue open-synergy/ssi-attendance-machine#31.
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI FINISH MACHINE"),
            [
                // ── Flow 3 — Import Data tab: counters are shown, values
                // are not asserted (unit test territory)
                {
                    content: "Open the Import Data tab",
                    trigger: ".o_notebook .nav-link:contains(Import Data)",
                },

                // ── Flow 4 — Resolve error rows via the row-level actions.
                // Rows are ordered by sequence: row 0 is already Done
                // (hidden buttons), rows 1-3 are Error.
                {
                    content: "Click Retry on the first error row",
                    trigger:
                        ".o_field_widget[name='data_ids'] .o_data_row:eq(1) " +
                        "button[name='action_retry']:enabled",
                },
                {
                    content: "Open Edit Data on the second error row",
                    trigger:
                        ".o_field_widget[name='data_ids'] .o_data_row:eq(2) " +
                        "button[name='action_open_edit_data_wizard']:enabled",
                },
                {
                    // 14.0: trigger inside an open modal is scoped to it --
                    // never prefixed with ".modal".
                    content: "Edit Data wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Confirm the Edit Data wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    content: "Open Ignore on the third error row",
                    trigger:
                        "body:not(:has(.modal)) " +
                        ".o_field_widget[name='data_ids'] .o_data_row:eq(3) " +
                        "button[name='action_open_ignore_wizard']:enabled",
                },
                {
                    content: "Ignore wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    // A Text field without a label renders the <textarea>
                    // itself carrying the o_field_widget class and name
                    // attribute -- no wrapper div to descend into.
                    content: "Fill in the Reason",
                    trigger: "textarea.o_field_widget[name='reason']",
                    run: "text Tour ignore reason",
                },
                {
                    content: "Confirm the Ignore wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    content: "Click Retry All Errors",
                    trigger:
                        "body:not(:has(.modal)) " +
                        ".o_form_view button[name='action_retry_all_error']:enabled",
                },

                // ── Flow 5-6 — Queue Processing tab: Requeue and
                // Recompute Queue Done Result
                {
                    content: "Open the Queue Processing tab",
                    trigger: ".o_notebook .nav-link:contains(Queue Processing)",
                },
                {
                    // Action_requeue_done has no confirm= attribute, so no
                    // dialog follows (Keputusan Desain, issue
                    // open-synergy/ssi-attendance-machine#24).
                    content: "Click the Requeue button",
                    trigger: ".o_form_view button[name='action_requeue_done']",
                },
                {
                    content: "Requeue call has completed",
                    trigger: "button[name='action_requeue_done']:enabled",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Click Recompute Queue Done Result",
                    trigger:
                        ".o_form_view button[name='action_recompute_queue_done_result']",
                },

                // ── Flow 7 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — Error rows remain unresolved (the
                // first row keeps failing on retry), so the document stays
                // on Queue To Done.
                {
                    content: "Status is still Queue To Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='queue_done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/10-cancel.md
    //
    // Scope: the tour stops once the statusbar leaves Done for Queue To
    // Cancel -- the queue_cancel -> cancel transition is
    // base.automation-driven, not a click. See the test file's class
    // docstring and Keputusan Desain, issue
    // open-synergy/ssi-attendance-machine#31.
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI CANCEL MACHINE"),
            [
                // ── Flow 3 — Click the Cancel button. It opens the Select
                // Cancel Reason wizard directly (header button is a
                // type="action" wizard opener, not action_cancel itself).
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains(Cancel)",
                    extra_trigger: ".o_form_view",
                },
                {
                    // 14.0: trigger inside an open modal is scoped to it --
                    // never prefixed with ".modal".
                    content: "The cancellation reason wizard is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Flow 4 — Select the Reason
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] .o_radio_item " +
                        "label:contains(TOUR AMI CANCEL REASON)",
                },

                // ── Flow 5 — Click Confirm
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // ── Flow 6 — Click OK on the confirmation dialog. The
                // wizard Confirm (confirm="Are you sure?") opens a second
                // modal on top; the tour scopes to the topmost modal.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                },

                // ── Post-Condition — Status immediately changes to Queue
                // To Cancel via action_queue_cancel(). No queue job runner
                // processes the resulting cancellation job in this test
                // environment, so it never reaches Cancelled here.
                {
                    content: "Status is Queue To Cancel",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='queue_cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/12-restart.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI RESTART MACHINE"),
            [
                // ── Flow 3 — Click the Restart button
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — Status returns to Draft
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/13-reset-number.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI RESET NUMBER MACHINE"),
            [
                // ── Flow 3 — Click the Reset Document Number button
                {
                    content: "Click the Reset Document Number button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reset_document_number']",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — dialog closes and the form is
                // re-rendered; the resulting Document Number value is not
                // asserted (unit test territory).
                {
                    content: "The form is displayed again",
                    trigger: "body:not(:has(.modal)) .o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/14-restart-approval.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI RESTART APPROVAL MACHINE"),
            [
                // ── Flow 3 — Click the Restart Approval Process button
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },

                // ── Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — a new approval process is started;
                // the Approvals tab now shows at least one approval line
                // where before (no approval_template_id, see setUpClass)
                // there could be none.
                {
                    content: "Open the Approvals tab",
                    trigger: ".o_notebook .nav-link:contains(Approvals)",
                    extra_trigger: "body:not(:has(.modal))",
                },
                {
                    content: "The approval process has been rebuilt",
                    trigger: ".o_field_widget[name='approval_ids'] .o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/attendance_machine_import/15-ignore-all-errors.md
    //
    // Scope: the tour only proves the wizard opens, accepts a Reason, and
    // closes back to the form -- it does not assert the resulting
    // Error/Ignored counts (unit test territory) nor the document's
    // possible side-effect transition to Done. See the test file's class
    // docstring and Keputusan Desain, issue
    // open-synergy/ssi-attendance-machine#31.
    tour.register(
        "ssi_attendance_machine_attendance_machine_import_ignore_all_errors",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openAttendanceMachineImportMenuSteps(),
            openImportByMachineSteps("TOUR AMI IGNORE ALL MACHINE"),
            [
                // ── Flow 3 — Import Data tab: click Ignore All Errors
                {
                    content: "Open the Import Data tab",
                    trigger: ".o_notebook .nav-link:contains(Import Data)",
                },
                {
                    content: "Click Ignore All Errors",
                    trigger: ".o_form_view button:contains(Ignore All Errors)",
                },
                {
                    // 14.0: trigger inside an open modal is scoped to it --
                    // never prefixed with ".modal".
                    content: "Ignore All Errors wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Flow 4 — Fill in the Reason
                {
                    content: "Fill in the Reason",
                    trigger: "textarea.o_field_widget[name='reason']",
                    run: "text Tour ignore all errors reason",
                },

                // ── Flow 5 — Click Confirm
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // ── Post-Condition — wizard closes, form is re-rendered
                {
                    content: "The form is displayed again",
                    trigger: "body:not(:has(.modal)) .o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );
});

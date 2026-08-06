odoo.define("ssi_attendance_machine.attendance_machine_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Configuration >
    // Attendance Machines. The first "Configuration" (level 2) is a
    // clickable section. The second "Configuration" (level 3,
    // menu_attendance_machine_configuration) has no action of its own and
    // has children of its own (the leaf model menus), so it is rendered as
    // a non-clickable dropdown header without [data-menu-xmlid] -- its
    // children are flattened into the level-2 section's dropdown instead.
    // There is therefore no step for it; the tour goes straight from the
    // level-2 "Configuration" section to the "Attendance Machines" leaf
    // item.
    function openAttendanceMachineMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                content: "Open the Attendance Machines menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_attendance_machine.attendance_machine_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view --
                // the app landing action is also a .o_list_view.
                content: "Attendance Machines list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Attendance Machines)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/attendance_machine/01-create.md
    //
    // Scope: Machine Model / CSV Mapping (Configuration tab) are optional
    // fields left at their empty default, same as Note -- skipped here, not
    // exercised by this tour. The Employees tab is exercised because the
    // IK documents it as the operational prerequisite for attendance file
    // import (employees must be listed with their Employee Code).
    tour.register(
        "ssi_attendance_machine_attendance_machine_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineMenuSteps(), [
            // ── Flow 2 — Click the New button
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

            // ── Flow 3 — Fill in the required fields
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-MACHINE-CREATE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },

            // ── Flow 4 — Configuration tab: Machine Model / CSV Mapping
            // (skipped; optional fields, left empty)

            // ── Flow 5 — Click Generate Code in the header
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 6 — No sequence.template is configured: a warning
            // dialog appears instead of a new code. Click OK to dismiss it.
            {
                content: "Dismiss the missing sequence.template warning",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Flow 7 — Employees tab: add one employee row
            {
                content: "Open the Employees tab",
                trigger: ".o_notebook .nav-link:contains(Employees)",
            },
            {
                content: "Add an employee line",
                trigger:
                    ".o_field_widget[name='employee_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                content: "Select the Employee",
                trigger: ".o_selected_row .o_field_widget[name='employee_id'] input",
                run: "text TOUR-MACHINE-EMP-CREATE",
            },
            {
                content: "Pick the employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-MACHINE-EMP-CREATE)",
            },
            {
                content: "Fill in the Employee Code",
                trigger: ".o_selected_row .o_field_widget[name='employee_code']",
                run: "text EMP-CREATE-001",
            },
            {
                // Commit by clicking an existing field outside the list --
                // the Name field stays rendered above the notebook
                // regardless of the active tab. Do not commit with Tab: on
                // an editable="bottom" list it opens a new empty row and
                // leaves the form dirty at teardown.
                content: "Commit the employee line",
                trigger: ".o_field_widget[name='name']",
                run: function () {
                    this.$anchor[0].click();
                },
            },

            // ── Flow 8 — Optionally fill in Note (skipped; optional field)

            // ── Flow 9 — Click Save
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
                content: "Back to the Attendance Machines list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machines)",
            },
            {
                content: "New record is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-MACHINE-CREATE)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine/02-edit.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-MACHINE-EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
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

            // ── Flow 3 — Change Name
            {
                content: "Change Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-MACHINE-EDIT-CHANGED",
            },

            // ── Flow 4 — Configuration tab: Machine Model / CSV Mapping
            // (skipped; optional fields, unchanged)

            // ── Flow 5 — Click Generate Code in the header
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 6 — No sequence.template is configured: a warning
            // dialog appears instead of a new code. Click OK to dismiss it.
            {
                content: "Dismiss the missing sequence.template warning",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Flow 7 — Employees tab: add one employee row
            {
                content: "Open the Employees tab",
                trigger: ".o_notebook .nav-link:contains(Employees)",
            },
            {
                content: "Add an employee line",
                trigger:
                    ".o_field_widget[name='employee_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                content: "Select the Employee",
                trigger: ".o_selected_row .o_field_widget[name='employee_id'] input",
                run: "text TOUR-MACHINE-EMP-EDIT",
            },
            {
                content: "Pick the employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-MACHINE-EMP-EDIT)",
            },
            {
                content: "Fill in the Employee Code",
                trigger: ".o_selected_row .o_field_widget[name='employee_code']",
                run: "text EMP-EDIT-001",
            },
            {
                content: "Commit the employee line",
                trigger: ".o_field_widget[name='name']",
                run: function () {
                    this.$anchor[0].click();
                },
            },

            // ── Flow 8 — Click Save
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

            // ── Post-Condition — record updated with the new value
            {
                content: "Back to the Attendance Machines list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machines)",
            },
            {
                content: "Updated record is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-MACHINE-EDIT-CHANGED)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine/03-delete.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineMenuSteps(), [
            // ── Flow 2 — Open the record to delete
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-MACHINE-DELETE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Flow 3 — Click Action > Delete
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // Action menu items are Owl components; match the exact
                // label so "Archive" is never picked instead.
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

            // ── Flow 5 — Click the Attendance Machines breadcrumb
            {
                content: "Click the Attendance Machines breadcrumb",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machines)",
            },

            // ── Post-Condition — record permanently removed
            {
                content: "Deleted record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-MACHINE-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine/04-deactivate.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineMenuSteps(), [
            // ── Flow 2 — Open the record to deactivate
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-MACHINE-DEACTIVATE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Flow 3 — Click the Edit button
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

            // ── Flow 4 — Toggle the Active field off
            {
                content: "Toggle Active off",
                trigger: ".o_field_widget[name='active'] input",
                run: "click",
            },

            // ── Flow 5 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — Archived ribbon is displayed
            {
                content: "Archived ribbon is displayed",
                trigger: ".o_form_view .ribbon:visible:contains(Archived)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine/05-activate.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineMenuSteps(), [
            // ── Flow 2 — Enable the Archived filter in the search bar
            {
                content: "Open the Filters menu",
                trigger: ".o_search_options .o_filter_menu button",
                run: function () {
                    // Owl dropdowns in 14.0 are not always opened by a
                    // synthetic click -- use a native click instead.
                    this.$anchor[0].click();
                },
            },
            {
                content: "Enable the Archived filter",
                trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Archived record is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-MACHINE-ACTIVATE)",
                extra_trigger: ".o_list_view",
            },

            // ── Flow 3 — Open the archived record to reactivate
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-MACHINE-ACTIVATE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Flow 4 — Click the Edit button
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

            // ── Flow 5 — Toggle the Active field on
            {
                content: "Toggle Active on",
                trigger: ".o_field_widget[name='active'] input",
                run: "click",
            },

            // ── Flow 6 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — Archived ribbon is no longer displayed
            {
                content: "Archived ribbon is no longer displayed",
                trigger: ".o_form_view:not(:has(.ribbon:visible:contains(Archived)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine/06-reset-code.md
    //
    // Note: unlike a form-header object button, the `confirm=` attribute on
    // a <tree><header> button is not processed anywhere in the 14.0 web
    // client list view stack (only form_controller.js and
    // kanban_controller.js read `attrs.confirm`), so clicking "Reset code"
    // here runs the action immediately without a confirmation dialog. Same
    // finding already documented for the sibling models of this module
    // (see attendance_machine_model_tour.js / attendance_machine_csv_mapping_tour.js
    // and issue open-synergy/ssi-attendance-machine#24).
    tour.register(
        "ssi_attendance_machine_attendance_machine_reset_code",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineMenuSteps(), [
            // ── Flow 2 — Select the record whose code will be reset
            {
                content: "Wait for the list data to finish loading",
                trigger: ".o_data_row:contains(TOUR-MACHINE-RESET-CODE)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Select the record to reset",
                trigger:
                    ".o_data_row:contains(TOUR-MACHINE-RESET-CODE) " +
                    ".o_list_record_selector input",
                run: "click",
            },

            // ── Flow 3 — Click the Reset code button above the list. The
            // action runs immediately: unlike form-header object buttons,
            // the `confirm=` attribute on a <tree><header> button is not
            // honored by the 14.0 web client, so no confirmation dialog
            // is shown here.
            {
                content: "Click the Reset code button",
                trigger: "button[name='action_reset_code']:visible",
            },

            // ── Post-Condition — the list is refreshed and the selection
            // is cleared: the Reset code button (only rendered while a
            // record is selected) no longer appears above the list, and
            // no dialog was ever opened.
            {
                content: "Reset code button is no longer displayed",
                trigger: ".o_list_buttons:not(:has(button[name='action_reset_code']))",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});

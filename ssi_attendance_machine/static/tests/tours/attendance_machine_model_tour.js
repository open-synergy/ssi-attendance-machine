odoo.define("ssi_attendance_machine.attendance_machine_model_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Configuration >
    // Attendance Machine Models. The first "Configuration" (level 2) is a
    // clickable section. The second "Configuration" (level 3,
    // menu_attendance_machine_configuration) has no action of its own and
    // has children of its own (the leaf model menus), so it is rendered as
    // a non-clickable dropdown header without [data-menu-xmlid] — its
    // children are flattened into the level-2 section's dropdown instead.
    // There is therefore no step for it; the tour goes straight from the
    // level-2 "Configuration" section to the "Attendance Machine Models"
    // leaf item.
    function openAttendanceMachineModelMenuSteps() {
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
                content: "Open the Attendance Machine Models menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_attendance_machine.attendance_machine_model_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Attendance Machine Models list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Attendance Machine Models)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/attendance_machine_model/01-create.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_model_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineModelMenuSteps(), [
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
                run: "text TOUR-MODEL-CREATE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },

            // ── Flow 4 — Click Generate Code in the header
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 5 — No sequence.template is configured: a warning
            // dialog appears instead of a new code. Click OK to dismiss it.
            {
                content: "Dismiss the missing sequence.template warning",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Flow 6 — Optionally fill in Note (skipped; optional field)

            // ── Flow 7 — Click Save
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
                content: "Back to the Attendance Machine Models list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machine Models)",
            },
            {
                content: "New record is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-MODEL-CREATE)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine_model/02-edit.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_model_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineModelMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-MODEL-EDIT) .o_data_cell:first",
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
                run: "text TOUR-MODEL-EDIT-CHANGED",
            },

            // ── Flow 4 — Click Generate Code in the header
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 5 — No sequence.template is configured: a warning
            // dialog appears instead of a new code. Click OK to dismiss it.
            {
                content: "Dismiss the missing sequence.template warning",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Flow 6 — Click Save
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
                content: "Back to the Attendance Machine Models list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machine Models)",
            },
            {
                content: "Updated record is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-MODEL-EDIT-CHANGED)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine_model/03-delete.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_model_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineModelMenuSteps(), [
            // ── Flow 2 — Open the record to delete
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-MODEL-DELETE) .o_data_cell:first",
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

            // ── Flow 5 — Click the Attendance Machine Models breadcrumb
            {
                content: "Click the Attendance Machine Models breadcrumb",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Machine Models)",
            },

            // ── Post-Condition — record permanently removed
            {
                content: "Deleted record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-MODEL-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/attendance_machine_model/04-deactivate.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_model_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineModelMenuSteps(), [
            // ── Flow 2 — Open the record to deactivate
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-MODEL-DEACTIVATE) .o_data_cell:first",
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

    // IK: docs/attendance_machine_model/05-activate.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_model_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineModelMenuSteps(), [
            // ── Flow 2 — Enable the Archived filter in the search bar
            {
                content: "Open the Filters menu",
                trigger: ".o_search_options .o_filter_menu button",
                run: function () {
                    // Owl dropdowns in 14.0 are not always opened by a
                    // synthetic click — use a native click instead.
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
                trigger: ".o_data_row:contains(TOUR-MODEL-ACTIVATE)",
                extra_trigger: ".o_list_view",
            },

            // ── Flow 3 — Open the archived record to reactivate
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-MODEL-ACTIVATE) .o_data_cell:first",
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

    // IK: docs/attendance_machine_model/06-reset-code.md
    tour.register(
        "ssi_attendance_machine_attendance_machine_model_reset_code",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceMachineModelMenuSteps(), [
            // ── Flow 2 — Select the record whose code will be reset
            {
                content: "Wait for the list data to finish loading",
                trigger: ".o_data_row:contains(TOUR-MODEL-RESET-CODE)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Select the record to reset",
                trigger:
                    ".o_data_row:contains(TOUR-MODEL-RESET-CODE) " +
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

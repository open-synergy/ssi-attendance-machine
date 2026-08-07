// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_attendance_machine_documenso_signing.attendance_machine_import_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/attendance_machine_import/05-approve.md (E2a delta -- Modified
        // Flow)
        // Navigation (open menu -> open record) is retraced from the base IK
        // ssi_attendance_machine/docs/attendance_machine_import/05-approve.md Flow
        // steps 1-2 -- see skill odoo-development-ui-test,
        // scope-and-boundaries.md §3 ("E2a -- telusur-ulang aksi itu dari base
        // sampai titik ubah"). The delta assertion, anchored at base Flow step 2
        // (open the record to approve), verifies the Signature Requests tab
        // injected because `_documenso_signing_create_page = True`, then stops --
        // base Flow steps 3-4 (Approve / OK) and the resulting Queue Done status
        // are NOT exercised here, since whether the Approve button is even
        // visible depends on whether the active Approval Template has a
        // Documenso Signing Template configured, and this tour's fixture leaves
        // that unconfigured. The final signed/rejected outcome is driven by the
        // external Documenso connector and is out of scope for a tour
        // (Keputusan Desain, issue open-synergy/ssi-attendance-machine#30).
        tour.register(
            "ssi_attendance_machine_documenso_signing_attendance_machine_import_approve",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Base Flow 1 — Open the Human Resource > Timesheets >
                // Attendance Machine Imports menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Timesheets menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_timesheet.timesheet_menu"]',
                },
                {
                    content: "Open the Attendance Machine Imports menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_attendance_machine.attendance_machine_import_menu"]',
                },
                {
                    // Gate: wait for the TARGET action to be mounted, not just any
                    // list view (the app may land on a stale list first).
                    content: "Attendance Machine Imports list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Attendance Machine Imports)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Base Flow 2 — Open the record to approve.
                // `_create_sequence_state = "done"` means the document number
                // (`name`) is still "/" at this state, so the row is located by
                // the Machine column instead, which is unique and stable.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(Tour AMI Documenso Machine) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Delta assertion (anchor: base Flow step 2) — the Signature
                // Requests tab is always present once this module is installed,
                // regardless of whether Documenso signing is actually used for
                // the current approval.
                {
                    content: "Open the Signature Requests tab",
                    trigger: ".o_notebook .nav-link:contains(Signature Requests)",
                },
                {
                    // Anchored on the group label rather than the (currently
                    // empty) `approval_signature_request_id` many2one widget
                    // itself -- a many2one rendered with no value has no text
                    // node inside its link, so it collapses to a zero-size box
                    // and jQuery's `:visible` (offsetWidth/offsetHeight) never
                    // matches it, hanging the tour until timeout. The group
                    // label always has text, so it is a stable proxy for "the
                    // Approval Signing Request group is rendered".
                    content:
                        "Signature Requests tab shows the Approval Signing " +
                        "Request group",
                    trigger:
                        ".o_horizontal_separator:contains(Approval Signing Request)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action. The tour stops here -- it does not click
                        // Approve, does not assert a final state, and never
                        // calls the external Documenso service.
                    },
                },
            ]
        );
    }
);

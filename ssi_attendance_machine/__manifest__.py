# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Attendance Machine",
    "version": "14.0.2.12.3",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "external_dependencies": {"python": ["xlrd"]},
    "depends": [
        "web_tour",
        "ssi_web_widget_json",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_queue_done_mixin",
        "ssi_transaction_queue_cancel_mixin",
        "ssi_timesheet_attendance",
        "ssi_hr",
        "queue_job_batch",
        "base_automation",
    ],
    "data": [
        # Security - module categories (transactional)
        "security/ir_module_category/attendance_machine_import.xml",
        # Security - groups
        "security/res_groups/attendance_machine_model.xml",
        "security/res_groups/attendance_machine_csv_mapping.xml",
        "security/res_groups/attendance_machine.xml",
        "security/res_groups/attendance_machine_import.xml",
        # Security - access
        "security/ir_model_access/attendance_machine_model.xml",
        "security/ir_model_access/attendance_machine_csv_mapping.xml",
        "security/ir_model_access/attendance_machine.xml",
        "security/ir_model_access/attendance_machine_employee.xml",
        "security/ir_model_access/attendance_machine_import.xml",
        "security/ir_model_access/attendance_machine_import_data.xml",
        "security/ir_model_access/attendance_machine_import_ignore.xml",
        "security/ir_model_access/attendance_machine_import_data_ignore.xml",
        "security/ir_model_access/attendance_machine_import_data_edit.xml",
        # Security - rules
        "security/ir_rule/attendance_machine_import.xml",
        # Sequences
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/approval_template_data.xml",
        "data/policy_template_data.xml",
        # Queue automation
        "data/ir_actions_server_data.xml",
        "data/base_automation_data.xml",
        # Menu
        "menu.xml",
        # Wizards
        "wizards/attendance_machine_import_ignore_views.xml",
        "wizards/attendance_machine_import_data_ignore_views.xml",
        "wizards/attendance_machine_import_data_edit_views.xml",
        # Views
        "views/attendance_machine_model_views.xml",
        "views/attendance_machine_csv_mapping_views.xml",
        "views/attendance_machine_views.xml",
        "views/attendance_machine_import_views.xml",
        "views/assets.xml",
    ],
    "demo": [
        "demo/attendance_machine_model_demo.xml",
        "demo/attendance_machine_csv_mapping_demo.xml",
        "demo/attendance_machine_demo.xml",
    ],
    "images": [],
}

# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Attendance Machine + Operating Unit",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_attendance_machine",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/attendance_machine_import.xml",
        "security/ir_rule/attendance_machine_import.xml",
        "views/attendance_machine_import_views.xml",
    ],
}

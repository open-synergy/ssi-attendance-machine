# Create Attendance Machine Import

> **Module:** ssi_attendance_machine_operating_unit
>
> **Extends:** ssi_attendance_machine — model `attendance_machine_import`, aksi
> `01-create`

## Additional Pre-Condition

- **Module:** `ssi_attendance_machine_operating_unit` is installed.
- **Access:** User is in group _Multiple Operating Unit_
  (`operating_unit.group_multi_operating_unit`) to see and use the Operating Unit field
  described below. Users outside this group never see the field.

## Additional Fields

When this module is installed, the create form gains one field, visible only to users in
the **Multiple Operating Unit** group (`operating_unit.group_multi_operating_unit`) — on
the form, on the tree (optional column, hidden by default), and in the search panel:

- **Operating Unit**: the operating unit that owns this import document. Not required.
  Defaults to the current user's default operating unit (falls back to an operating unit
  assigned to the user, if any). Change if needed.

This field also changes what happens when **Import Data** is processed and attendance
records are created (see the base IK's `09-finish`): each resulting
`hr.timesheet_attendance` record inherits the operating unit of the **employee** the
attendance belongs to — not this document's Operating Unit, and not any default
operating unit. This is an outcome observed at the end of the import, not a new UI step,
so it does not create a delta for `09-finish`.

## Modified — Record Visibility

- The **Attendance Machine Imports** list is filtered by operating unit (record rule). A
  user only sees import documents whose Operating Unit is one of the operating units
  assigned to them. This is not a Flow step.

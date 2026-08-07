# Restart Approval Process — Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** user in group _Attendance Machine Import — Validator_
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `restart_approval_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group _Attendance Machine Import — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Open the record whose approval process will be restarted.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- All existing approval records for this document are removed.
- A new approval process is started from the approval template's first level, based on
  the active `approval.template` that matches this record.

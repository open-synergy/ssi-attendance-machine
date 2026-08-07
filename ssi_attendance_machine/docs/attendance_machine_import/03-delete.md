# Delete Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** user in group _Attendance Machine Import — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _Attendance Machine Import — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system, along with their import
  data lines.

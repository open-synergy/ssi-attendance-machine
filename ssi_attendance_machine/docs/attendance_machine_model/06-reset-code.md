# Reset Code — Attendance Machine Model

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_model`
>
> **Menu:** Human Resource > Configuration > Configuration > Attendance Machine Models
>
> **Actor:** user in group _Attendance Machine Model_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** One or more records exist.
- **Access:** User is in group _Attendance Machine Model_.

## Flow

1. Open the **Human Resource > Configuration > Configuration > Attendance Machine
   Models** menu.
2. Select one or more records whose code will be reset (check the checkbox).
3. Click the **Reset code** button that appears above the list.
4. Click **OK** on the confirmation dialog ("Reset code. Are you sure?").

## Post-Condition

- **Code** of the selected records returns to **/**.
- The records become eligible for automatic code assignment the next time **Generate
  Code** is used (see `01-create` and `02-edit`), or the field can be filled in
  manually.

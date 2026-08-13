# Activate Attendance Machine

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine`
>
> **Menu:** Human Resource > Configuration > Attendance Machine > Attendance Machines
>
> **Actor:** user in group _Attendance Machine_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Attendance Machine_.

## Flow

1. Open the **Human Resource > Configuration > Attendance Machine > Attendance
   Machines** menu.
2. Enable the **Archived** filter in the search bar.
3. Open the archived record to reactivate.
4. Click the **Edit** button.
5. Toggle the **Active** field on.
6. Click **Save**.

## Post-Condition

- The record is restored and appears again in the default list view.
- The **Archived** ribbon no longer appears on the form.
- The record can be selected again in new transactions.

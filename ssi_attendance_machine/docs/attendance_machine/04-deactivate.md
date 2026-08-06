# Deactivate Attendance Machine

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine`
>
> **Menu:** Human Resource > Configuration > Configuration > Attendance Machines
>
> **Actor:** user in group _Attendance Machine_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Attendance Machine_.

## Flow

1. Open the **Human Resource > Configuration > Configuration > Attendance Machines**
   menu.
2. Open the record to deactivate.
3. Click the **Edit** button.
4. Toggle the **Active** field off.
5. Click **Save**.

## Post-Condition

- The record is archived; an **Archived** ribbon appears on the form.
- The record no longer appears in the default list view.
- The deactivated record cannot be selected in new transactions.
- Transactions that already use this record can still be viewed.

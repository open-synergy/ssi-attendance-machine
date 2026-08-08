# Ignore All Errors — Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** user in group _Attendance Machine Import — User_ (or above)
>
> **Requires:** `05-approve`
>
> **Inline Actions:** `action_confirm` (Confirm, on the Ignore All Errors wizard)

## Pre-Condition

- **Record:** Status is **Queue To Done**. The button is only visible in this status.
- **Record:** At least one **Import Data** row is in status **Error** — the wizard has
  nothing to write when **# Error** is zero.
- **Access:** User is in group _Attendance Machine Import — User_ (or above) — write
  access is required and the button is not guarded by a dedicated policy field.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Open the record whose error rows will be bulk-ignored.
3. On the **Import Data** tab, click the **Ignore All Errors** button.
4. In the wizard that appears, fill in the **Reason**.
5. Click the **Confirm** button.

## Post-Condition

- Every **Import Data** row that was in status **Error** changes to status **Ignored**,
  with the same **Reason** recorded as its **Ignore Reason**. The **# Error** counter
  drops to zero and **# Ignored** increases by the same amount.
- If ignoring the last unresolved row leaves no row in **Draft** or **Error**, the
  document immediately moves to **Done** as a side effect — see `09-finish`. Otherwise
  it remains **Queue To Done**.

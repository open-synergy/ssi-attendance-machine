# Approve Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** approver registered on the approval level that is currently pending
>
> **State:** `confirm` → `confirm` (see Post-Condition for the automatic transition on
> the last approval)
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The approval template validates levels sequentially, so only the first
  unapproved level is pending.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels after this approval, status remains
  **Waiting for Approval** and the next level becomes pending.
- If this was the last pending approval level, status automatically changes to **Queue
  Done** via `action_queue_done` (`_after_approved_method`) — no separate button click
  is required. Queue Done phase processing (the queue jobs that convert import data
  lines into attendance records) is documented in a separate item.

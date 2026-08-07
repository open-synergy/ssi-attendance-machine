# Cancel Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** user in group _Attendance Machine Import — Validator_
>
> **State:** `draft` | `confirm` | `done` → `queue_cancel` → `cancel`
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_requeue_cancel` (Requeue),
> `action_recompute_queue_cancel_result` (Recompute Queue Cancel Result)

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group.
- **Access:** User is in group _Attendance Machine Import — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Open the record to cancel.
3. Click the **Cancel** button. This opens the **Select Cancel Reason** wizard.
4. In the wizard, select the **Reason**.
5. Click the **Confirm** button.
6. Click **OK** on the confirmation dialog.
7. While the document is in status **Queue To Cancel**, if needed, open the **Queue
   Processing** tab: click the **Requeue** button to re-run every cancellation queue job
   that is not yet **Done**, or click the **Recompute Queue Cancel Result** button to
   force an immediate check instead of waiting for the automation described in
   Post-Condition.
8. Click **OK** on the confirmation dialog (only when the **Recompute Queue Cancel
   Result** button was used).

## Post-Condition

- Status immediately changes to **Queue To Cancel** (`queue_cancel`) via
  `action_queue_cancel` (the wizard's `_method_to_run_from_wizard`). The selected Reason
  is stored on the document, and a queue job is started for every **Import Data** row
  that already has a linked attendance record, to remove that `hr.timesheet_attendance`
  record.
- Once every cancellation queue job finishes and **To Cancel Queue Job Batch State**
  (`cancel_queue_job_batch_state`) becomes **Finished**, a `base.automation` calls
  `action_recompute_queue_cancel_result` on its own, which finally changes status to
  **Cancelled**.
- Once status reaches **Cancelled**, the selected Cancellation Reason is displayed next
  to the document's title.

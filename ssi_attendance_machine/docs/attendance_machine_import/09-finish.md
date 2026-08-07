# Finish Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** system-triggered by `base.automation`; user in group _Attendance Machine
> Import — User_ (or above) drives it manually with the actions below
>
> **State:** `queue_done` → `done`
>
> **Requires:** `05-approve`
>
> **Inline Actions:** `action_requeue_done` (Requeue),
> `action_recompute_queue_done_result` (Recompute Queue Done Result),
> `action_retry_all_error` (Retry All Errors), `action_retry` (Retry, on an Import Data
> row), `action_open_ignore_wizard` (Ignore, on an Import Data row),
> `action_open_edit_data_wizard` (Edit Data, on an Import Data row)

## Pre-Condition

- **Record:** Status is **Queue To Done**. The document reaches this status
  automatically once the last approval level is approved (see `05-approve`) — there is
  no button that puts a document into this status directly.
- **Record:** For the document to reach **Done**, every **Import Data** row must be
  **Done** or **Ignored** — none may remain **Draft** or **Error**.
- **Config:** A `base.automation` on this model recomputes the queue result
  automatically, on every write, whenever **To Done Queue Job Batch State**
  (`done_queue_job_batch_state`) becomes **Finished** — so the document frequently
  reaches **Done** on its own, without any button on this page being clicked.
- **Access:** User is in group _Attendance Machine Import — User_ (or above) to use
  **Requeue**, **Recompute Queue Done Result**, **Retry All Errors**, and the row-level
  **Retry**, **Ignore**, and **Edit Data** buttons — all of them require write access
  and none is guarded by a dedicated policy field.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Open the record. After the last approval level is approved, it is already in status
   **Queue To Done**: a queue job was started for every **Import Data** row to convert
   it into an `hr.timesheet_attendance` record.
3. On the **Import Data** tab, check the **# Data**, **# Done**, **# Error**, and **#
   Ignored** counters to see how many rows still need attention.
4. If **# Error** is greater than zero, resolve each error row. For a single row:
   - Click the row's **Retry** button to re-run that row immediately (also usable on
     rows still **Draft**). On success the row becomes **Done**; on failure it stays
     **Error** with an updated **Error Message**.
   - Click the row's **Edit Data** button to open a wizard and correct the row's raw
     JSON **Data**, then click **Confirm**. This only returns the row to **Draft** with
     the corrected data — it does **not** retry the row by itself, so follow up with
     **Retry** (or **Retry All Errors**).
   - Click the row's **Ignore** button to open a wizard, fill in the **Reason**, and
     click **Confirm** to exclude that single row from the import without creating an
     attendance record.
   - Click the header **Retry All Errors** button to retry every **Error** row at once —
     a shortcut equivalent to clicking **Retry** on each of them individually.
   - Alternatively, click the header **Ignore All Errors** button to exclude every
     remaining **Error** row with one shared reason — see `15-ignore-all-errors`.
5. If a row's queue job appears stuck (its **Job Batch** is not progressing), open the
   **Queue Processing** tab and click the **Requeue** button to re-run every queue job
   that is not yet **Done**. This is the only way to force a stuck job batch to run
   again.
6. Still on the **Queue Processing** tab, optionally click the **Recompute Queue Done
   Result** button to force an immediate check instead of waiting for the automation
   described in Post-Condition.
7. Click **OK** on the confirmation dialog (only when the **Recompute Queue Done
   Result** button was used).

## Post-Condition

- Resolving the last **Draft**/**Error** row — whether by **Retry**, **Ignore**, **Retry
  All Errors**, or the wizard behind **Ignore All Errors** — immediately re-checks the
  document and moves it to **Done** if the **To Done Queue Job Batch** has already
  finished.
- Otherwise, once every queued job finishes and **To Done Queue Job Batch State**
  becomes **Finished**, the `base.automation` calls `action_recompute_queue_done_result`
  on its own, which moves the document to **Done** without further user action.
- On **Done**, the document receives its sequence number
  (`_create_sequence_state = "done"` — see `13-reset-number` for the manual reset path).

## Related Views

- The **Attendances** smart button (`action_open_attendances`) in the button box opens
  the list of `hr.timesheet_attendance` records created by this import. It only returns
  an `act_window` and writes no field, so it is pure navigation with no Flow step of its
  own.

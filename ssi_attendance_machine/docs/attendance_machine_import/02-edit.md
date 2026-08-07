# Edit Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** user in group _Attendance Machine Import — User_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_load_data` (Load Data)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Attendance Machine Import — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Find and open the record to edit.
3. Change **Date**, **Machine**, or **Attendance File** as needed.
4. On the **Import Data** tab, click **Load Data** to discard the existing import data
   lines and re-read the current **Attendance File** — for example after replacing the
   file or changing **Machine** (which changes the CSV mapping used to parse it). There
   is no manual alternative. Skipping this step after replacing the file leaves the
   **Import Data** tab showing lines generated from the previous file.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- If **Load Data** was clicked, the **Import Data** tab is replaced with one line per
  row of the current **Attendance File**, and **# Data** reflects the new count.

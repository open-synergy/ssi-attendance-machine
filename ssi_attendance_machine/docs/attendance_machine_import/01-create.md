# Create Attendance Machine Import

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_import`
>
> **Menu:** Human Resource > Timesheets > Attendance Machine Imports
>
> **Actor:** user in group _Attendance Machine Import — User_
>
> **State:** `—` → `draft`
>
> **Inline Actions:** `action_load_data` (Load Data)

## Pre-Condition

- **Data:** An attendance machine record exists, with its CSV mapping and employee
  roster already configured (see `attendance_machine/01-create`).
- **Access:** User is in group _Attendance Machine Import — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Machine Imports** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date** _(required)_: Automatically filled with today's date. Change if needed.
   - **Machine** _(required)_: Select the attendance machine this import belongs to.
   - **Attendance File**: Upload the attendance data file exported from the machine
     (CSV/delimited text, or Excel, depending on the machine's CSV mapping
     configuration).
4. On the **Import Data** tab, click **Load Data** to delete any existing data lines,
   read the uploaded **Attendance File**, and create one import data line per file row.
   There is no manual alternative — this is the only way to populate the tab. Without
   clicking it, the **Import Data** tab stays empty and there is nothing for approval to
   hand off to queue processing.
5. Click **Save**.

## Post-Condition

- A new attendance machine import record is created in **Draft** status.
- If **Load Data** was clicked, the **Import Data** tab lists one line per row of the
  uploaded file, and **# Data** reflects the number of lines created.

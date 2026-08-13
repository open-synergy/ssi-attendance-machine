# Create Attendance Machine

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine`
>
> **Menu:** Human Resource > Configuration > Attendance Machine > Attendance Machines
>
> **Actor:** user in group _Attendance Machine_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** An attendance machine model record exists (see
  `attendance_machine_model/01-create`) if **Machine Model** will be filled in.
- **Data:** A CSV mapping record exists (see `attendance_machine_csv_mapping/01-create`)
  if **CSV Mapping** will be filled in.
- **Access:** User is in group _Attendance Machine_.

## Flow

1. Open the **Human Resource > Configuration > Attendance Machine > Attendance
   Machines** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label identifying this attendance machine (for
     example "HQ Main Entrance").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment via **Generate Code**.
4. On the **Configuration** tab, optionally fill in:
   - **Machine Model**: Select the brand/model of this device.
   - **CSV Mapping**: Select the CSV mapping template used to parse attendance files
     exported from this machine.
5. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**.
6. No `sequence.template` is currently configured for **Attendance Machine**, so a
   warning dialog appears instead of a new code being assigned. Click **OK** to dismiss
   it. **Code** remains **/**.
7. On the **Employees** tab, add one row per employee registered on this machine:

   - **Employee** _(required)_: Select the employee record.
   - **Employee Code**: Enter the identifier used for this employee inside the
     attendance machine's exported file.
   - **Sequence**: Leave the default display order, or reorder rows by dragging the
     handle.

   > This tab is the prerequisite that makes attendance file import work: when an
   > attendance import matches file rows to employees, it does so by **Employee Code**.
   > An employee whose code is missing here — or a machine with no employees at all —
   > causes every file row for that employee to end up as an **Error** during import,
   > with no other explanation shown to the user.

8. Optionally fill in **Note**.
9. Click **Save**.

## Post-Condition

- A new attendance machine record is created, active by default.
- The record is displayed in the list view.
- If no `sequence.template` was configured, **Code** is still **/**; the record can be
  found again later by **Name** and its code assigned once a `sequence.template` is set
  up, or generated afterwards (see `02-edit`).

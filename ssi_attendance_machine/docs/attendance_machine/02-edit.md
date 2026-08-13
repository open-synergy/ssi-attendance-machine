# Edit Attendance Machine

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine`
>
> **Menu:** Human Resource > Configuration > Attendance Machine > Attendance Machines
>
> **Actor:** user in group _Attendance Machine_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Machine_.

## Flow

1. Open the **Human Resource > Configuration > Attendance Machine > Attendance
   Machines** menu.
2. Find and open the record to edit.
3. Change **Name**, **Code**, **Active**, or **Note** as needed.
4. On the **Configuration** tab, change **Machine Model** or **CSV Mapping** as needed.
5. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model — for example after resetting
   **Code** back to **/** (see `06-reset-code`). Only applies while **Code** is **/**.
6. No `sequence.template` is currently configured for **Attendance Machine**, so a
   warning dialog appears instead of a new code being assigned. Click **OK** to dismiss
   it. **Code** is left unchanged.
7. On the **Employees** tab, add, edit, or remove rows as needed:

   - **Employee** _(required)_: Select the employee record.
   - **Employee Code**: Enter the identifier used for this employee inside the
     attendance machine's exported file.
   - **Sequence**: Reorder rows by dragging the handle if needed.

   > Keep this tab in sync with the machine's actual employee roster: attendance file
   > import matches file rows to employees by **Employee Code**, so an employee whose
   > code is missing or wrong here causes that employee's file rows to end up as an
   > **Error** during import, with no other explanation shown to the user.

8. Click **Save**.

## Post-Condition

- The record is updated with the new values.

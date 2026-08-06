# Create Attendance Machine CSV Mapping

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_csv_mapping`
>
> **Menu:** Human Resource > Configuration > Configuration > CSV Mappings
>
> **Actor:** user in group _Attendance Machine CSV Mapping_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Machine CSV Mapping_.

## Flow

1. Open the **Human Resource > Configuration > Configuration > CSV Mappings** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label describing this CSV mapping (for example
     "Standard CSV Import").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment via **Generate Code**.
4. On the **File Format** tab:

   - **File Format** _(required)_: Keep the default **CSV / Delimited Text**. The
     remaining steps on this tab describe the CSV / Delimited Text path — see the
     conditional note below for **Excel**.
   - Review the remaining parsing options as needed: **Encoding**, **Delimiter**, **Text
     Qualifier**, **No Header Line**, **Skip Empty Lines**, **Row Offset**, **Column
     Offset**.

   > **If File Format is Excel:** **Sheet Index** becomes enabled — enter the 0-based
   > worksheet index to read. **Encoding**, **Delimiter**, and **Text Qualifier** become
   > disabled and are ignored.

5. On the **Column Mapping** tab:

   - **Row Mode** _(required)_: Keep the default **Single Row**. The remaining steps
     describe the Single Row path — see the conditional note below for **Separate
     Rows**.
   - **Datetime Mode** _(required)_: Keep the default **Combined**. The remaining steps
     describe the Combined path — see the conditional note below for **Separate**.
   - **Employee Column** _(required)_: Enter the column name (or 0-based index if **No
     Header Line** is checked) containing the employee code that will be matched against
     the machine's employee list.
   - **Check-in Column**: Enter the column name/index for the combined check-in
     datetime.
   - **Check-out Column**: Enter the column name/index for the combined check-out
     datetime.

   > **If Row Mode is Separate Rows:** the **Check-in Column** / **Check-out Column**
   > pair is replaced by **Row Type Column** (the column that flags whether a row is a
   > check-in or check-out record), **Sign-in Value** (the value in **Row Type Column**
   > that identifies a check-in row), and **Sign-out Value** (the value that identifies
   > a check-out row).
   >
   > **If Datetime Mode is Separate:** each combined datetime column is replaced by a
   > date/time column pair — **Check-in Date Column** + **Check-in Time Column**, and
   > **Check-out Date Column** + **Check-out Time Column** (or, in Separate Rows mode, a
   > single **Date Column** + **Time Column** pair instead of **Datetime Column**).

6. Optionally fill in **Exclude Column** and **Exclude Values** to discard
   junk/duplicate rows before processing (for example a machine exception/validity
   column). Both fields must be filled in together — leaving either one empty disables
   this feature.
7. Optionally adjust **Datetime Format**, **Date Format**, or **Time Format** if the
   file uses a non-default format string.
8. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**.
9. No `sequence.template` is currently configured for **Attendance Machine CSV
   Mapping**, so a warning dialog appears instead of a new code being assigned. Click
   **OK** to dismiss it. **Code** remains **/**.
10. Optionally fill in **Note**.
11. Click **Save**.

## Post-Condition

- A new attendance machine CSV mapping record is created, active by default.
- The record is displayed in the list view.
- If no `sequence.template` was configured, **Code** is still **/**; the record can be
  found again later by **Name** and its code assigned once a `sequence.template` is set
  up, or generated afterwards (see `02-edit`).

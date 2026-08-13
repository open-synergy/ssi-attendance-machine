# Edit Attendance Machine CSV Mapping

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_csv_mapping`
>
> **Menu:** Human Resource > Configuration > Attendance Machine > Attendance Machine CSV
> Mappings
>
> **Actor:** user in group _Attendance Machine CSV Mapping_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Machine CSV Mapping_.

## Flow

1. Open the **Human Resource > Configuration > Attendance Machine > Attendance Machine
   CSV Mappings** menu.
2. Find and open the record to edit.
3. Change **Name**, **Code**, **Active**, **Note**, or any of the CSV parsing / column
   mapping fields on the **File Format** and **Column Mapping** tabs as needed.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model — for example after resetting
   **Code** back to **/** (see `06-reset-code`). Only applies while **Code** is **/**.
5. No `sequence.template` is currently configured for **Attendance Machine CSV
   Mapping**, so a warning dialog appears instead of a new code being assigned. Click
   **OK** to dismiss it. **Code** is left unchanged.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.

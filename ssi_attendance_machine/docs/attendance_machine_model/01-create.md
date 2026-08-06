# Create Attendance Machine Model

> **Module:** ssi_attendance_machine
>
> **Model:** `attendance_machine_model`
>
> **Menu:** Human Resource > Configuration > Configuration > Attendance Machine Models
>
> **Actor:** user in group _Attendance Machine Model_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Machine Model_.

## Flow

1. Open the **Human Resource > Configuration > Configuration > Attendance Machine
   Models** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label describing the attendance machine
     brand/model (for example "ZKTeco K40").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment via **Generate Code**.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**.
5. No `sequence.template` is currently configured for **Attendance Machine Model**, so a
   warning dialog appears instead of a new code being assigned. Click **OK** to dismiss
   it. **Code** remains **/**.
6. Optionally fill in **Note**.
7. Click **Save**.

## Post-Condition

- A new attendance machine model record is created, active by default.
- The record is displayed in the list view.
- If no `sequence.template` was configured, **Code** is still **/**; the record can be
  found again later by **Name** and its code assigned once a `sequence.template` is set
  up, or generated afterwards (see `02-edit`).

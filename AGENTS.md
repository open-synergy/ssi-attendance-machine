# Agent Instructions — ssi-attendance-machine

This file is intended for **AI assistants** (GitHub Copilot, Claude, Cursor, ChatGPT,
and similar tools) working inside this repository.

This repository provides Odoo modules to manage attendance machine data and import
attendance data from attendance machines via CSV/Excel file import, for PT. Simetri
Sinergi Indonesia (SSI) / OpenSynergy Indonesia, targeting Odoo 14.0.

---

## Modules in This Repository

| Module                                     | Description                                        |
| ------------------------------------------ | -------------------------------------------------- |
| `ssi_attendance_machine`                   | Attendance Machine                                 |
| `ssi_attendance_machine_documenso_signing` | Attendance Machine - Documenso Signing Integration |
| `ssi_attendance_machine_operating_unit`    | Attendance Machine + Operating Unit                |

---

## User Guide (Work Instructions)

Each module has a `docs/` directory containing **Work Instructions (IK)** — step-by-step
operational documentation for using the feature from the user's perspective.

### How to Answer User Questions About Feature Usage

1. Identify the feature being asked about.
2. Find the relevant Work Instruction from the index below.
3. **Read that file** before answering — do not fabricate steps from assumptions.
4. If a relevant extension module is installed (marked _additive_ below), also read its
   Work Instruction and **merge** it with the base IK.
5. Answer based on the content of the Work Instruction.

### Work Instruction Location Pattern

```
<module_name>/docs/<model_name>/<number>-<action>.md
```

---

## Work Instruction Index

### `ssi_attendance_machine` — Model: `attendance_machine`

Menu: **Human Resource > Configuration > Configuration > Attendance Machines**

| File                                                              | Action                                            |
| ----------------------------------------------------------------- | ------------------------------------------------- |
| `ssi_attendance_machine/docs/attendance_machine/01-create.md`     | Create a new attendance machine                   |
| `ssi_attendance_machine/docs/attendance_machine/02-edit.md`       | Edit an attendance machine                        |
| `ssi_attendance_machine/docs/attendance_machine/03-delete.md`     | Delete an attendance machine                      |
| `ssi_attendance_machine/docs/attendance_machine/04-deactivate.md` | Deactivate an attendance machine                  |
| `ssi_attendance_machine/docs/attendance_machine/05-activate.md`   | Activate an attendance machine                    |
| `ssi_attendance_machine/docs/attendance_machine/06-reset-code.md` | Reset the code of one or more attendance machines |

### `ssi_attendance_machine` — Model: `attendance_machine_csv_mapping`

Menu: **Human Resource > Configuration > Configuration > CSV Mappings**

| File                                                                          | Action                                     |
| ----------------------------------------------------------------------------- | ------------------------------------------ |
| `ssi_attendance_machine/docs/attendance_machine_csv_mapping/01-create.md`     | Create a new CSV mapping                   |
| `ssi_attendance_machine/docs/attendance_machine_csv_mapping/02-edit.md`       | Edit a CSV mapping                         |
| `ssi_attendance_machine/docs/attendance_machine_csv_mapping/03-delete.md`     | Delete a CSV mapping                       |
| `ssi_attendance_machine/docs/attendance_machine_csv_mapping/04-deactivate.md` | Deactivate a CSV mapping                   |
| `ssi_attendance_machine/docs/attendance_machine_csv_mapping/05-activate.md`   | Activate a CSV mapping                     |
| `ssi_attendance_machine/docs/attendance_machine_csv_mapping/06-reset-code.md` | Reset the code of one or more CSV mappings |

### `ssi_attendance_machine` — Model: `attendance_machine_model`

Menu: **Human Resource > Configuration > Configuration > Attendance Machine Models**

| File                                                                    | Action                                                  |
| ----------------------------------------------------------------------- | ------------------------------------------------------- |
| `ssi_attendance_machine/docs/attendance_machine_model/01-create.md`     | Create a new attendance machine model                   |
| `ssi_attendance_machine/docs/attendance_machine_model/02-edit.md`       | Edit an attendance machine model                        |
| `ssi_attendance_machine/docs/attendance_machine_model/03-delete.md`     | Delete an attendance machine model                      |
| `ssi_attendance_machine/docs/attendance_machine_model/04-deactivate.md` | Deactivate an attendance machine model                  |
| `ssi_attendance_machine/docs/attendance_machine_model/05-activate.md`   | Activate an attendance machine model                    |
| `ssi_attendance_machine/docs/attendance_machine_model/06-reset-code.md` | Reset the code of one or more attendance machine models |

### `ssi_attendance_machine` — Model: `attendance_machine_import`

Menu: **Human Resource > Timesheets > Attendance Machine Imports**

| File                                                                            | Action                                                                     |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `ssi_attendance_machine/docs/attendance_machine_import/01-create.md`            | Create a new attendance machine import                                     |
| `ssi_attendance_machine/docs/attendance_machine_import/02-edit.md`              | Edit an attendance machine import                                          |
| `ssi_attendance_machine/docs/attendance_machine_import/03-delete.md`            | Delete an attendance machine import                                        |
| `ssi_attendance_machine/docs/attendance_machine_import/04-confirm.md`           | Confirm an attendance machine import (submit for approval)                 |
| `ssi_attendance_machine/docs/attendance_machine_import/05-approve.md`           | Approve an attendance machine import                                       |
| `ssi_attendance_machine/docs/attendance_machine_import/06-reject.md`            | Reject an attendance machine import                                        |
| `ssi_attendance_machine/docs/attendance_machine_import/09-finish.md`            | Automatic transition to Done once every Import Data row is Done or Ignored |
| `ssi_attendance_machine/docs/attendance_machine_import/10-cancel.md`            | Cancel an attendance machine import                                        |
| `ssi_attendance_machine/docs/attendance_machine_import/12-restart.md`           | Restart a cancelled/rejected attendance machine import                     |
| `ssi_attendance_machine/docs/attendance_machine_import/13-reset-number.md`      | Reset an attendance machine import's document number                       |
| `ssi_attendance_machine/docs/attendance_machine_import/14-restart-approval.md`  | Restart an attendance machine import's approval process                    |
| `ssi_attendance_machine/docs/attendance_machine_import/15-ignore-all-errors.md` | Bulk-ignore all Error rows on an attendance machine import                 |

### `ssi_attendance_machine_documenso_signing` — Extends: `attendance_machine_import` _(additive)_

> Read together with `ssi_attendance_machine/docs/attendance_machine_import/*` — these
> files are deltas (additional effects), only relevant when
> `ssi_attendance_machine_documenso_signing` is installed.

| File                                                                                    | Action                                                                       |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `ssi_attendance_machine_documenso_signing/docs/attendance_machine_import/05-approve.md` | Additional effect when approving (Signature Requests tab, Documenso signing) |

### `ssi_attendance_machine_operating_unit` — Extends: `attendance_machine_import` _(additive)_

> Read together with `ssi_attendance_machine/docs/attendance_machine_import/*` — these
> files are deltas (additional fields), only relevant when
> `ssi_attendance_machine_operating_unit` is installed.

| File                                                                                | Action                                          |
| ----------------------------------------------------------------------------------- | ----------------------------------------------- |
| `ssi_attendance_machine_operating_unit/docs/attendance_machine_import/01-create.md` | Additional field when creating (Operating Unit) |

---

## Module Development Guidelines

For code conventions, file structure, naming, security, views, and other SSI standard
patterns, follow the SSI Odoo development guidelines.

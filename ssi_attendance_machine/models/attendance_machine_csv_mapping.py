# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AttendanceMachineCsvMapping(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Defines the template algorithm for parsing attendance CSV files.
    Supports various file formats including single-row and separate-row
    check-in/check-out, combined or separate date/time fields, and
    configurable datetime formats.
    """

    _name = "attendance_machine_csv_mapping"
    _description = "Attendance Machine CSV Mapping"
    _inherit = ["mixin.master_data"]

    # --- File format ---

    file_format = fields.Selection(
        string="File Format",
        selection=[
            ("csv", "CSV / Delimited Text"),
            ("excel", "Excel (.xls / .xlsx)"),
        ],
        required=True,
        default="csv",
        help=(
            "Format of the attendance file to be imported.\n"
            "- CSV / Delimited Text: parsed using Encoding, Delimiter and "
            "Text Qualifier below.\n"
            "- Excel: parsed by worksheet using Sheet Index below; "
            "Encoding, Delimiter and Text Qualifier are ignored."
        ),
    )
    sheet_index = fields.Integer(
        string="Sheet Index",
        default=0,
        help=(
            "0-based index of the worksheet to read when File Format = "
            "Excel. Ignored for CSV / Delimited Text files."
        ),
    )
    file_encoding = fields.Selection(
        string="Encoding",
        selection=[
            ("utf-8", "UTF-8"),
            ("utf-8-sig", "UTF-8 (with BOM)"),
            ("utf-16", "UTF-16"),
            ("utf-16-sig", "UTF-16 (with BOM)"),
            ("windows-1252", "Western (Windows-1252)"),
            ("iso-8859-1", "Western (Latin-1 / ISO 8859-1)"),
        ],
        default="utf-8",
        help="Character encoding of the attendance CSV file.",
    )
    delimiter = fields.Selection(
        string="Delimiter",
        selection=[
            ("comma", "comma (,)"),
            ("semicolon", "semicolon (;)"),
            ("tab", "tab"),
            ("pipe", "pipe (|)"),
            ("space", "space"),
        ],
        default="comma",
        help="Field delimiter used in the CSV file.",
    )
    quotechar = fields.Char(
        string="Text Qualifier",
        size=1,
        default='"',
        help="Character used to quote fields containing special characters.",
    )
    no_header = fields.Boolean(
        string="No Header Line",
        default=False,
        help=(
            "Check if the file does not contain a header row. "
            "When checked, use column index (0-based) instead of column name."
        ),
    )
    skip_empty_lines = fields.Boolean(
        string="Skip Empty Lines",
        default=True,
        help="Skip blank lines when parsing the file.",
    )
    offset_row = fields.Integer(
        string="Row Offset",
        default=0,
        help="Number of rows to skip from the top before starting to parse.",
    )
    offset_column = fields.Integer(
        string="Column Offset",
        default=0,
        help="Number of columns to skip from the left before starting to parse.",
    )

    # --- Algorithm template ---

    row_mode = fields.Selection(
        string="Row Mode",
        selection=[
            ("single", "Single Row (check-in and check-out in the same row)"),
            ("separate", "Separate Rows (check-in and check-out in different rows)"),
        ],
        required=True,
        default="single",
        help=(
            "Defines how check-in and check-out data are stored in the file.\n"
            "- Single Row: each row contains both check-in and check-out timestamps.\n"
            "- Separate Rows: check-in and check-out are recorded as separate rows."
        ),
    )
    datetime_mode = fields.Selection(
        string="Datetime Mode",
        selection=[
            ("combined", "Combined (date and time in one field)"),
            ("separate", "Separate (date and time in different fields)"),
        ],
        required=True,
        default="combined",
        help=(
            "Defines how date and time data are stored.\n"
            "- Combined: a single field holds both date and time.\n"
            "- Separate: date and time are in different columns."
        ),
    )

    # --- Employee column ---

    employee_column = fields.Char(
        string="Employee Column",
        required=True,
        help=(
            "Column name (or 0-based index if no header) containing the employee "
            "code. This code will be matched against the machine's employee list."
        ),
    )

    # --- Single-row mode: combined datetime ---

    check_in_column = fields.Char(
        string="Check-in Column",
        help=(
            "Column name/index for the combined check-in datetime. "
            "Used when Row Mode = Single Row and Datetime Mode = Combined."
        ),
    )
    check_out_column = fields.Char(
        string="Check-out Column",
        help=(
            "Column name/index for the combined check-out datetime. "
            "Used when Row Mode = Single Row and Datetime Mode = Combined."
        ),
    )

    # --- Single-row mode: separate date/time ---

    check_in_date_column = fields.Char(
        string="Check-in Date Column",
        help=(
            "Column name/index for the check-in date. "
            "Used when Row Mode = Single Row and Datetime Mode = Separate."
        ),
    )
    check_in_time_column = fields.Char(
        string="Check-in Time Column",
        help=(
            "Column name/index for the check-in time. "
            "Used when Row Mode = Single Row and Datetime Mode = Separate."
        ),
    )
    check_out_date_column = fields.Char(
        string="Check-out Date Column",
        help=(
            "Column name/index for the check-out date. "
            "Used when Row Mode = Single Row and Datetime Mode = Separate."
        ),
    )
    check_out_time_column = fields.Char(
        string="Check-out Time Column",
        help=(
            "Column name/index for the check-out time. "
            "Used when Row Mode = Single Row and Datetime Mode = Separate."
        ),
    )

    # --- Separate-rows mode ---

    row_type_column = fields.Char(
        string="Row Type Column",
        help=(
            "Column name/index that indicates whether the row is a check-in "
            "or check-out record. Used when Row Mode = Separate Rows."
        ),
    )
    sign_in_value = fields.Char(
        string="Sign-in Value",
        help=(
            "Value in the Row Type Column that identifies a check-in row. "
            "Used when Row Mode = Separate Rows."
        ),
    )
    sign_out_value = fields.Char(
        string="Sign-out Value",
        help=(
            "Value in the Row Type Column that identifies a check-out row. "
            "Used when Row Mode = Separate Rows."
        ),
    )

    # --- Row exclusion ---

    exclude_column = fields.Char(
        string="Exclude Column",
        help=(
            "Column name/index used to decide whether a row must be discarded "
            "before processing (e.g. a machine exception/validity column). "
            "Leave empty together with Exclude Values to disable this feature."
        ),
    )
    exclude_values = fields.Char(
        string="Exclude Values",
        help=(
            "Comma-separated list of values in the Exclude Column that mark a "
            "row as junk/duplicate to be discarded (e.g. 'Invalid,Mengulang'). "
            "Leave empty together with Exclude Column to disable this feature."
        ),
    )

    # --- Separate-rows mode: combined datetime ---

    datetime_column = fields.Char(
        string="Datetime Column",
        help=(
            "Column name/index for the combined datetime. "
            "Used when Row Mode = Separate Rows and Datetime Mode = Combined."
        ),
    )

    # --- Separate-rows mode: separate date/time ---

    date_column = fields.Char(
        string="Date Column",
        help=(
            "Column name/index for the date. "
            "Used when Row Mode = Separate Rows and Datetime Mode = Separate."
        ),
    )
    time_column = fields.Char(
        string="Time Column",
        help=(
            "Column name/index for the time. "
            "Used when Row Mode = Separate Rows and Datetime Mode = Separate."
        ),
    )

    # --- Format strings ---

    datetime_format = fields.Char(
        string="Datetime Format",
        default="%Y-%m-%d %H:%M:%S",
        help=(
            "Python strptime format string for combined datetime fields. "
            "Example: '%Y-%m-%d %H:%M:%S' or '%d/%m/%Y %H:%M'."
        ),
    )
    date_format = fields.Char(
        string="Date Format",
        default="%Y-%m-%d",
        help=(
            "Python strptime format string for date-only fields. "
            "Example: '%Y-%m-%d' or '%d/%m/%Y'."
        ),
    )
    time_format = fields.Char(
        string="Time Format",
        default="%H:%M:%S",
        help=(
            "Python strptime format string for time-only fields. "
            "Example: '%H:%M:%S' or '%H:%M'."
        ),
    )

    @api.constrains("offset_row", "offset_column", "sheet_index")
    def _check_offsets(self):
        """Reject negative offsets.

        Raises ``ValidationError`` when ``offset_row``,
        ``offset_column`` or ``sheet_index`` is negative.
        """
        for rec in self:
            if rec.offset_row < 0 or rec.offset_column < 0:
                raise ValidationError(_("Offsets cannot be negative."))
            if rec.sheet_index < 0:
                raise ValidationError(_("Sheet Index cannot be negative."))

    def _get_column_delimiter_character(self):
        """Resolve the ``delimiter`` selection to its literal character.

        :return: one of ``,``, ``;``, tab, ``|``, space; ``,`` if the
            selection value is unrecognized
        """
        self.ensure_one()
        return {
            "comma": ",",
            "semicolon": ";",
            "tab": "\t",
            "pipe": "|",
            "space": " ",
        }.get(self.delimiter, ",")

    def _get_sign_value_tokens(self, direction):
        """Return the list of Row Type Column values that identify a check-in
        (direction='in') or check-out (direction='out') row in Separate Rows mode.

        Each token is split on comma and stripped, but EMPTY tokens are kept:
        a blank Row Type Column value is a legitimate sign-in/out label on some
        machines, and today's exact-match behavior already relies on that (a
        blank sign_in_value/sign_out_value matches a blank row value). A single
        value without a comma yields exactly one token, so mappings configured
        before this feature existed behave identically (zero regression).
        """
        self.ensure_one()
        raw = self.sign_in_value if direction == "in" else self.sign_out_value
        return [token.strip() for token in (raw or "").split(",")]

    def _get_exclude_value_tokens(self):
        """Return the list of Exclude Column values that mark a row as
        junk/duplicate to be discarded before processing.

        Unlike `_get_sign_value_tokens`, EMPTY tokens are discarded here, and
        the feature is disabled (empty list) whenever Exclude Column or
        Exclude Values is not configured. Without this, an Exclude Column
        filled in with Exclude Values left empty would discard every row
        whose column happens to be blank -- the majority of most files.
        """
        self.ensure_one()
        if not self.exclude_column or not self.exclude_values:
            return []
        return [
            token.strip() for token in self.exclude_values.split(",") if token.strip()
        ]

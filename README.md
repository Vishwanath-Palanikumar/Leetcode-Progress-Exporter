# LeetCode Progress Exporter

A small Python command-line tool that exports problems marked as solved on your LeetCode account to a CSV file. The CSV can be opened in Excel or imported into Google Sheets.

## Features

- Retrieves solved-problem data in pages.
- Exports one row per unique problem.
- Sorts by LeetCode problem number.
- Includes problem title, difficulty, URL, last accepted timestamp, and topic tags.
- Writes a UTF-8 CSV suitable for spreadsheet applications.
- Reads the LeetCode session cookie from an environment variable rather than hardcoding it.

## CSV fields

| Field | Description |
|---|---|
| `Problem Number` | LeetCode's displayed problem number |
| `Title` | Problem title |
| `Difficulty` | Easy, Medium, or Hard |
| `URL` | Direct link to the problem |
| `Last Accepted Timestamp` | Timestamp returned by LeetCode's progress query |
| `Topics` | Topic tags returned by LeetCode |

## Requirements

- Python 3.10 or newer recommended
- A LeetCode account
- Internet access
- A session cookie from your own logged-in browser session

## Setup on Windows

Clone the repository or download its ZIP, then open PowerShell in the project directory.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, you can skip activation and install with `py -m pip install -r requirements.txt`.

### Set your session cookie

In your browser, sign in to LeetCode and use the browser developer tools to locate the `LEETCODE_SESSION` cookie for `leetcode.com`.

In PowerShell, set it for the current terminal session:

```powershell
$env:LEETCODE_SESSION = "PASTE_YOUR_COOKIE_VALUE_HERE"
```

**Security:** Treat this cookie like a password. Do not commit it, paste it into issues, or share it with anyone. The environment variable is temporary and is cleared when that terminal session ends.

### Run the exporter

```powershell
py .\export_leetcode_solved.py
```

The output file `leetcode_solved_problems.csv` is created in the same directory as the script.

## Import into Google Sheets

1. Open Google Sheets.
2. Select **File → Import → Upload**.
3. Select `leetcode_solved_problems.csv`.
4. Choose whether to create a new spreadsheet or insert a new sheet.

## Troubleshooting

- **`LEETCODE_SESSION is missing`:** Set the environment variable in the same PowerShell window where you run the script.
- **HTTP or GraphQL errors:** LeetCode's internal GraphQL API can change. Review the error message and update the query if the schema changes.
- **No solved problems returned:** Confirm that your account's LeetCode Progress page shows solved problems and that your session is valid.
- **Authentication or security page:** Sign in again and use a fresh session cookie. Never share the cookie in a bug report.

## Limitations

This project uses LeetCode's internal GraphQL endpoint, which is not a stable, officially documented public API. Fields, query names, authentication requirements, and response formats may change. The exporter only includes fields returned by the current query; it does not retrieve every submission attempt or provide a full submission-history export.

This is an independent community project and is not affiliated with or endorsed by LeetCode.

## Responsible use

- Use only your own account/session.
- Keep your session cookie private.
- Avoid excessive requests; the script uses pagination rather than requesting all records in one call.
- Check LeetCode's current terms and policies before using or redistributing data.

## License

Distributed under the MIT License. See [LICENSE](LICENSE).

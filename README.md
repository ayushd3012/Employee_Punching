# Employ_Inn — Simple Attendance Logger ✅

**Short description:**
A minimal command-line attendance logger which records "IN" and "OUT" punches to `attendance.csv`. The tool only keeps and shows entries from the last **24 hours** and reports per-session durations and per-person totals for that window.

---

## Features ✨
- Punch In / Punch Out logging (name, type, time) to `attendance.csv` (CSV format)
- Automatic cleanup that keeps only the last 24 hours of records
- `show_log()` prints session ranges and durations and a total worked time per user (last 24 hours)
- No external dependencies — uses Python standard library

## Requirements 🔧
- Python 3.6 or later

## Files
- `Employ_Inn.py` — main script (interactive)
- `attendance.csv` — data file (created automatically, header: `Name,Punch Type,Time`)
- `README.md` — this file

## Quick usage 💡
1. Run the script:

```powershell
python "c:\College things\Python\Employ_Inn.py"
```

2. Interactive menu options:
- `1` Punch In — type your name when prompted
- `2` Punch Out — type your name when prompted
- `3` Show Attendance Log — lists sessions and total worked time in last 24 hours
- `4` Exit

Example flow:
- Choose `1` → enter `Alice` (logs an IN timestamp)
- Choose `2` → enter `Alice` (logs an OUT timestamp)
- Choose `3` → shows `Alice` session with duration and total time

## Format of `attendance.csv` 📄
CSV with header row: `Name,Punch Type,Time`. Time format: `YYYY-MM-DD HH:MM:SS`.

## Behavior notes ⚠️
- The script will automatically remove entries older than 24 hours on startup and after each punch.
- If an `IN` exists without a matching `OUT` in the last 24 hours, the log will treat the current time as the open session end when showing totals.
- To preserve older records, remove or modify the `cleanup_old_entries()` calls in `Employ_Inn.py`.

## Testing / Quick verification ✅
- Start the script, punch in and out with a test name, then choose `3` to view the session(s) and verify the durations.

## Extending
- Add persistent per-day archives instead of deleting old entries.
- Add a CSV export or a small GUI.

---

If you want, I can run the script and demonstrate a sample session and the log output. Would you like me to do that?
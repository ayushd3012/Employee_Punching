import datetime
import csv
import os

FILE_NAME = "attendance.csv"

# Initialize CSV file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Punch Type", "Time"])


def punch_in(name):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, "IN", current_time])
    print(f"{name} punched IN at {current_time}")
    # remove entries older than 24 hours to keep log short
    cleanup_old_entries()

def punch_out(name):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, "OUT", current_time])
    print(f"{name} punched OUT at {current_time}")
    # remove entries older than 24 hours to keep log short
    cleanup_old_entries()

def _is_within_24_hours(timestamp_str):
    try:
        ts = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return False
    return datetime.datetime.now() - ts <= datetime.timedelta(days=1)


def cleanup_old_entries():
    # Keep only header + rows from the last 24 hours
    if not os.path.exists(FILE_NAME):
        return
    with open(FILE_NAME, mode="r", newline="") as file:
        reader = list(csv.reader(file))
    if not reader:
        return
    header, rows = reader[0], reader[1:]
    kept = [header]
    for row in rows:
        if len(row) >= 3 and _is_within_24_hours(row[2]):
            kept.append(row)
    # Only rewrite if we removed anything
    if len(kept) != len(reader):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(kept)


def show_log():
    print("\n--- Attendance Log (last 24 hours) ---")
    if not os.path.exists(FILE_NAME):
        print("No attendance records found.")
        return
    rows = []
    with open(FILE_NAME, mode="r", newline="") as file:
        reader = csv.reader(file)
        try:
            next(reader)
        except StopIteration:
            return
        for row in reader:
            if len(row) < 3:
                continue
            if not _is_within_24_hours(row[2]):
                continue
            try:
                ts = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            except Exception:
                continue
            rows.append((ts, row[0], row[1]))

    if not rows:
        print("No attendance entries in the last 24 hours.")
        return

    rows.sort()
    from collections import defaultdict

    sessions = defaultdict(list)  # name -> list of (start, end)
    last_in = {}
    for ts, name, typ in rows:
        if typ.upper() == "IN":
            last_in[name] = ts
        elif typ.upper() == "OUT":
            if name in last_in and last_in[name] is not None:
                sessions[name].append((last_in[name], ts))
                last_in[name] = None

    now = datetime.datetime.now()
    for name, in_ts in list(last_in.items()):
        if in_ts:
            sessions[name].append((in_ts, now))

    for name in sorted(sessions.keys()):
        total = datetime.timedelta()
        print(f"\n{name}:")
        for start, end in sessions[name]:
            dur = end - start
            total += dur
            h = start.strftime("%Y-%m-%d %H:%M:%S")
            e = end.strftime("%Y-%m-%d %H:%M:%S")
            # Format duration as H:M:S
            secs = int(dur.total_seconds())
            hh, rem = divmod(secs, 3600)
            mm, ss = divmod(rem, 60)
            print(f"  {h} -> {e}  ({hh}h {mm}m {ss}s)")
        total_secs = int(total.total_seconds())
        th, trem = divmod(total_secs, 3600)
        tm, ts = divmod(trem, 60)
        print(f"  Total: {th}h {tm}m {ts}s")

# Main loop
# Ensure old entries removed before starting interactive loop
cleanup_old_entries()
while True:
    print("\n1. Punch In")
    print("2. Punch Out")
    print("3. Show Attendance Log")
    print("4. Exit")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        name = input("Enter your name: ").strip().title()
        punch_in(name)
    elif choice == "2":
        name = input("Enter your name: ").strip().title()
        punch_out(name)
    elif choice == "3":
        show_log()
    elif choice == "4":
        print("Exiting system...")
        break
    else:
        print("Invalid choice, try again.")

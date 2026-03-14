# Date Manipulation in Python

Python provides powerful built-in modules for working with dates and times: `datetime`, `calendar`, and `zoneinfo` (Python 3.9+). For advanced needs, the third-party `dateutil` library is widely used.

---

## Importing the Modules

```python
from datetime import datetime, date, time, timedelta
import calendar
from zoneinfo import ZoneInfo          # Python 3.9+
from dateutil import parser, relativedelta  # pip install python-dateutil
```

---

## Core Classes

| Class | Description |
|---|---|
| `date` | Year, month, day only |
| `time` | Hour, minute, second, microsecond only |
| `datetime` | Combined date and time |
| `timedelta` | Duration / difference between two dates |
| `timezone` | Fixed UTC offset timezone |

---

## Creating Dates & Times

```python
# Specific date
d = date(2024, 3, 15)               # date(year, month, day)

# Specific datetime
dt = datetime(2024, 3, 15, 10, 30, 0)  # datetime(y, m, d, h, min, s)

# Current date and time
today      = date.today()
now        = datetime.now()          # local time
utc_now    = datetime.utcnow()       # UTC time (naive)

# From timestamp
dt = datetime.fromtimestamp(1710499800)

# From ISO format string
dt = datetime.fromisoformat('2024-03-15T10:30:00')
```

---

## Formatting Dates (datetime → string)

Use `strftime()` to format a datetime as a string.

```python
now = datetime.now()

print(now.strftime('%Y-%m-%d'))           # '2024-03-15'
print(now.strftime('%d/%m/%Y'))           # '15/03/2024'
print(now.strftime('%B %d, %Y'))          # 'March 15, 2024'
print(now.strftime('%I:%M %p'))           # '10:30 AM'
print(now.strftime('%Y-%m-%d %H:%M:%S'))  # '2024-03-15 10:30:00'
```

### Common Format Codes

| Code | Meaning | Example |
|---|---|---|
| `%Y` | 4-digit year | `2024` |
| `%y` | 2-digit year | `24` |
| `%m` | Month (zero-padded) | `03` |
| `%B` | Full month name | `March` |
| `%b` | Abbreviated month | `Mar` |
| `%d` | Day (zero-padded) | `15` |
| `%A` | Full weekday name | `Friday` |
| `%a` | Abbreviated weekday | `Fri` |
| `%H` | Hour 24h | `10` |
| `%I` | Hour 12h | `10` |
| `%M` | Minute | `30` |
| `%S` | Second | `00` |
| `%p` | AM/PM | `AM` |
| `%Z` | Timezone name | `UTC` |
| `%j` | Day of year | `075` |
| `%w` | Weekday number (0=Sun) | `5` |

---

## Parsing Dates (string → datetime)

Use `strptime()` for known formats, or `dateutil.parser` for flexible parsing.

```python
# Known format
dt = datetime.strptime('15-03-2024', '%d-%m-%Y')
dt = datetime.strptime('March 15, 2024', '%B %d, %Y')

# Flexible / unknown format (requires python-dateutil)
from dateutil import parser
dt = parser.parse('March 15, 2024')
dt = parser.parse('15/03/2024')
dt = parser.parse('2024-03-15T10:30:00')
dt = parser.parse('next Friday')        # Natural language
```

---

## Arithmetic with timedelta

```python
from datetime import timedelta

now = datetime.now()

# Add / subtract time
tomorrow     = now + timedelta(days=1)
last_week    = now - timedelta(weeks=1)
in_two_hours = now + timedelta(hours=2)
ninety_days  = now + timedelta(days=90)

# timedelta supports: days, seconds, microseconds,
#                     milliseconds, minutes, hours, weeks

# Difference between two dates
d1 = date(2024, 1, 1)
d2 = date(2024, 3, 15)
diff = d2 - d1
print(diff.days)        # 74
print(diff.total_seconds())  # 6393600.0
```

---

## Relative Deltas (months & years)

`timedelta` doesn't support months/years directly. Use `relativedelta` from `dateutil`:

```python
from dateutil.relativedelta import relativedelta

now = datetime.now()

next_month     = now + relativedelta(months=1)
next_year      = now + relativedelta(years=1)
three_months   = now + relativedelta(months=3)
one_year_ago   = now - relativedelta(years=1)

# Age calculation
birthday = date(1990, 6, 15)
age = relativedelta(date.today(), birthday).years
print(age)  # e.g., 33
```

---

## Accessing Date Components

```python
dt = datetime(2024, 3, 15, 10, 30, 45)

print(dt.year)        # 2024
print(dt.month)       # 3
print(dt.day)         # 15
print(dt.hour)        # 10
print(dt.minute)      # 30
print(dt.second)      # 45
print(dt.weekday())   # 4 (Monday=0, Sunday=6)
print(dt.isoweekday())# 5 (Monday=1, Sunday=7)
print(dt.date())      # datetime.date(2024, 3, 15)
print(dt.time())      # datetime.time(10, 30, 45)
```

---

## Start & End of Periods

```python
today = date.today()

# Start / end of month
start_of_month = today.replace(day=1)
last_day = calendar.monthrange(today.year, today.month)[1]
end_of_month = today.replace(day=last_day)

# Start of week (Monday)
start_of_week = today - timedelta(days=today.weekday())

# Start of year
start_of_year = date(today.year, 1, 1)

# End of year
end_of_year = date(today.year, 12, 31)
```

---

## Timezones

```python
from datetime import timezone
from zoneinfo import ZoneInfo  # Python 3.9+

# UTC-aware datetime
utc_now = datetime.now(tz=timezone.utc)

# Specific timezone
ist_now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
ny_now  = datetime.now(tz=ZoneInfo('America/New_York'))

# Convert between timezones
utc_dt = datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc)
ist_dt = utc_dt.astimezone(ZoneInfo('Asia/Kolkata'))
print(ist_dt)  # 2024-03-15 15:30:00+05:30

# Strip timezone (make naive)
naive_dt = ist_dt.replace(tzinfo=None)
```

---

## Useful Checks & Utilities

```python
# Is it a leap year?
calendar.isleap(2024)   # True

# Days in a month
calendar.monthrange(2024, 2)[1]   # 29 (leap year)

# Compare dates
d1 = date(2024, 1, 1)
d2 = date(2024, 6, 1)
print(d1 < d2)    # True
print(d1 == d2)   # False

# Min / Max of a list of dates
dates = [date(2024, 3, 1), date(2024, 1, 5), date(2024, 7, 20)]
print(min(dates))  # 2024-01-05
print(max(dates))  # 2024-07-20

# Convert date to datetime
dt = datetime.combine(date.today(), time.min)   # midnight

# Unix timestamp
timestamp = datetime.now().timestamp()
dt = datetime.fromtimestamp(timestamp)
```

---

## Common Patterns

```python
# Check if a date is a weekend
def is_weekend(d: date) -> bool:
    return d.weekday() >= 5  # 5=Sat, 6=Sun

# Get all Mondays in a month
def mondays_in_month(year, month):
    cal = calendar.monthcalendar(year, month)
    return [week[0] for week in cal if week[0] != 0]

# Days until a future date
def days_until(target: date) -> int:
    return (target - date.today()).days

# Format relative time (e.g., "3 days ago")
def relative_time(dt: datetime) -> str:
    delta = datetime.now() - dt
    if delta.days > 0:
        return f"{delta.days} day(s) ago"
    hours = delta.seconds // 3600
    if hours > 0:
        return f"{hours} hour(s) ago"
    minutes = delta.seconds // 60
    return f"{minutes} minute(s) ago"
```

---

## Quick Reference: Module Cheatsheet

| Task | Code |
|---|---|
| Today's date | `date.today()` |
| Current datetime | `datetime.now()` |
| Format to string | `dt.strftime('%Y-%m-%d')` |
| Parse from string | `datetime.strptime(s, fmt)` |
| Add days | `dt + timedelta(days=n)` |
| Add months | `dt + relativedelta(months=n)` |
| Date difference | `(d2 - d1).days` |
| Convert timezone | `dt.astimezone(ZoneInfo('...'))` |
| Unix timestamp | `dt.timestamp()` |
| ISO format | `dt.isoformat()` |

---

## Tips

- Always use **timezone-aware** datetimes for production apps to avoid bugs.
- Use `dateutil.relativedelta` for month/year arithmetic — `timedelta` only handles fixed durations.
- Store dates in **UTC** internally; convert to local time only for display.
- `datetime.fromisoformat()` is the fastest way to parse ISO 8601 strings (Python 3.7+).

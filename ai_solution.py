To solve this task, we need to format a list of date strings from a specific format to a more readable format.

Here is the code:

```python
from datetime import datetime

def format_dates(dates):
    formatted_dates = []
    for date in dates:
        dt = datetime.fromisoformat(date)
        formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        formatted_dates.append(formatted_date)
    return formatted_dates

# Example usage:
dates = [
    "2025-12-14T04:51:46Z",
    "2026-01-01T10:56:05Z",
    "2026-01-01T10:56:06Z",
    "2026-02-26T14:49:24Z",
    "2026-02-26T14:50:18Z",
    "2026-02-26T14:52:19Z",
    "2026-02-26T20:15:44Z",
    "2026-02-26T20:15:47Z",
    "2026-03-01T13:24:18Z",
    "2026-03-01T13:30:22Z",
    "2026-03-01T13:31:19Z",
    "2026-03-01T13:32:39Z",
    "2026-03-01T13:33:28Z"
]

formatted = format_dates(dates)
for date in formatted:
    print(date)
```

The function `format_dates` takes a list of date strings in the format "YYYY-MM-DDTHH:MM:SSZ" and converts them to the format "YYYY-MM-DD HH:MM:SS". Each date is parsed using `datetime.fromisoformat()` and then formatted accordingly. The example usage demonstrates how the function works with the provided dates.
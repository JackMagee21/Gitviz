
def format_size(size):
    # Turn a byte count into something readable, e.g. 2048 -> '2.0 KB'.
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def format_date(date):
    # Turn a date into text like '20 Sep 2026'.
    return date.strftime("%d %b %Y") if date else "Unknown"


def bar(value, max_value, width=20, fill="#", empty="-"):
    # Renders a simple ASCII meter, e.g. bar(3, 10, width=10) -> '###-------'.
    if max_value <= 0:
        filled = 0
    else:
        filled = max(0, min(width, round((value / max_value) * width)))
    return fill * filled + empty * (width - filled)
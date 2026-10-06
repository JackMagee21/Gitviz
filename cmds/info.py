from utils.formatting import format_date, format_size
from utils.colors import color

from colorama import Fore, Style

lines = []

LANGUAGE_BAR_WIDTH = 24
LANGUAGE_COLORS = (Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED)

# Returns a stacked bar plus a legend, e.g. '[######------] Python 82.1%, Shell 17.9%'.
def get_language_breakdown(repo):
    languages = repo.get_languages()   # costs 1 extra request
    # Separates JSON values into a str "lang" and num is the byte count of that language within the repo
    byte_counts = [(lang, num) for lang, num in languages.items() if lang != 'url']
    total = sum(num for _, num in byte_counts)

    if total == 0:
        return "None detected"

    # Only shows the top 5 languages within the repo
    top_languages = byte_counts[:5]

    bar_parts = []
    legend_parts = []
    allocated = 0
    for i, (lang, num) in enumerate(top_languages):
        fore = LANGUAGE_COLORS[i % len(LANGUAGE_COLORS)]
        percent = num / total * 100
        # Give the last segment whatever width is left so rounding can't under/overfill the bar.
        is_last = i == len(top_languages) - 1
        segment_width = (LANGUAGE_BAR_WIDTH - allocated) if is_last else round(num / total * LANGUAGE_BAR_WIDTH)
        allocated += segment_width

        bar_parts.append(color("#" * segment_width, fore))
        legend_parts.append(f"{color(lang, fore)} {percent:.1f}%")

    return f"[{''.join(bar_parts)}] " + ", ".join(legend_parts)


def cmd_info(repo_wrapper):
    repo = repo_wrapper.repo

    description = repo.description or "No description"
    licence = repo.license.name if repo.license else "No licence"
    visibility = "Private" if repo.private else "Public"

    status = []
    if repo.archived:
        status.append("archived")
    if repo.fork:
        status.append(f"fork of {repo.parent.full_name}")

    rows = [
        ("Name", repo.full_name),
        ("Description", description),
        ("URL", repo.html_url),
        ("Visibility", visibility),
        ("Default branch", repo.default_branch),
        ("Stars", repo.stargazers_count),
        ("Forks", repo.forks_count),
        ("Watchers", repo.subscribers_count),
        ("Open issues", repo.open_issues_count),
        ("Size", format_size(repo.size * 1024)),
        ("Licence", licence),
        ("Created", format_date(repo.created_at)),
        ("Last push", format_date(repo.pushed_at)),
        ("Languages", get_language_breakdown(repo)),
    ]

    if status:
        rows.append(("Status", ", ".join(status)))

    label_width = max(len(label) for label, _ in rows)

    for label, value in rows:
        padded_label = label.ljust(label_width)
        # Creates a green label with a white colon and the value of the label, e.g. "Name: repo_name"
        line = f"{color(padded_label, Fore.GREEN)} {Style.BRIGHT}{color(':' , Fore.WHITE)}{Style.RESET_ALL} {value}"
        lines.append(line)
    
    return "\n".join(lines)
from colorama import Fore
from github import GithubException

from utils.colors import color
from utils.formatting import format_date
from utils.paths import figure_path 

DEFAULT_COUNT = 10
MAX_COUNT = 100
MAX_MESSAGE_LENGTH = 70


def parse_log_args(parameters):
    # Split the parameters into a commit count and an optional path.
    count = DEFAULT_COUNT
    target = None

    for word in parameters.split():
        if word.isdigit():
            count = int(word)
        else:
            target = word

    count = min(count, MAX_COUNT)   # GitHub pages max out at 100
    return count, target


def first_line(message):
    # Return the first line of a commit message, shortened if it's too long.
    line = message.splitlines()[0] if message else ""
    if len(line) > MAX_MESSAGE_LENGTH:
        line = line[:MAX_MESSAGE_LENGTH - 3] + "..."
    return line


def cmd_log(repo, parameters=""):
    count, target = parse_log_args(parameters)
    if count < 1:
        print("log: commit count must be above 0, e.g. 'log 5'")
        return

    path = figure_path(repo.current_path, target) if target else repo.current_path

    try:
        current_commit_ids = repo.get_commits(count, path)
    except GithubException as e:
        if e.status == 409:   # GitHub returns 409 for a repo with no commits
            print("log: no commits found")
            return
        raise

    if not current_commit_ids:
        print(f"log: {target}: no commits found" if target else "log: no commits found")
        return

    headers = ("Commit ID", "Author", "Date", "Message")
    rows = [
        (
            com.sha[:7],
            com.commit.author.name or "Unknown",
            format_date(com.commit.author.date),
            first_line(com.commit.message),
        )
        for com in current_commit_ids
    ]

    # Work out how wide each column needs to be so everything lines up
    widths = [
        max(len(header), max(len(row[col]) for row in rows))
        for col, header in enumerate(headers)
    ]
    column_colors = (Fore.CYAN, Fore.YELLOW, Fore.MAGENTA, Fore.GREEN)

    def render_row(values, colors=None):
        cells = []
        for value, width, fore in zip(values, widths, colors or (None,) * len(values)):
            padded = value.ljust(width)
            cells.append(color(padded, fore) if fore else padded)
        return "  ".join(cells)

    print(render_row(headers, column_colors))
    print(render_row(["-" * width for width in widths]))
    for row in rows:
        print(render_row(row, column_colors))

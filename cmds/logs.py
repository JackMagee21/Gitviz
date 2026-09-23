from github import Github, GithubException
from colorama import Fore, Style

from utils.colors import color
from utils.formatting import format_date
from utils.paths import figure_path 

DEFAULT_COUNT = 10
DEFAULT_NUM_OF_LOGS = 10
MAX_COUNT = 100
MAX_MESSAGE_LENGTH = 70


git = Github()

def parse_log_args(parameters):
    # Split the parameters into a commit count and an optional path.
    count = DEFAULT_COUNT
    target = None

    for word in parameters.split():
        if word.isdigit():
            count = int(word)
        else:
            target = word

    count = max(1, min(count, MAX_COUNT))   # keep count between 1 and 100
    return count, target


def first_line(message):
    # Return the first line of a commit message, shortened if it's too long.
    line = message.splitlines()[0] if message else ""
    if len(line) > MAX_MESSAGE_LENGTH:
        line = line[:MAX_MESSAGE_LENGTH - 3] + "..."
    return line


def cmd_log(repo, parameters=""):

    current_commit_ids = None
    current_repo_path = repo.current_path

    if parameters == "":
        current_commit_ids = repo.get_commits(DEFAULT_NUM_OF_LOGS, current_repo_path)
    else:
        current_commit_ids = repo.get_commits(int(parameters), current_repo_path)

    if not current_commit_ids:
        print("log: no commits found")
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

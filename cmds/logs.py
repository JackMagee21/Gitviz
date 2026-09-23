from github import GithubException
from colorama import Fore, Style

from utils.colors import color
from utils.formatting import format_date
from utils.paths import figure_path 

DEFAULT_COUNT = 10
MAX_COUNT = 100
MAX_MESSAGE_LENGTH = 60


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

    lines = []
    rows = []

    count, target = parse_log_args(parameters)
    path = figure_path(repo.current_path, target) if target else ""

    try:
        # if path isn't the root of the repo, it will get the commits of that path 
        if path != "":
            all_commits = repo.repo.get_commits(path=path)
        else:
            all_commits = repo.repo.get_commits()

        commits = list(all_commits[:count])
    except GithubException as e:
        if e.status == 409: # the status for no commits 
            return "log: this repo has no commits yet"
        return f"log: GitHub error ({e.status})"

    if not commits:
        return f"log: no commits found for '{target}'"

    # Gather the details first, so we can line up the author column
    for com in commits:
        details = com.commit
        rows.append((
            com.sha[:7],
            format_date(details.author.date),
            details.author.name or "Unknown",
            first_line(details.message),
        ))

    author_width = max(len(author) for _, _, author, _ in rows)
    for sha, date, author, message in rows:
        padded_author = author.ljust(author_width)
        lines.append(f"{color(sha, Fore.YELLOW)}  {date}  {color(padded_author, Fore.CYAN)}  {message}")
    return "\n".join(lines)
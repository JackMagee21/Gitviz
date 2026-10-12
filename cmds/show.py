from github import GithubException, UnknownObjectException
from colorama import Fore

from utils.colors import color
from utils.formatting import format_date
from utils.paths import figure_path

MAX_FILES = 50  # Commits can touch thousands of files, so only list the first 50

STATUS_COLORS = {
    "added": Fore.GREEN,
    "removed": Fore.RED,
    "modified": Fore.YELLOW,
    "renamed": Fore.CYAN,
}


def parse_show_args(parameters):
    # Split "<sha> [path]" into the commit sha and an optional file path.
    parts = parameters.strip().split(maxsplit=1)
    if not parts:
        return None, None
    return parts[0], (parts[1] if len(parts) > 1 else None)


def render_details(commit):
    # Commit details in the same "Label : value" style as 'info'.
    author = commit.commit.author
    stats = commit.stats
    rows = [
        ("Commit", commit.sha),
        ("Author", f"{author.name or 'Unknown'} <{author.email or 'no email'}>"),
        ("Date", format_date(author.date)),
        ("Changes", f"{color(f'+{stats.additions}', Fore.GREEN)} {color(f'-{stats.deletions}', Fore.RED)}"),
    ]

    label_width = max(len(label) for label, _ in rows)
    lines = []
    for label, value in rows:
        line = f"{color(label.ljust(label_width), Fore.GREEN)} : {value}"
        lines.append(line)

    # Show the full commit message, indented, rather than just the first line like 'log'
    lines.append("")
    for message_line in commit.commit.message.splitlines():
        lines.append(f"    {message_line}")
    return lines


def render_files(files, has_more):
    lines = ["", "Files changed:"]
    names = [f"{f.previous_filename} -> {f.filename}" if f.status == "renamed" else f.filename for f in files]
    status_width = max(len(f.status) for f in files)
    name_width = max(len(name) for name in names)

    for f, name in zip(files, names):
        status = color(f.status.ljust(status_width), STATUS_COLORS.get(f.status, Fore.WHITE))
        changes = f"{color(f'+{f.additions}', Fore.GREEN)} {color(f'-{f.deletions}', Fore.RED)}"
        lines.append(f"  {status}  {name.ljust(name_width)}  {changes}")

    if has_more:
        lines.append(f"  ...only the first {MAX_FILES} files are shown")
    lines.append("")
    lines.append("Type 'show <sha> <file>' to see the changes to one file.")
    return lines


def render_patch(file):
    # GitHub leaves out the patch for binary files and very large diffs
    if not file.patch:
        return [f"show: {file.filename}: no diff available (binary or too large)"]

    lines = [color(f"--- {file.filename}", Fore.WHITE)]
    for line in file.patch.splitlines():
        if line.startswith("@@"):
            lines.append(color(line, Fore.CYAN))
        elif line.startswith("+"):
            lines.append(color(line, Fore.GREEN))
        elif line.startswith("-"):
            lines.append(color(line, Fore.RED))
        else:
            lines.append(line)
    return lines


def cmd_show(repo, parameters=""):
    sha, target = parse_show_args(parameters)
    if not sha:
        return "show: no commit given, e.g. 'show a1b2c3d' (copy an ID from 'log')"

    try:
        commit = repo.repo.get_commit(sha)
    except UnknownObjectException:
        return f"show: {sha}: no such commit"
    except GithubException as e:
        # GitHub returns 422 for a sha that's malformed or too short to be unique
        if e.status == 422:
            return f"show: {sha}: no such commit"
        raise

    # The first page of files comes with the commit, so slicing here costs no extra requests
    files = list(commit.files[:MAX_FILES + 1])
    has_more = len(files) > MAX_FILES
    files = files[:MAX_FILES]

    if target:
        file_path = figure_path(repo.current_path, target)
        for f in files:
            if f.filename == file_path:
                return "\n".join(render_patch(f))
        return f"show: {target}: not changed in this commit"

    lines = render_details(commit)
    if files:
        lines += render_files(files, has_more)
    return "\n".join(lines)

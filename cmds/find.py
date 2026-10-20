import fnmatch

from colorama import Fore

from utils.colors import color


def cmd_find(repo, parameters=""):
    pattern = parameters.strip()
    if not pattern:
        return "find: give a name or pattern, e.g. 'find *.py' or 'find readme'"

    # No wildcards given: match anywhere in the name, so 'find readme' finds README.md
    if not any(c in pattern for c in "*?["):
        pattern = f"*{pattern}*"
    pattern = pattern.lower()

    # One API call for the whole tree, then filter it locally
    entries, truncated, error = repo.get_tree(repo.current_path)
    if error:
        return f"find: {error}"

    prefix = (repo.current_path + "/") if repo.current_path else ""
    lines = []
    for entry in sorted(entries, key=lambda e: e.path):
        rel_path = entry.path[len(prefix):]
        if not rel_path:  # the current directory itself
            continue

        # A pattern with a slash matches the path relative to here, otherwise just the name
        target = rel_path if "/" in pattern else rel_path.rsplit("/", 1)[-1]
        if not fnmatch.fnmatchcase(target.lower(), pattern):
            continue

        # Printed from the repo root so the result can be passed straight to cd or cat
        if entry.type == "tree":
            lines.append(color(f"/{entry.path}/", Fore.CYAN))
        else:
            lines.append(f"/{entry.path}")

    if not lines:
        return f"find: no matches for '{parameters.strip()}'"

    if truncated:
        lines.append("Note: GitHub truncated this tree because the repo is too large, so some matches may be missing")

    return "\n".join(lines)

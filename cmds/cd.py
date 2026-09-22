from github import UnknownObjectException
from utils.paths import figure_path


def cmd_cd(repo, parameters=""):
    target = parameters.strip()

    # "cd", "cd /" and "cd ~" all go back to the root
    if target in ("", "/", "~"):
        repo.current_path = ""
        return None

    new_path = figure_path(repo.current_path, target)

    if new_path == "":             # e.g. "cd .." from a top-level folder
        repo.current_path = ""
        return None

    try:
        contents = repo.repo.get_contents(new_path)
    except UnknownObjectException:
        return f"cd: {target}: no such directory"

    if not isinstance(contents, list):
        return f"cd: {target}: not a directory"

    repo.current_path = new_path
    return None
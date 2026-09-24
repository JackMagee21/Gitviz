from utils.paths import figure_path


def cmd_tree(repo, parameters=""):
    target = parameters.strip()
    path = figure_path(repo.current_path, target) if target else repo.current_path

    entries, error = repo.get_tree(path)
    if error:
        print(f"tree: {target or '.'}: {error}")
        return

    for entry in sorted(entries, key=lambda e: e.path):
        suffix = "/" if entry.type == "tree" else ""
        print(f"{entry.path}{suffix}")

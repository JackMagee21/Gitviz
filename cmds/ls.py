from github import UnknownObjectException

def cmd_ls(repo, path=""):
    try:
        items = repo.repo.get_contents(path)
    except UnknownObjectException:
        return f"ls: {path}: no such directory"

    if not isinstance(items, list):   # the path was a single file
        return items.name

    lines = []
    for item in sorted(items, key=lambda i: (i.type != "dir", i.name)):
        lines.append(f"{item.name}/" if item.type == "dir" else item.name)
    return "\n".join(lines)
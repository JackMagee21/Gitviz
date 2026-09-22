from github import UnknownObjectException

def sort_folders_first(item):
    return (item.type != "dir", item.name)


def cmd_ls(repo, path=""):
    lines = []
    try:
        items = repo.repo.get_contents(path)
    except UnknownObjectException:
        return f"ls: {path}: no such directory"

    if not isinstance(items, list):   # the path was a single file
        return items.name

    

    # Sorts each item in a list of files and directories, putting directories first and then files, both in alphabetical order.
    sorted_items = sorted(items, key=sort_folders_first)

    for item in sorted_items:
        if item.type == "dir":
            lines.append(f"{item.name}/")
        else:
            lines.append(item.name)

    return "\n".join(lines)
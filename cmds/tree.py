from colorama import Fore

from utils.colors import color
from utils.paths import figure_path

BRANCH = "|-- "
LAST_BRANCH = "`-- "
PIPE = "|   "
BLANK = "    "


def build_tree(entries, base_path):
    # Turns the flat list of blob paths into a nested dict of
    # {name: {...}} for directories and {name: None} for files.
    prefix = (base_path + "/") if base_path else ""
    root = {}

    for entry in entries:
        if entry.type != "blob":
            continue

        rel_path = entry.path[len(prefix):]
        parts = rel_path.split("/")

        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = None

    return root


def render_tree(node, prefix=""):
    lines = []
    dir_count = 0
    file_count = 0

    # Folders first, then files, both alphabetical
    items = sorted(node.items(), key=lambda kv: (kv[1] is None, kv[0].lower()))

    for i, (name, children) in enumerate(items):
        is_last = i == len(items) - 1
        connector = LAST_BRANCH if is_last else BRANCH
        is_dir = children is not None

        if is_dir:
            dir_count += 1
            lines.append(f"{prefix}{connector}{color(name + '/', Fore.CYAN)}")
            child_lines, child_dirs, child_files = render_tree(
                children, prefix + (BLANK if is_last else PIPE)
            )
            lines.extend(child_lines)
            dir_count += child_dirs
            file_count += child_files
        else:
            file_count += 1
            lines.append(f"{prefix}{connector}{name}")

    return lines, dir_count, file_count


def cmd_tree(repo, parameters=""):
    target = parameters.strip()
    path = figure_path(repo.current_path, target) if target else repo.current_path

    entries, error = repo.get_tree(path)
    if error:
        print(f"tree: {target or '.'}: {error}")
        return

    # A single exact match that's a file rather than a directory
    if len(entries) == 1 and entries[0].path == path and entries[0].type == "blob":
        print(entries[0].path.rsplit("/", 1)[-1])
        return

    label = path.rsplit("/", 1)[-1] if path else repo.get_repo()
    print(color(f"{label}/", Fore.CYAN))

    tree = build_tree(entries, path)
    lines, dir_count, file_count = render_tree(tree)
    for line in lines:
        print(line)

    print(f"\n{dir_count} director{'y' if dir_count == 1 else 'ies'}, "
          f"{file_count} file{'' if file_count == 1 else 's'}")

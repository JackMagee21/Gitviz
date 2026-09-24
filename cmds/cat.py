from utils.paths import figure_path

DEFAULT_PREVIEW_LINES = 40


def parse_cat_args(parameters):
    # Split "<path> [all]" into a target path and whether to show everything.
    parts = parameters.strip().split()
    if not parts:
        return None, False

    show_all = parts[-1].lower() == "all"
    if show_all:
        parts = parts[:-1]

    return " ".join(parts), show_all


def cmd_cat(repo, parameters=""):
    target, show_all = parse_cat_args(parameters)

    if not target:
        print("cat: no file specified, e.g. 'cat path/to/file.py'")
        return

    file_path = figure_path(repo.current_path, target)

    content, error = repo.get_file_content(file_path)
    if error:
        print(f"cat: {target}: {error}")
        return

    lines = content.splitlines()

    if show_all or len(lines) <= DEFAULT_PREVIEW_LINES:
        print(content)
        return

    print("\n".join(lines[:DEFAULT_PREVIEW_LINES]))
    print(f"\n... showing {DEFAULT_PREVIEW_LINES} of {len(lines)} lines, "
          f"run 'cat {target} all' to see the full file")

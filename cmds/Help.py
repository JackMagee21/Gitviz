COMMANDS = {
    "help":    ("help [command]",       "shows this list, or details about one command"),
    "info":    ("info",                 "shows details about the current repo (description, stars, languages, etc.)"),
    "ls":      ("ls [path]",            "lists files and folders in a directory (folders first, alphabetical)"),
    "cd":      ("cd [path]",            "changes directory; 'cd' or 'cd /' returns to the repo root, 'cd ..' goes up one level"),
    "log":     ("log [count]",          "shows the most recent commits for the current directory (default 10, max 100)"),
    "summary": ("summary",              "shows the top 5 contributors by commits, additions and deletions"),
    "repo":    ("repo <author/name>",   "switches to browsing a different repo, e.g. 'repo torvalds/linux'"),
    "q":       ("q",                    "quits the application"),
}


def help_cmd(parameters=""):
    # "help ls" shows just one command
    if parameters:
        name = parameters.strip().lower()
        if name not in COMMANDS:
            return f"help: no command called '{name}'"
        usage, description = COMMANDS[name]
        return f"{usage}\n    {description}"

    # plain "help" shows everything
    usage_width = max(len(usage) for usage, _ in COMMANDS.values())

    lines = ["Commands:"]
    for usage, description in COMMANDS.values():
        lines.append(f"  {usage:<{usage_width}}  {description}")
    lines.append("\nType 'help <command>' for more on one command.")
    return "\n".join(lines)
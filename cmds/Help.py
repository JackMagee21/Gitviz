COMMANDS = {
    "help":  ("help [command]", "shows this list, or details about one command"),
    "info":  ("info",           "shows details about the repo"),
    "ls":    ("ls [-l] [path]", "lists files in a folder (-l for sizes)"),
    "q":     ("q",              "quits the application"),
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
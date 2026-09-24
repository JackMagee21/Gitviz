from cmds.help import help_cmd
from cmds.ls import cmd_ls
from cmds.info import cmd_info
from cmds.cd import cmd_cd
from cmds.logs import cmd_log
from cmds.repo import cmd_repo
from cmds.summary import cmd_summary
from cmds.cat import cmd_cat
from cmds.tree import cmd_tree

def cmd(repo, command, parameters=""):
    if command == "help":
        print(help_cmd())
    elif command == "ls":
        print(cmd_ls(repo, parameters))
    elif command == "info":
        print(cmd_info(repo))
    elif command == "cd":
        cmd_cd(repo, parameters)
    elif command == "log":
        cmd_log(repo, parameters)
    elif command == "repo":
        cmd_repo(repo, parameters)
    elif command == "summary":
        cmd_summary(repo, parameters)
    elif command == "cat":
        cmd_cat(repo, parameters)
    elif command == "tree":
        cmd_tree(repo, parameters)
    else:
        print("Sorry, command not found")
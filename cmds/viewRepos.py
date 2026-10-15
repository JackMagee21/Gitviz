from colorama import Style, Fore
from utils.colors import color, bold

def cmd_view_repos(repo, parameters=""):
   for r in repo.get_repo_of_user(parameters):
      if r == repo.repo:
        print(f"{Style.BRIGHT}{color(r.name, Fore.GREEN)}")
      else:
        print(color(r.name, Fore.CYAN))
from github import Github
from RepoData import set_repo

git = Github()

def cmd_repo(repo, parameters=""):
    if parameters == "":
        print("Error: no repo name added, enter (for example) Author/Repo_name")

    if repo.switch_repo(parameters) == False:
        print("Repo cannot be found")
    
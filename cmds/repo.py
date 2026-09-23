from github import Github
from RepoData import set_repo

git = Github()

def cmd_repo(repo, parameters=""):
    if repo.switch_repo(parameters) == False:
        print("Repo cannot be found")
    
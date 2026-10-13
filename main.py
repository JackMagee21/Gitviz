from github import GithubException, RateLimitExceededException
from requests.exceptions import RequestException

from RepoData import set_repo, get_token_warning
from cmds.cmd import cmd
from cmds.clear import cmd_clear


def describe_api_error(error, label):
    # Turns an API/network failure into a one-line message instead of a traceback.
    # RateLimitExceededException is a subclass of GithubException, so check it first.
    if isinstance(error, RateLimitExceededException):
        return ("GitHub API rate limit reached - wait for the hourly reset, "
                "or run 'key <token>' to raise it to 5000/hr")
    if isinstance(error, GithubException):
        message = error.data.get("message") if isinstance(error.data, dict) else None
        return f"{label}: GitHub API error ({error.status})" + (f": {message}" if message else "")
    return f"{label}: network error - check your connection and try again"


def read_input(prompt):
    # Returns None on Ctrl+C / Ctrl+D (Ctrl+Z on Windows) so the caller can exit cleanly.
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main():
    cmd_clear()

    token_warning = get_token_warning()
    if token_warning:
        print(f"Warning: {token_warning}")

    current_repo = None

    while True:
        repo_name = read_input("Enter repo author and name with a slash (/) in between "
                               "(e.g. name/repo_name), or press q to quit: ")

        if repo_name is None or repo_name.lower() == "q":
            return

        try:
            current_repo = set_repo(repo_name)
        except (GithubException, RequestException) as e:
            print(describe_api_error(e, "repo"))
            continue

        if current_repo is None:
            print("Repo not found, please try again!")
        else:
            break

    while current_repo is not None:

        prompt = f"{current_repo.get_repo()}:/{current_repo.current_path}> "
        user_input = read_input(prompt)
        if user_input is None:
            break

        parts = user_input.split(maxsplit=1)

        if not parts:          # empty input, ask again
            continue

        # Split the input into the command and any parameters
        command = parts[0].lower()
        parameters = parts[1] if len(parts) > 1 else ""

        if command == "q":
            break

        try:
            cmd(current_repo, command, parameters)
        except (GithubException, RequestException) as e:
            print(describe_api_error(e, command))
        except KeyboardInterrupt:
            print()    # Ctrl+C cancels the running command, not the whole session


if __name__ == "__main__":
    main()

import os

from dotenv import set_key

import RepoData

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

def cmd_key(repo, parameters=""):
    if parameters == "-limit":
        return (f"Current rate limit: {RepoData.single_rate_limit()}")

    token = parameters.strip()

    if not token:
        limit = RepoData.single_rate_limit()
        return (f"key: limit = {limit}"
                f"Use 'key <token>' to set a GitHub token and raise this limit, to a max of 5000.")

    RepoData.set_github_token(token)
    set_key(ENV_PATH, "GITHUB_TOKEN", token)

    remaining, limit = RepoData.get_rate_limit()
    return f"key: token saved to .env, now authenticated ({remaining}/{limit} requests remaining this hour)"

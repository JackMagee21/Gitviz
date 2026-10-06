import os
import re

from dotenv import set_key

import RepoData

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

# Matches GitHub's current token shapes: classic 40-char hex PATs, the
# ghp_/gho_/ghu_/ghs_/ghr_ prefixed tokens, and fine-grained github_pat_ tokens.
TOKEN_PATTERN = re.compile(r"^(?:[0-9a-f]{40}|gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{22,255})$")

def cmd_key(repo, parameters=""):
    if parameters == "-limit":
        return (f"Current rate limit: {RepoData.single_rate_limit()}")

    # Strip whitespace and any wrapping quotes/backticks picked up from a copy-paste.
    token = parameters.strip().strip("'\"`")

    if not token:
        limit = RepoData.single_rate_limit()
        return (f"key: limit = {limit}"
                f"Use 'key <token>' to set a GitHub token and raise this limit, to a max of 5000.")

    if not TOKEN_PATTERN.match(token):
        return ("key: that doesn't look like a valid GitHub token "
                "(expected a ghp_/gho_/ghu_/ghs_/ghr_/github_pat_ token, or a classic 40-character hex token) "
                "- check for typos or extra characters and try again.")

    RepoData.set_github_token(token)
    set_key(ENV_PATH, "GITHUB_TOKEN", token)

    warning = RepoData.get_token_warning()
    if warning:
        return f"key: token saved to .env, but {warning}"

    remaining, limit = RepoData.get_rate_limit()
    return f"key: token saved to .env, now authenticated ({remaining}/{limit} requests remaining this hour)"

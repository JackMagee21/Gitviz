from cmds.ls import format_size
from utils.formatting import format_date


# Return languages as percentages, e.g. 'Python 82.1%, Shell 17.9%'.
def get_language_breakdown(repo):
    languages = repo.get_languages()   # costs 1 extra request
    total = sum(languages.values())
    if total == 0:
        return "None detected"

    parts = []
    for name, byte_count in languages.items():
        percent = byte_count / total * 100
        parts.append(f"{name} {percent:.1f}%")
    return ", ".join(parts)


def cmd_info(repo_wrapper):
    repo = repo_wrapper.repo

    description = repo.description or "No description"
    licence = repo.license.name if repo.license else "No licence"
    visibility = "Private" if repo.private else "Public"

    status = []
    if repo.archived:
        status.append("archived")
    if repo.fork:
        status.append(f"fork of {repo.parent.full_name}")

    rows = [
        ("Name", repo.full_name),
        ("Description", description),
        ("URL", repo.html_url),
        ("Visibility", visibility),
        ("Default branch", repo.default_branch),
        ("Stars", repo.stargazers_count),
        ("Forks", repo.forks_count),
        ("Watchers", repo.subscribers_count),
        ("Open issues", repo.open_issues_count),
        ("Size", format_size(repo.size * 1024)),
        ("Licence", licence),
        ("Created", format_date(repo.created_at)),
        ("Last push", format_date(repo.pushed_at)),
        ("Languages", get_language_breakdown(repo)),
    ]

    if status:
        rows.append(("Status", ", ".join(status)))

    label_width = max(len(label) for label, _ in rows)
    lines = [f"{label:<{label_width}} : {value}" for label, value in rows]
    return "\n".join(lines)
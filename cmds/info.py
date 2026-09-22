from utils.formatting import format_date, format_size


# Return languages as percentages, e.g. 'Python 82.1%, Shell 17.9%'.
def get_language_breakdown(repo):
    languages = repo.get_languages()   # costs 1 extra request
    parts = []
    total = 0
    # Seperates JSON values into a str "lang" and num is the byte count of that language within the repo
    for lang, num in languages.items():
        if lang != 'url':
            total += num
            if(total == 0):
                return "None detected"

    # Only gets the top 5 languages within the repo and calculates the percentage of each language within the repo
    for lang, num in list(languages.items())[:5]:
        if lang != 'url':
            precent = round(num / total * 100, 2)
            parts.append(f"{lang} {precent}%")

            

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
from colorama import Fore

from utils.colors import color
from utils.formatting import bar

BAR_WIDTH = 20

TOP_N = 5
LARGE_REPO_COMMIT_THRESHOLD = 10000  # GitHub omits addition/deletion counts past this
STATS_CONTRIBUTOR_CAP = 100  # GitHub's stats/contributors endpoint only ever returns the top 100


def cmd_summary(repo, parameters=""):
    print("Gathering contributor stats (GitHub may need a few seconds to "
          "compute these for a repo it hasn't cached recently)...")

    stats = repo.get_stats_contributors()

    if stats is None:
        print("summary: GitHub is still computing stats for this repo, try again shortly")
        return

    if not stats:
        print("summary: no contributors found")
        return

    total_commits = sum(contributor.total for contributor in stats)
    stats_unavailable = total_commits >= LARGE_REPO_COMMIT_THRESHOLD

    # GitHub caches contributor stats and computes them asynchronously; a repo with
    # recent commit activity can have a stale cache that silently omits contributors
    # or undercounts them, without ever signalling "still computing" (see get_stats_contributors).
    # Skip this check when the endpoint hit its documented 100-contributor cap, since
    # that alone (not staleness) explains a lower total and can't affect the top N shown.
    actual_commit_count = repo.repo.get_commits().totalCount
    if len(stats) < STATS_CONTRIBUTOR_CAP and total_commits < actual_commit_count:
        print(f"Warning: GitHub's cached contributor stats look stale "
              f"({total_commits}/{actual_commit_count} commits accounted for) - "
              "contributors below may be missing or undercounted.\n")

    contributors = []
    for contributor in stats:
        additions = sum(week.a for week in contributor.weeks)
        deletions = sum(week.d for week in contributor.weeks)
        share = (contributor.total / total_commits * 100) if total_commits else 0
        name = contributor.author.login if contributor.author else "Unknown"
        contributors.append((name, contributor.total, additions, deletions, share))

    # Rank by commit count and keep the top N
    contributors.sort(key=lambda row: row[1], reverse=True)
    top_contributors = contributors[:TOP_N]

    headers = ("Author", "Commits", "Bar", "Additions", "Deletions", "% of Commits")
    aligns = ("<", ">", "<", ">", ">", ">")
    column_colors = (Fore.CYAN, Fore.YELLOW, Fore.BLUE, Fore.GREEN, Fore.RED, Fore.MAGENTA)

    def format_changes(additions, deletions):
        if stats_unavailable:
            return "N/A", "N/A"
        return f"+{additions}", f"-{deletions}"

    # Bars are relative to the top contributor shown, not the whole repo.
    max_commits = top_contributors[0][1] if top_contributors else 0

    rows = []
    for name, commits, additions, deletions, share in top_contributors:
        added, removed = format_changes(additions, deletions)
        rows.append((name, str(commits), bar(commits, max_commits, width=BAR_WIDTH), added, removed, f"{share:.1f}%"))

    widths = [
        max(len(header), max(len(row[i]) for row in rows))
        for i, header in enumerate(headers)
    ]

    def render_row(values, colored=False):
        cells = []
        for value, width, align, fore in zip(values, widths, aligns, column_colors):
            padded = f"{value:{align}{width}}"
            cells.append(color(padded, fore) if colored else padded)
        return "  ".join(cells)

    print(render_row(headers, colored=True))
    print(render_row(["-" * width for width in widths]))
    for row in rows:
        print(render_row(row, colored=True))

    if stats_unavailable:
        print("\nNote: GitHub omits addition/deletion counts for repos with "
              f"{LARGE_REPO_COMMIT_THRESHOLD:,}+ commits, so those show as N/A.")

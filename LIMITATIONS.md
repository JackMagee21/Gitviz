# Gitviz — Known Limitations

This lists the current limitations of Gitviz: why each one exists, and how the tool behaves because of it. Most come from constraints in GitHub's REST API; a few are gaps in Gitviz itself.

## GitHub API constraints

| Limitation | Cause | Gitviz behaviour |
| --- | --- | --- |
| Capped at 60 requests/hour | Gitviz calls the GitHub REST API without authentication | Heavy browsing of one repo can exhaust the quota; requests then fail until the hour rolls over |
| Only public repos are accessible | Same as above — unauthenticated requests can't see private data | Private repos can't be browsed at all |
| Additions/Deletions show as `N/A` on repos with 10,000+ commits | GitHub's `stats/contributors` endpoint stops returning line-change counts past that size, to keep the endpoint fast | `summary` detects this and shows `N/A` instead of a misleading `0` |
| Contributor stats can take a few seconds to appear | GitHub computes `stats/contributors` asynchronously and returns "still generating" the first time a repo is queried | `summary` retries a few times with a short delay before giving up |
| Files over 1 MB can't be read | GitHub's Contents API only returns file content up to 1 MB | `cat` shows a "too large to display" message instead of the file |
| Binary files can't be displayed | File content comes back meant to be decoded as UTF-8 text | `cat` shows a "binary file, not displayed" message instead of raw bytes |

## Gaps in Gitviz itself

| Limitation | Detail |
| --- | --- |
| `ls` ignores the current directory | Calling `ls` with no path always lists the repo root, not wherever `cd` has navigated to — you need to pass the full path explicitly for now |
| `log` only accepts a commit count | `log <argument>` is parsed as a number; passing anything else (e.g. a folder name) raises an error instead of scoping the log to that path |
| `summary` is always repo-wide | GitHub's contributor-stats endpoint isn't scoped by path, so `cd`-ing into a folder has no effect on `summary` |
| `repo` with no argument can error out | It prints a usage message but still attempts to switch repos afterwards, which can raise an unhandled error instead of stopping cleanly |
| No branch or tag selection | Every command reads from the repo's default branch; there's no way to browse a different branch or tag |
| No search | There's no way to search file names or code content across a repo |
| No commit diff view | `log` shows commit messages, but there's no way to see what a specific commit actually changed |
| Single repo per session | Only one repo is "open" at a time; `repo` replaces it rather than letting you compare two |

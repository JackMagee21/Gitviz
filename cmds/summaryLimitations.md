# `summary` Command Limitations

Some limitations of the `summary` command come from constraints in the GitHub API itself, not from bugs in Gitviz.

## Known Limitations

| Limitation | Cause | Gitviz behaviour |
| --- | --- | --- |
| Additions / Deletions are inaccurate on repositories with 10,000+ commits | GitHub's `stats/contributors` endpoint returns `0` for addition/deletion counts once a repository passes 10,000 commits, to keep the endpoint performant | Detected automatically and displayed as `N/A` instead of a misleading `0` |

# Gitviz

![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-active%20development-brightgreen)

Gitviz is a terminal REPL for exploring a public GitHub repository — browse its file tree, read commit history, check repo metadata, and see top contributors — all live via the GitHub API, with nothing cloned to disk.

## Features

- **Browse the file tree** directory by directory (`ls`), or see the whole thing at once as a nested tree (`tree`)
- **View recent commit history**, scoped to whatever directory you're currently in
- **See repo metadata** — description, stars, forks, license, and a colorized language-breakdown bar
- **See the top 5 contributors** to a repo, ranked by commits, with an at-a-glance commit bar plus additions/deletions
- **Read file contents** straight from GitHub, with a preview cap for long files
- **Switch repos mid-session** without restarting the tool
- **Raise the API rate limit** from 60 to 5,000 requests/hour with a personal GitHub token, with a live color-coded usage bar
- Colorized output that auto-disables when piped to a file or when `NO_COLOR` is set

## Requirements

- Python 3.x
- [PyGithub](https://pypi.org/project/PyGithub/)
- [colorama](https://pypi.org/project/colorama/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

### Quick install (recommended)

Gitviz can be installed as a standalone `gitviz` command using [pipx](https://pipx.pypa.io/), which installs it into its own isolated environment and puts it on your PATH automatically:

```
pipx install git+https://github.com/JackMagee21/Gitviz.git
```

Don't have pipx yet? Install it once (works on Windows, macOS, and Linux):

```
pip install --user pipx
pipx ensurepath
```

Then re-open your terminal and run the `pipx install` command above. After that, `gitviz` works from any new terminal, anywhere.

### From source (for development)

```
git clone https://github.com/JackMagee21/Gitviz.git
cd Gitviz
pip install -e .
```

`pip install -e .` installs the same `gitviz` command, but editable — changes to the source take effect immediately without reinstalling. Note this installs into whatever Python environment is currently active, so `gitviz` is only on PATH if that environment's script/Scripts directory is too; `pipx` avoids that problem entirely.

## Usage

Once installed, just run:

```
gitviz
```

Or, without installing, run it directly from a clone:

```
python main.py
```

```
Enter repo author and name with a slash (/) in between (e.g. name/repo_name), or press q to quit: torvalds/linux
torvalds/linux:/> ls
torvalds/linux:/> cd kernel
torvalds/linux:/kernel> log 5
torvalds/linux:/> tree drivers/usb
torvalds/linux:/> summary
```

Type `q` at any prompt to quit.

### Raising the rate limit

Unauthenticated requests are capped at 60/hour. To raise that to 5,000/hour, generate a [personal access token](https://github.com/settings/tokens) (no scopes are needed for browsing public repos) and set it once:

```
torvalds/linux:/> key ghp_your_token_here
key: token saved to .env, now authenticated
[###################-] 4998/5000 requests remaining this hour
```

The token is saved to a local `.env` file (already gitignored) and reused on future runs. Run `key` with no arguments at any time to check your current usage.

## Commands

| Command | Usage | Description |
| --- | --- | --- |
| Help | `help [command]` | Shows this list, or details about one command |
| Info | `info` | Shows details about the current repo (description, stars, languages, etc.) |
| List | `ls [path]` | Lists files and folders in a directory (folders first, alphabetical) |
| Cat | `cat <path> [all]` | Shows a file's content; previews the first 40 lines unless `all` is given |
| Change directory | `cd [path]` | Changes directory; `cd` or `cd /` returns to the repo root, `cd ..` goes up one level |
| Log | `log [count]` | Shows the most recent commits for the current directory (default 10, max 100) |
| Summary | `summary` | Shows the top 5 contributors by commits, additions and deletions |
| Repo | `repo <author/name>` | Switches to browsing a different repo, e.g. `repo torvalds/linux` |
| Tree | `tree [path]` | Shows a nested tree of all files and folders under a path |
| Key | `key [token]` | Sets a GitHub token to raise the API rate limit (60/hr → 5,000/hr); no args shows current usage |
| Clear | `clear` | Clears the terminal screen (`clr` also works) |
| Quit | `q` | Quits the application |

Run `help <command>` inside the app for details on any single command.

## Current Limitations

- Even with a token, Gitviz is bound by whatever the GitHub REST API allows — unauthenticated sessions are capped at 60 requests/hour, and heavy browsing can still exhaust a token's 5,000/hour allowance.
- All commands are fetched live from GitHub each time, so results depend on GitHub's API availability and response time.
- Every command reads from the repo's default branch — there's no way to browse a different branch or tag.
- GitHub's `stats/contributors` endpoint is cached and computed asynchronously; `summary` detects and flags an obviously stale/incomplete cache, but can't force GitHub to recompute it.

See [`LIMITATIONS.md`](LIMITATIONS.md) for the full list, including known gaps in `ls`, `log`, `summary`, and `repo`.

## Project structure

```
main.py                    REPL entry point
RepoData.py                RepoWrapper: wraps the PyGithub repo object + current path, builds the GitHub client
cmds/
  cmd.py                   Command dispatcher
  help.py, info.py, ls.py, cd.py, logs.py, repo.py, summary.py, cat.py,
  tree.py, key.py, clear.py
                            One module per command
utils/
  colors.py                Color helper (auto-disables outside a TTY / with NO_COLOR)
  formatting.py            Shared display helpers (dates, byte sizes, ASCII bar meters)
  paths.py                 Resolves cd/ls/log paths against the current directory
.env                       Optional, gitignored: stores a GitHub token set via 'key <token>'
```

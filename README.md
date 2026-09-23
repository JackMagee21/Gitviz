# Gitviz

Gitviz is a terminal REPL for exploring a public GitHub repository — browse its file tree, read commit history, check repo metadata, and see top contributors — all live via the GitHub API, with nothing cloned to disk.

## Features

- **Browse the file tree** of a repo directory by directory
- **View recent commit history**, scoped to whatever directory you're currently in
- **See repo metadata** — description, stars, forks, license, languages, and more
- **See the top 5 contributors** to a repo, ranked by commits, with additions/deletions
- **Switch repos mid-session** without restarting the tool
- Colorized output that auto-disables when piped to a file or when `NO_COLOR` is set

## Requirements

- Python 3.x
- [PyGithub](https://pypi.org/project/PyGithub/)
- [colorama](https://pypi.org/project/colorama/)

## Installation

```
git clone https://github.com/JackMagee21/Gitviz.git
cd Gitviz
pip install PyGithub colorama
```

## Usage

Run the app and enter a repo as `author/repo_name` when prompted:

```
python main.py
```

```
Enter repo author and name with a slash (/) in between (e.g. name/repo_name), or press q to quit: torvalds/linux
torvalds/linux:/> ls
torvalds/linux:/> cd kernel
torvalds/linux:/kernel> log 5
torvalds/linux:/> summary
```

Type `q` at any prompt to quit.

## Commands

| Command | Usage | Description |
| --- | --- | --- |
| Help | `help [command]` | Shows this list, or details about one command |
| Info | `info` | Shows details about the current repo (description, stars, languages, etc.) |
| List | `ls [path]` | Lists files and folders in a directory (folders first, alphabetical) |
| Change directory | `cd [path]` | Changes directory; `cd` or `cd /` returns to the repo root, `cd ..` goes up one level |
| Log | `log [count]` | Shows the most recent commits for the current directory (default 10, max 100) |
| Summary | `summary` | Shows the top 5 contributors by commits, additions and deletions |
| Repo | `repo <author/name>` | Switches to browsing a different repo, e.g. `repo torvalds/linux` |
| Quit | `q` | Quits the application |

Run `help <command>` inside the app for details on any single command.

## Current Limitations

- Gitviz talks to the **unauthenticated** GitHub API, which is capped at 60 requests per hour — heavy browsing of a single repo can exhaust that quickly.
- `summary` and `log` are fetched live from GitHub each time, so results depend on GitHub's API availability and response time.
- On repos GitHub hasn't recently cached contributor stats for, `summary` may need a few seconds (and a retry) before data is ready.
- On repos with 10,000+ commits, GitHub's API stops returning addition/deletion counts; `summary` shows `N/A` for those columns rather than a misleading `0`. See [`cmds/summaryLimitations.md`](cmds/summaryLimitations.md) for details.

## Project structure

```
main.py                    REPL entry point
RepoData.py                RepoWrapper: wraps the PyGithub repo object + current path
cmds/
  cmd.py                   Command dispatcher
  help.py, info.py, ls.py, cd.py, logs.py, repo.py, summary.py
                            One module per command
utils/
  colors.py                Color helper (auto-disables outside a TTY / with NO_COLOR)
  formatting.py             Shared display helpers (dates, byte sizes)
  paths.py                  Resolves cd/ls/log paths against the current directory
```

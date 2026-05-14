# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal dotfiles/toolbelt repository containing shell configuration and Claude Code utilities. No build system, no tests, no package manager — changes are applied by symlinking or copying files to their target locations.

## Structure

- `shell/zshrc` — Zsh configuration. Symlink or copy to `~/.zshrc`. Reload with `source ~/.zshrc` or the `reload` alias.
- `shell/starship.toml` — Starship prompt configuration. Symlink or copy to `~/.config/starship.toml`.
- `statusline/statusline-command.sh` — Claude Code status line script. Reads JSON from stdin (Claude Code's hook payload), outputs a formatted string showing model name, context window usage %, and time until the 5-hour rolling token reset.

## Applying changes

```bash
# Reload zsh config after editing shell/zshrc
source ~/.zshrc

# Test the statusline script manually (requires a JSON payload on stdin)
echo '{"model":{"display_name":"Claude Sonnet"},"context_window":{"used_percentage":42}}' | bash statusline/statusline-command.sh
```

## Shell tooling in use

The zshrc assumes these are installed via Homebrew:

| Tool | Purpose |
|------|---------|
| `zsh-autosuggestions` | Fish-style inline suggestions; accept with `→` |
| `zsh-syntax-highlighting` | Real-time command highlighting (must source last) |
| `fzf` + `fd` | Fuzzy file/directory search |
| `zoxide` | Smart `cd` with frecency; use `z` / `zi` |
| `eza` | Modern `ls` replacement (aliased as `ls`, `ll`, `la`, `tree`) |
| `bat` | Syntax-highlighted `cat` (aliased as `cat`) |
| `delta` | Better git diff pager (set as `GIT_PAGER`) |
| `starship` | Cross-shell prompt |
| `fnm` | Node version manager (initialized at end of zshrc) |

## Key git aliases (defined in zshrc)

- `gcm "message"` — stages everything and commits
- `gpush` — pushes current branch to origin
- `gs`, `gd`, `gds`, `gl`, `gla` — status/diff/log shortcuts

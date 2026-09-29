# git-tidy

A Git commit message linter: parses, validates, and automatically fixes Git commit message format.

## Features

- Validates that commit messages follow the Conventional Commits spec
- Automatically fixes common format issues (missing type, casing, overlong lines)
- Usable as a pre-commit hook

## Installation

```bash
pip install git-tidy
```

## Usage

```bash
git-tidy check
git-tidy fix
git-tidy install-hook
```

## Configuration

The `[tool.git-tidy]` section in `pyproject.toml`:

```toml
[tool.git-tidy]
types = ["feat", "fix", "docs", "chore"]
max-line-length = 72
```

## License

MIT

---

> This project was developed by the team with the aid of AI tools; see [AI-USAGE.md](AI-USAGE.md) for the extent of AI involvement.

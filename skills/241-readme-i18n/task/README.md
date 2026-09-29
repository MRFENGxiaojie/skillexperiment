# pymo-cli

[![CI](https://img.shields.io/github/actions/workflow/status/example/pymo-cli/ci.yml)](https://github.com/example/pymo-cli)
[![npm version](https://img.shields.io/npm/v/pymo-cli)](https://www.npmjs.com/package/pymo-cli)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A command-line tool for managing Python project metadata and dependencies — inspect, pin, and upgrade packages across projects from one place.

## Features

- Fast dependency inspection with `pymo-cli inspect`
- Pin dependencies to exact versions
- Batch upgrade across multiple projects
- Works with `pyproject.toml`, `requirements.txt`, and `Pipfile`

## Installation

```bash
npm install -g pymo-cli
```

Requires Node.js 18+ and Python 3.9+.

See [Usage](#usage) for examples.

## Usage

Run `pymo-cli run --config config.yaml`.

Basic commands:

```bash
pymo-cli inspect --project ./my-project
pymo-cli pin --project ./my-project
pymo-cli upgrade --all
```

## Configuration

Create a `config.yaml` in your project root:

```yaml
project:
  name: my-project
  python: ">=3.9"
```

## License

MIT

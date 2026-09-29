# security-scan plugin

A hook script that runs after every file change, scanning changed files for sensitive information.

## Current state (v1 hardcoded config)

All config is hardcoded at the top of `hook-scan.sh`; switching projects means editing the script, which risks accidental commits. The plan is to refactor to a per-project config file (YAML) approach:

- `enabled`: whether enabled (boolean)
- `strict_mode`: strict mode, blocks the commit when sensitive info is found (boolean)
- `max_retries`: number of retries (number)
- `notification_level`: notification level, one of info / warn / error

## Plan

1. Create a new per-project config file (YAML, may include explanatory text)
2. The hook script reads the config before each run; uses defaults if missing
3. Config files must not be committed to git (add to .gitignore)
4. Provide a config template and README configuration docs

## Implementation Workflow

To add settings to a plugin:

1. Design settings schema (which fields, types, defaults)
2. Create template file in plugin documentation
3. Add gitignore entry for `.claude/*.local.md`
4. Implement settings parsing in hooks/commands
5. Use quick exit pattern (check file existence, check enabled field)
6. Document settings in plugin README with template
7. Remind users that changes require Claude Code restart

Focus on keeping settings simple and providing good defaults when configuration file does not exist.
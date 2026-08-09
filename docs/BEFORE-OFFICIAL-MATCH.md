# Before an official match

Replace the sample values in both `config/police/game.toml` and
`config/thief/game.toml`:

1. `group_name` and the unique eight-character `group_id`.
2. `members` with the real student identifiers.
3. `repos.cop` and `repos.thief` with the two submission repositories.
4. `mcp_servers` and `network.opponent_url` with the negotiated endpoints.
5. Confirm the private email settings; never commit OAuth credentials or tokens.

Before every match, compare both copies of `game.json` byte-for-byte. The opponent
must agree to any values that differ from the binding defaults. Record the actual
Git commit in the declaration and keep all four generated JSON artifact types.

## Local verification

Open two PowerShell terminals in the project directory:

```powershell
.\.venv\Scripts\python.exe -m police_thief peer --role police --stub-llm --no-gui
.\.venv\Scripts\python.exe -m police_thief peer --role thief --stub-llm --no-gui
```

For the GUI, omit `--no-gui`. The configured template provider uses no LLM and no
tokens. Official remote play requires each peer's public tunnel URL in the private
TOML and the matching MCP server declaration.

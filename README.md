# hdb - Hamradio Discord Bot

Discord bot for amateur radio (ham radio) related tools, including xOTA, DX Clusters, Propagation Forecast, etc.

The bot is being built incrementally. The initial version contains only the project structure
and functional module boundaries; Discord commands, external API clients, and persistence will follow
in later steps.

## Local Development

`hdb` uses the `uv` command for executing tests, linter and formatter.

## Discord Configuration

For local bot launches, create a `.env` file following the pattern of `.env.example`:

```text
DISCORD_TOKEN=your-bot-token
```
Tokens and other secrets are not committed.

## Planned Module Structure

- `hdb.json`: JSON parsing helpers.
- `hdb.storage`: Storage module supporting SQLite database.

## License

Copyright (c) 2026 Yannick Seibert.

This project is licensed under the MIT License. Details are in the file `LICENSE`.
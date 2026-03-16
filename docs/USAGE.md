# Usage Guide: AI-Assistant

## CLI Frontend
- Start the CLI and type your prompt.
- Change model: `:model gpt-oss-120b`, `:model zai-glm-4.7`, `:model qwen-3-235b`
- Change mode: `:mode low`, `:mode pro`, `:mode max`
- Change session: `:session <session_id>`
- Exit: `exit` or `quit`

## Backend
- Receives prompt, model, mode, and session_id from CLI
- Retrieves session context from Firestore
- Sends prompt to Cerebras API
- Updates session context in Firestore

## Project Structure
- `cli/` - Python CLI frontend
- `firebase/` - Node.js Firebase backend
- `docs/requirements.md` - Requirements
- `docs/USAGE.md` - This usage guide

## Improvements
- Syntax highlighting: Install `pygments` and integrate in CLI
- Command autocomplete: Use `prompt-toolkit` in CLI
- Multi-file project editing: Extend CLI/backend
- Local caching: Add cache logic in CLI

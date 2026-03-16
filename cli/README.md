# MIYO CODE CLI

## Features
- Termux-compatible Python CLI
- Typewriter effect for output
- Model and mode selection
- Session management
- Sends requests to Firebase backend

## Usage
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Run:
  ```sh
  python miyo_cli.py
  ```
- Change model: `:model gpt-oss-120b` or `:model zai-glm-4.7` or `:model qwen-3-235b`
- Change mode: `:mode low`, `:mode pro`, `:mode max`
- Change session: `:session <session_id>`
- Exit: `exit` or `quit`

## Environment Variables
- `FIREBASE_FUNCTION_URL` (optional): Override backend URL

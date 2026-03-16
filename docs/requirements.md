# Requirements for AI-Assistant Project

## 1. CLI Frontend (Python, Termux Compatible)
- Written in Python, runnable in Termux.
- Presents MIYO CODE UI:
  - Typewriter effect for output.
  - "Thinking..." status while waiting for backend.
- Reads user commands and sends them to Firebase backend.
- Supports model selection (gpt-oss-120b, zai-glm-4.7, qwen-3-235b).
- Supports mode selection (Low Effort / Pro / Max).
- Parses commands like `:run script.py`.
- Handles file/project management requests (read/write files, sync with Firestore).
- Optional: Syntax highlighting, command autocomplete, local caching.

## 2. Firebase Backend (Node.js)
- Firestore:
  - Stores user sessions, project context, memory, model preferences.
- Cloud Functions:
  - Accept CLI requests, forward to selected AI model API.
  - Handle mode logic (Low Effort / Pro / Max).
  - Sanitize and log terminal commands for safe execution.
  - Authentication (optional): per-user API key or login.
  - Use environment variable for Cerebras API key.
  - Store session context for each session_id.
  - Provide memory summaries to avoid exceeding token limits.

## 3. AI Model API
- Use Cerebras API (https://api.cerebras.net/v1/completions) for model calls.
- Backend acts as proxy to avoid exposing API keys in CLI.
- Use provided Cerebras API key: `csk-xehf29ke82khjwk9prwxy2dxrcddthexey6p25x9wtwc5fey` (store as env variable in backend).

## 4. Project Structure
- `/cli/` - Python CLI frontend code
- `/firebase/` - Node.js Firebase backend (functions, Firestore rules)
- `/docs/` - Documentation (including this requirements file)

## 5. Documentation
- README with setup instructions for both CLI and backend.
- Usage guide for all features.

## 6. Improvements (Optional)
- Multi-file project editing via CLI.
- Syntax highlighting in CLI (pygments).
- Command autocomplete (prompt-toolkit).
- Local caching in CLI.
- Tiered modes with different verbosity/creativity.

---

**Next Steps:**
- Scaffold `/cli/` and `/firebase/` directories.
- Implement CLI skeleton in Python.
- Implement Firebase function in Node.js.
- Add README instructions for setup and usage.

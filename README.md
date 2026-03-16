# AI-Assistant Project

## Overview
A terminal-based AI assistant with a Python CLI frontend (Termux compatible) and a Firebase backend proxying requests to Cerebras AI models.

---

## Setup Instructions

### 1. CLI Frontend (Python)
- Requirements: Python 3.7+, requests
- Install dependencies:
  ```sh
  pip install requests
  ```
- Run the CLI:
  ```sh
  python cli/miyo_cli.py
  ```
- Environment variable (optional):
  - `FIREBASE_FUNCTION_URL` (default: https://YOUR_PROJECT.cloudfunctions.net/miyo_request)

#### Usage
- Type your prompt and press Enter.
- Change model: `:model gpt-oss-120b` or `:model zai-glm-4.7` or `:model qwen-3-235b`
- Change mode: `:mode low`, `:mode pro`, `:mode max`
- Change session: `:session <session_id>`
- Exit: `exit` or `quit`

---

### 2. Firebase Backend (Node.js)
- Requirements: Node.js 18+, Firebase CLI
- Install dependencies:
  ```sh
  cd firebase
  npm install firebase-functions axios
  ```
- Deploy function:
  1. Set your Cerebras API key as an environment variable:
     ```sh
     export CEREBRAS_API_KEY=csk-xehf29ke82khjwk9prwxy2dxrcddthexey6p25x9wtwc5fey
     ```
  2. Deploy with Firebase CLI:
     ```sh
     firebase deploy --only functions
     ```

---

## Project Structure
- `cli/` - Python CLI frontend
- `firebase/` - Node.js Firebase backend
- `docs/requirements.md` - Project requirements

---

## Improvements (Optional)
- Syntax highlighting (pygments)
- Command autocomplete (prompt-toolkit)
- Multi-file project editing
- Local caching

---

## License
MIT
        "model": model,
        "mode": mode,
        "session_id": session_id
    }
    res = requests.post(FIREBASE_FUNCTION_URL, json=payload)
    return res.json()["response"]

def main():
    print("=== MIYO CODE CLI ===")
    while True:
        user_input = input("You> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        typewriter_print("MIYO CODE is thinking...\n")
        response = send_request(user_input)
        typewriter_print(response)

if __name__ == "__main__":
    main()
4️⃣ Firebase Function Example (Node.js)
JavaScript
Copy code
const functions = require("firebase-functions");
const axios = require("axios");

exports.miyo_request = functions.https.onRequest(async (req, res) => {
  const { prompt, model, mode, session_id } = req.body;

  // Build the master prompt for MIYO CODE here
  const systemPrompt = `You are MIYO CODE, a terminal AI assistant... Mode: ${mode}`;

  try {
    const aiRes = await axios.post("https://api.cerebras.net/v1/completions", {
      model,
      prompt: `${systemPrompt}\nUser: ${prompt}`,
      max_tokens: 1500
    }, {
      headers: { "Authorization": `Bearer ${process.env.CEREBRAS_API_KEY}` }
    });

    res.json({ response: aiRes.data.choices[0].text });
  } catch (err) {
    res.status(500).send({ error: err.message });
  }
});
Notes:
Use environment variable for your Cerebras API key in Firebase
Firestore can store session context for each session_id
CLI can request memory summaries to avoid exceeding token limits
5️⃣ Additional Improvements You Can Add
Multi-file project editing: store code files in Firestore and edit via CLI
Syntax highlighting using pygments in Termux
Command autocomplete using prompt-toolkit
Local caching to reduce repeated API calls
Tiered modes with different levels of verbosity and AI creativity. Make sure it will work on Termux, and also add a Readme instructions, make sure to use this Cerebras API key csk-xehf29ke82khjwk9prwxy2dxrcddthexey6p25x9wtwc5fey

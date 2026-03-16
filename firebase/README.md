# Firebase Backend for AI-Assistant

## Features
- Receives requests from CLI frontend
- Proxies requests to Cerebras AI models
- Stores session context in Firestore
- Supports multiple models and modes

## Setup
- Requirements: Node.js 18+, Firebase CLI
- Install dependencies:
  ```sh
  npm install
  ```
- Set Cerebras API key:
  ```sh
  export CEREBRAS_API_KEY=csk-xehf29ke82khjwk9prwxy2dxrcddthexey6p25x9wtwc5fey
  ```
- Deploy function:
  ```sh
  firebase deploy --only functions
  ```

## Firestore Rules
- See firestore.rules for open read/write (for demo/dev only)

## Files
- `index.js` - Main function handler
- `firestore.js` - Firestore session context helpers
- `firestore.rules` - Firestore security rules

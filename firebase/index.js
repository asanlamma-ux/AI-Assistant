const functions = require("firebase-functions");
const axios = require("axios");
const { saveSessionContext, getSessionContext } = require("./firestore");

// Use environment variable for Cerebras API key
const CEREBRAS_API_KEY = process.env.CEREBRAS_API_KEY || "csk-xehf29ke82khjwk9prwxy2dxrcddthexey6p25x9wtwc5fey";

exports.miyo_request = functions.https.onRequest(async (req, res) => {
  const { prompt, model, mode, session_id } = req.body;

  // Retrieve previous session context
  let prevContext = await getSessionContext(session_id);
  if (!prevContext) prevContext = "";

  // Build the master prompt for MIYO CODE
  const systemPrompt = `You are MIYO CODE, a terminal AI assistant. Mode: ${mode}`;
  const fullPrompt = `${systemPrompt}\nSession Context: ${prevContext}\nUser: ${prompt}`;

  try {
    const aiRes = await axios.post("https://api.cerebras.net/v1/completions", {
      model,
      prompt: fullPrompt,
      max_tokens: 1500
    }, {
      headers: { "Authorization": `Bearer ${CEREBRAS_API_KEY}` }
    });

    const aiText = aiRes.data.choices[0].text;
    // Save updated context (append latest prompt/response)
    const newContext = `${prevContext}\nUser: ${prompt}\nMIYO: ${aiText}`.slice(-4000); // keep last 4000 chars
    await saveSessionContext(session_id, newContext);

    res.json({ response: aiText });
  } catch (err) {
    res.status(500).send({ error: err.message });
  }
});

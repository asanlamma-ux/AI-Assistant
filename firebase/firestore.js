const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();

async function saveSessionContext(session_id, context) {
  await db.collection('sessions').doc(session_id).set({ context }, { merge: true });
}

async function getSessionContext(session_id) {
  const doc = await db.collection('sessions').doc(session_id).get();
  return doc.exists ? doc.data().context : null;
}

module.exports = { saveSessionContext, getSessionContext };

const API_BASE = '/api';

export async function sendMessage(
  message,
  sessionId = null,
  provider = null,
  format = 'graphviz',
  visionFeedback = true,
) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      provider,
      format,
      vision_feedback: visionFeedback,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export async function exportDiagram(sessionId, format = 'png') {
  const res = await fetch(`${API_BASE}/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, format }),
  });
  if (!res.ok) throw new Error('Export failed');
  const blob = await res.blob();
  return blob;
}

export async function resetSession(sessionId) {
  await fetch(`${API_BASE}/reset?session_id=${sessionId}`, { method: 'POST' });
}

export async function getConfig() {
  const res = await fetch(`${API_BASE}/config`);
  return res.json();
}

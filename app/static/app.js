async function summarize(e) {
  e.preventDefault();
  const form = document.getElementById('sumForm');
  const prompt = document.getElementById('prompt').value.trim();
  const text = document.getElementById('text').value.trim();
  const fileInput = document.getElementById('file');

  const fd = new FormData();
  fd.append('prompt', prompt);
  if (text) fd.append('text', text);
  if (fileInput.files.length) fd.append('file', fileInput.files[0]);

  const res = await fetch('/api/summarize', { method: 'POST', body: fd });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    alert('Failed: ' + (err.detail || res.status));
    return;
  }
  const data = await res.json();
  document.getElementById('summary').value = data.summary;
}

async function share(e) {
  e.preventDefault();
  const summary = document.getElementById('summary').value.trim();
  const raw = document.getElementById('recipients').value;
  const recipients = raw.split(',').map(s => s.trim()).filter(Boolean);
  const status = document.getElementById('status');
  status.textContent = 'Sending...';

  const res = await fetch('/api/share', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ summary, recipients }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    status.textContent = 'Failed: ' + (err.detail || res.status);
    return;
  }
  status.textContent = 'Email sent!';
}

document.getElementById('sumForm').addEventListener('submit', summarize);
document.getElementById('shareForm').addEventListener('submit', share);

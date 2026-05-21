// ── API helpers ──────────────────────────────────────────────────
async function api(url) {
  try {
    const res = await fetch(url);
    return await res.json();
  } catch (e) {
    toast('Erro ao conectar com o servidor.', 'erro');
    return {};
  }
}

async function apiPost(url, dados, method = 'POST') {
  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados),
    });
    return await res.json();
  } catch (e) {
    toast('Erro ao conectar com o servidor.', 'erro');
    return { erro: 'Erro de conexão' };
  }
}

// ── Toast ─────────────────────────────────────────────────────────
let toastTimer;
function toast(msg, tipo = 'ok') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast' + (tipo === 'erro' ? ' erro' : '');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add('hidden'), 3000);
}

/* ══════════════════════════════════
   EDUVERSE — MAIN JS
   ══════════════════════════════════ */

// ── Sidebar / Mobile ──────────────────────────
const sidebar   = document.getElementById('sidebar');
const hamburger = document.getElementById('hamburger');
const overlay   = document.getElementById('overlay');

hamburger?.addEventListener('click', () => {
  sidebar.classList.toggle('mobile-open');
  overlay.classList.toggle('show');
});
overlay?.addEventListener('click', () => {
  sidebar.classList.remove('mobile-open');
  chatWindow.classList.remove('open');
  overlay.classList.remove('show');
});

// ── Chat Widget ───────────────────────────────
const chatFab     = document.getElementById('chatFab');
const chatWindow  = document.getElementById('chatWindow');
const chatClose   = document.getElementById('chatClose');
const chatInput   = document.getElementById('chatInput');
const chatSend    = document.getElementById('chatSend');
const chatMessages= document.getElementById('chatMessages');

chatFab?.addEventListener('click', () => {
  const open = chatWindow.classList.toggle('open');
  if (open) overlay.classList.add('show');
  else overlay.classList.remove('show');
});
chatClose?.addEventListener('click', () => {
  chatWindow.classList.remove('open');
  overlay.classList.remove('show');
});

async function sendChat() {
  const msg = chatInput.value.trim();
  if (!msg) return;
  chatInput.value = '';

  appendMsg(msg, 'user');
  appendTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    removeTyping();
    appendMsg(data.reply, 'bot', data.time);
  } catch {
    removeTyping();
    appendMsg('Sorry, something went wrong. Please try again.', 'bot');
  }
}

function appendMsg(text, who, time) {
  const now = time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const div = document.createElement('div');
  div.className = `chat-msg ${who}`;
  div.innerHTML = `<span class="msg-bubble">${text}</span><span class="msg-time">${now}</span>`;
  div.style.animation = 'fadeUp 0.3s ease';
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendTyping() {
  const div = document.createElement('div');
  div.className = 'chat-msg bot';
  div.id = 'typingIndicator';
  div.innerHTML = `<span class="msg-bubble" style="display:flex;gap:4px;padding:12px 16px;">
    <span class="dot" style="width:7px;height:7px;background:var(--text3);border-radius:50%;animation:bounce 1s 0s infinite"></span>
    <span class="dot" style="width:7px;height:7px;background:var(--text3);border-radius:50%;animation:bounce 1s 0.2s infinite"></span>
    <span class="dot" style="width:7px;height:7px;background:var(--text3);border-radius:50%;animation:bounce 1s 0.4s infinite"></span>
  </span>`;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  const style = document.createElement('style');
  style.textContent = `@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}`;
  document.head.appendChild(style);
}
function removeTyping() {
  document.getElementById('typingIndicator')?.remove();
}

chatSend?.addEventListener('click', sendChat);
chatInput?.addEventListener('keypress', e => { if (e.key === 'Enter') sendChat(); });

// ── Animate progress bars on load ─────────────
document.addEventListener('DOMContentLoaded', () => {
  const fills = document.querySelectorAll('.progress-fill[data-width]');
  setTimeout(() => {
    fills.forEach(el => {
      el.style.width = el.dataset.width + '%';
    });
  }, 300);
});

// ── Filter Tabs ───────────────────────────────
document.querySelectorAll('.filter-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const group = tab.closest('.filter-tabs');
    group.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');

    const filter = tab.dataset.filter;
    const target = tab.closest('section')?.querySelector('[data-filterable]')
                || document.querySelector('[data-filterable]');
    if (!target) return;

    target.querySelectorAll('[data-category]').forEach(item => {
      const show = filter === 'all' || item.dataset.category === filter;
      item.style.display = show ? '' : 'none';
    });
  });
});

// ── Search ────────────────────────────────────
const searchInput = document.getElementById('searchInput');
searchInput?.addEventListener('input', () => {
  const q = searchInput.value.toLowerCase();
  document.querySelectorAll('[data-searchable]').forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(q) ? '' : 'none';
  });
});


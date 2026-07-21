document.addEventListener('DOMContentLoaded', function () {
  const launcher = document.getElementById('chat-launcher');
  const panel = document.getElementById('chat-panel');
  const closeBtn = document.getElementById('chat-close');
  const log = document.getElementById('chat-log');
  const form = document.getElementById('chat-form');
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');

  let opened = false;
  let history = [];

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  function addMessage(text, role) {
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
    return div;
  }

  function openPanel() {
    panel.classList.add('open');
    if (!opened) {
      opened = true;
      addMessage("Assalam-o-Alaikum! I'm here to help with fabric, sizing, or your order. What would you like to know?", 'bot');
    }
    input.focus();
  }

  launcher.addEventListener('click', openPanel);
  closeBtn.addEventListener('click', () => panel.classList.remove('open'));

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    input.value = '';
    sendBtn.disabled = true;
    const typingEl = addMessage('typing…', 'bot typing');

    try {
      const resp = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ message: text, history: history }),
      });
      const data = await resp.json();
      typingEl.remove();
      const reply = data.reply || "Sorry, something went wrong.";
      addMessage(reply, 'bot');
      history.push({ role: 'user', content: text });
      history.push({ role: 'assistant', content: reply });
    } catch (err) {
      typingEl.remove();
      addMessage("Couldn't reach support right now. Please try again.", 'bot');
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  });
});

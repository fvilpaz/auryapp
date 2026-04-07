/* ── TEMAS ── */
var THEMES = [
  { id: 'light',     name: 'Claro',     emoji: '☀️', group: 'light' },
  { id: 'mint',      name: 'Mint',      emoji: '🌿', group: 'light' },
  { id: 'barbie',    name: 'Barbie',    emoji: '💗', group: 'light' },
  { id: 'dark',      name: 'Oscuro',    emoji: '🌙', group: 'dark'  },
  { id: 'dracula',   name: 'Drácula',   emoji: '🧛', group: 'dark'  },
  { id: 'cyberpunk', name: 'Cyberpunk', emoji: '⚡', group: 'dark'  },
];

var AppTheme = { initialized: false };

function applyTheme(themeId) {
  document.documentElement.setAttribute('data-theme', themeId);
  localStorage.setItem('bc-theme', themeId);
  document.querySelectorAll('.theme-chip').forEach(function(chip) {
    chip.classList.toggle('active', chip.dataset.theme === themeId);
  });
  if (AppTheme.initialized) {
    setTimeout(closePanel, 350);
  }
  AppTheme.initialized = true;
}

function openPanel() {
  var p = document.getElementById('theme-panel');
  if (!p) return;
  p.style.display = 'block';
  void p.offsetWidth;
  p.classList.add('open');
}

function closePanel() {
  var p = document.getElementById('theme-panel');
  if (!p) return;
  p.classList.remove('open');
  setTimeout(function() {
    if (!p.classList.contains('open')) p.style.display = 'none';
  }, 400);
}

function buildThemePanel() {
  if (document.getElementById('theme-panel')) return;
  var panel = document.createElement('div');
  panel.id = 'theme-panel';
  panel.innerHTML = `
    <div id="theme-panel-overlay"></div>
    <div id="theme-panel-drawer">
      <div id="theme-panel-header">
        <span>🎨 Personalización</span>
        <button id="theme-panel-close" type="button">✕</button>
      </div>
      <div class="theme-group-label">Claros</div>
      <div class="theme-chips" id="theme-chips-light"></div>
      <div class="theme-group-label">Oscuros</div>
      <div class="theme-chips" id="theme-chips-dark"></div>
    </div>
  `;
  document.body.appendChild(panel);

  var saved = localStorage.getItem('bc-theme') || 'light';
  THEMES.forEach(function(theme) {
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'theme-chip';
    chip.dataset.theme = theme.id;
    if (theme.id === saved) chip.classList.add('active');
    chip.innerHTML = `
      <span class="chip-emoji">${theme.emoji}</span>
      <span class="chip-name">${theme.name}</span>
    `;
    chip.onclick = function() { applyTheme(theme.id); };
    var target = document.getElementById('theme-chips-' + theme.group);
    if (target) target.appendChild(chip);
  });

  document.getElementById('theme-panel-close').onclick = closePanel;
  document.getElementById('theme-panel-overlay').onclick = closePanel;
}

document.addEventListener('DOMContentLoaded', function() {
  var saved = localStorage.getItem('bc-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
  buildThemePanel();

  var calendarEl = document.getElementById('calendario');
  if (!calendarEl) return;

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'es',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,listMonth'
    },
    events: window.BC.urls.eventos_json,
    eventClick: function(info) {
      info.jsEvent.preventDefault();
      window.location.href = info.event.url;
    },
    height: 'auto',
  });
  calendar.render();

  var toolbar = calendarEl.querySelector('.fc-toolbar');
  var placeholder = document.getElementById('fc-toolbar-placeholder');
  if (toolbar && placeholder) {
    placeholder.appendChild(toolbar);
  }
});
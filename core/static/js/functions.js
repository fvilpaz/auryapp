/* ── TEMAS ── */
var THEMES = [
  { id: 'light',     name: 'Claro',     emoji: '☀️', group: 'light' },
  { id: 'mint',      name: 'Mint',      emoji: '🌿', group: 'light' },
  { id: 'barbie',    name: 'Barbie',    emoji: '💗', group: 'light' },
  { id: 'dark',      name: 'Oscuro',    emoji: '🌙', group: 'dark'  },
  { id: 'dracula',   name: 'Drácula',   emoji: '🧛', group: 'dark'  },
  { id: 'cyberpunk', name: 'Cyberpunk', emoji: '⚡', group: 'dark'  },
];

function applyTheme(themeId) {
  document.documentElement.setAttribute('data-theme', themeId);
  localStorage.setItem('bc-theme', themeId);
  document.querySelectorAll('.theme-chip').forEach(function(chip) {
    chip.classList.toggle('active', chip.dataset.theme === themeId);
  });
}

/* ── MENÚ DE USUARIO (dropdown GNOME-style) ── */
function buildUserMenu() {
  var container = document.getElementById('bc-user-theme-chips');
  if (!container) return;

  var saved = localStorage.getItem('bc-theme') || 'light';

  THEMES.forEach(function(theme) {
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'theme-chip' + (theme.id === saved ? ' active' : '');
    chip.dataset.theme = theme.id;
    chip.title = theme.name;
    chip.innerHTML = '<span class="chip-emoji">' + theme.emoji + '</span>'
                   + '<span class="chip-name">' + theme.name + '</span>';
    chip.onclick = function() { applyTheme(theme.id); };
    container.appendChild(chip);
  });

  var btn = document.getElementById('bc-user-menu-btn');
  var dropdown = document.getElementById('bc-user-menu-dropdown');
  if (!btn || !dropdown) return;

  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    var open = dropdown.classList.toggle('open');
    btn.classList.toggle('active', open);
  });

  document.addEventListener('click', function(e) {
    if (!dropdown.contains(e.target) && e.target !== btn) {
      dropdown.classList.remove('open');
      btn.classList.remove('active');
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  var saved = localStorage.getItem('bc-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
  buildUserMenu();

  var calendarEl = document.getElementById('calendario');
  if (!calendarEl) return;

  // Popover
  var popover = document.createElement('div');
  popover.id = 'cal-popover';
  popover.style.cssText = [
    'position:fixed',
    'background:var(--color-surface)',
    'border:0.5px solid var(--color-border)',
    'border-radius:var(--radius-lg)',
    'box-shadow:0 8px 24px rgba(0,0,0,0.15)',
    'padding:8px',
    'z-index:500',
    'display:none',
    'flex-direction:column',
    'gap:4px',
    'min-width:180px',
  ].join(';');
  document.body.appendChild(popover);

  function closePopover() {
    popover.style.display = 'none';
  }

  document.addEventListener('click', function(e) {
    if (!popover.contains(e.target)) closePopover();
  });

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
    dateClick: function(info) {
      info.jsEvent.stopPropagation();
      var fecha = info.dateStr;
      popover.innerHTML = [
        '<div style="font-size:11px;font-weight:600;color:var(--color-muted);',
        'text-transform:uppercase;letter-spacing:0.08em;padding:4px 8px 8px;">',
        info.date.toLocaleDateString("es-ES", {day:"numeric", month:"long"}),
        '</div>',
        '<a href="/eventos/nuevo/?fecha=' + fecha + '" ',
        'style="display:flex;align-items:center;gap:8px;padding:8px 10px;',
        'border-radius:var(--radius-sm);text-decoration:none;color:var(--color-text);',
        'font-size:13px;transition:background 0.1s;" ',
        'onmouseover="this.style.background=\'rgba(26,111,196,0.08)\'" ',
        'onmouseout="this.style.background=\'\'">',
        '<i class="ti ti-calendar-event" style="color:var(--color-primary)"></i> Nuevo evento',
        '</a>',
        '<a href="/agenda/?nota=' + fecha + '" ',
        'style="display:flex;align-items:center;gap:8px;padding:8px 10px;',
        'border-radius:var(--radius-sm);text-decoration:none;color:var(--color-text);',
        'font-size:13px;transition:background 0.1s;" ',
        'onmouseover="this.style.background=\'rgba(26,111,196,0.08)\'" ',
        'onmouseout="this.style.background=\'\'">',
        '<i class="ti ti-notebook" style="color:var(--color-primary)"></i> Nueva nota',
        '</a>',
      ].join('');

      var x = info.jsEvent.clientX;
      var y = info.jsEvent.clientY;
      popover.style.display = 'flex';
      var pw = popover.offsetWidth;
      var ph = popover.offsetHeight;
      if (x + pw + 8 > window.innerWidth) x = x - pw;
      if (y + ph + 8 > window.innerHeight) y = y - ph;
      popover.style.left = x + 'px';
      popover.style.top = y + 'px';
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

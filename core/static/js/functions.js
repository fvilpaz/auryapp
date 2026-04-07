document.addEventListener('DOMContentLoaded', function() {
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
});

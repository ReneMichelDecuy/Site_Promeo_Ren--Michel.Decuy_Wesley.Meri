$(document).ready(function() {
  $('#calendar').fullCalendar({
      header: {
          left: 'prev,next today',
          center: 'title',
          right: 'month,agendaWeek,agendaDay'
      },
      defaultView: 'agendaWeek',
      locale: 'fr', // Définir la langue en français
      editable: false,
      events: [
          {
              title: 'COMP 455',
              start: '2016-09-20T11:15:00',
              end: '2016-09-20T12:05:00',
              color: '#8dc3f9'
          },
          {
              title: 'COMP 410',
              start: '2016-09-20T14:00:00',
              end: '2016-09-20T15:15:00',
              color: '#8dc3f9'
          },
          // Ajoutez plus d'événements ici
      ]
  });
});

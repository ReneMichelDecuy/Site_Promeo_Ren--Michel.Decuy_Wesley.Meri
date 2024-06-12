$(document).ready(function() {
    var selectedEvent;

    moment.locale('fr'); // Définit la locale sur "fr"

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'agendaWeek,agendaDay'
        },
        defaultView: 'agendaWeek',
        selectable: true,
        selectHelper: true,
        slotLabelFormat: 'H:mm', // Format des heures sur les côtés
        firstDay: 1, // Premier jour de la semaine (lundi)
        weekends: false, // Masquer les week-ends
        minTime: '07:00:00', // Début du calendrier à 7h
        select: function(start, end) {
            var date = start.format('YYYY-MM-DD');
            $('#date').val(date);
            $('#addEventModal').modal('show');
        },
        eventClick: function(event) {
            selectedEvent = event;
            $('#deleteEventModal').modal('show');
        },
        events: '/api/rendezvous',
        height: 'auto',
        lang: 'fr' // Définit la langue sur "fr"
    });

    $('#addEventForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/ajouter_rendezvous',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('#addEventModal').modal('hide');
                $('#calendar').fullCalendar('refetchEvents');
            },
            error: function(error) {
                alert('Erreur lors de l\'ajout du rendez-vous');
            }
        });
    });

    $('#deleteEventBtn').click(function() {
        // Récupérer les données du rendez-vous
        var date = selectedEvent.start.format('YYYY-MM-DD');
        var heure = selectedEvent.start.format('HH:mm:ss');
        var nom = selectedEvent.title;

        // Envoyer une requête AJAX avec les données nécessaires
        $.ajax({
            url: '/supprimer_rendezvous',
            method: 'POST',
            data: {
                date: date,
                heure: heure,
                nom: nom
            },
            success: function(response) {
                $('#deleteEventModal').modal('hide');
                $('#calendar').fullCalendar('removeEvents', selectedEvent._id);
            },
            error: function(error) {
                alert('Erreur lors de la suppression du rendez-vous');
            }
        });
    });

});
function filterUsers() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("usersTable");
    tr = table.getElementsByTagName("tr");

    // Si le champ de recherche est vide, cacher le tableau
    if (filter === "") {
        table.style.display = "none";
    } else {
        table.style.display = "table";  // Afficher le tableau quand il y a du texte
    }

    for (i = 1; i < tr.length; i++) {  // Start at 1 to skip the table header
        td = tr[i].getElementsByTagName("td")[0];  // Get the first column (Prénom)
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// Appeler filterUsers pour s'assurer que le tableau est caché au chargement de la page si le champ de recherche est vide
document.addEventListener("DOMContentLoaded", function() {
    filterUsers();
});

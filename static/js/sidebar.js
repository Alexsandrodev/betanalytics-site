document.addEventListener("DOMContentLoaded", function() {
    const userMenuToggle = document.getElementById("user-menu-toggle");
    const userSidebar = document.getElementById("user-sidebar");

    userMenuToggle.addEventListener("click", function(event) {
        event.stopPropagation(); // Evita que o clique feche imediatamente
        userSidebar.classList.toggle("open");
    });

    // Permite que a sidebar continue aberta enquanto o usuário interage com ela
    userSidebar.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    // Fecha o menu ao clicar fora dele
    document.addEventListener("click", function(event) {
        if (!userSidebar.contains(event.target) && !userMenuToggle.contains(event.target)) {
            userSidebar.classList.remove("open");
        }
    });
});
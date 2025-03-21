let currentCompeticao = "britishDerbies";
let lastHtml = "";

const nameCompetitions = {
  britishDerbies: "British Derbies",
  copaDasEstrelas: "Copa das Estrelas",
  copaAmerica: "Copa América",
  tacaGloriaEterna: "Taça Glória Eterna",
  euro: "Euro Copa",
  ligaEspanhola: "Liga Espanhola",
  campeonatoItaliano: "Campeonato Italiano",
  scudettoItaliano: "Scudetto Italiano",
};

function normalizeHTML(html) {
  return html.replace(/\s+/g, " ").trim();
}

function getCSRFToken() {
  let cookieValue = null;
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith("csrftoken=")) {
          cookieValue = cookie.substring("csrftoken=".length, cookie.length);
          break;
      }
  }
  return cookieValue;
}

function refreshPercentages() {
  let greenElement = document.getElementById("porcentagem_green");
  let redElement = document.getElementById("porcentagem_red");

  if (greenElement && redElement) {
    let green = greenElement.textContent.trim();
    let red = redElement.textContent.trim();

    document.getElementById("green").textContent = green;
    document.getElementById("red").textContent = red;
  } else {
    console.warn("Elementos de porcentagem ainda não carregados.");
  }
}

function setTitle() {
  document.getElementById("competicao").textContent =
    nameCompetitions[currentCompeticao] || "Competição Desconhecida";
}

function refreshData(competicao = null) {
    if (competicao) {
        currentCompeticao = competicao;
        setTitle();
    }

    const filters = {
      hours: document.getElementById('hours').value,
      both: document.getElementById('both').value || null,
      matchResult: document.getElementById('matchResult').value,
      evenOddGoals: document.getElementById('evenOddGoals').value || null,
      overGoals: document.getElementById('overGoals').value || null,
      underGoals: document.getElementById('underGoals').value || null,
      turn: document.getElementById('turn').value || null,
      correctResult: document.getElementById('correctResult').value || null
    }

    $.ajax({
        url: `/betano/horarios/tabela?competicao=${currentCompeticao}`,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken() 
      },
        data: JSON.stringify(filters),

        success: function (response) {
            if (response.status === "updated") {
                if (lastHtml != response.html){
                  console.log("🔄 Dados diferentes! Atualizando...");
                  $(".tabela").empty().html(response.html);
                  
                  refreshPercentages();

                  updateTooltips();
                  lastHtml = response.html
                }
                
            } else {
                console.log("✅ Nenhuma mudança detectada.");
            }
        }
    });
}

function updateTooltips() {
    $('.tooltip').each(function() {
        $(this).text($(this).text().replace(/-/g, 'X'));
    });
}

document.addEventListener("DOMContentLoaded", function() {
  setTitle();
  const selects = document.querySelectorAll("select");
  selects.forEach(select => {
    select.addEventListener("change", () => refreshData);
  });
});

setInterval(() => refreshData(), 1000);

def apply_filter(result, filters):
    """
    Aplica múltiplos filtros aos resultados e retorna 'green' se todos forem verdadeiros, 
    e 'red' se pelo menos um for falso.

    :param result: Dados do jogo (ex. resultados das equipes)
    :param filters: Dicionário com os filtros ativados (extraído do formulário)
    :return: 'green' ou 'red'
    """
    
    
    if not result:
        return "#0c0c0c"  # Se não houver resultado, retorna vermelho.

    if filters.get("both") == None and filters.get("evenOddGoals") == None and filters.get("overGoals") == None and filters.get("underGoals") == None:
        return "gray"

    try:
        # 🏆 Número de gols no jogo
        goalsTotal, goalsA, goalsB = getGoals(result)
        color_filter = ''

        # 📌 Filtro 1: Ambas Marcaram (SIM/Não)
        if filters.get("both") == "bothYes":
            if not (goalsA > 0 and goalsB > 0):
                color_filter = "red"
        elif filters.get("both") == "bothNo":
            if goalsA > 0 and goalsB > 0:
                color_filter = "red"


        # 📌 Filtro 2: Gols PAR/ÍMPAR
        if filters.get("evenOddGoals") == "even":
            if goalsTotal % 2 != 0:  # Se for ímpar, retorna vermelho.
                color_filter = "red"
        elif filters.get("evenOddGoals") == "odd":
            if goalsTotal % 2 == 0:  # Se for par, retorna vermelho.
                color_filter = "red"

        # 📌 Filtro 3: Over Gols
        if filters.get("overGoals"):
            over_value = float(filters["overGoals"].split("_")[1])  # Ex: 'over_1.5' vira '1.5'
            if goalsTotal <= over_value:
                color_filter = "red"

        # 📌 Filtro 4: Under Gols
        if filters.get("underGoals"):
            under_value = float(filters["underGoals"].split("_")[1])  # Ex: 'under_1.5' vira '1.5'
            if goalsTotal >= under_value:
                color_filter = "red"

        # 📌 Filtro 5: Virada
        # if filters.get("turn") == "turnYes":
        #     if not (result["team1_goals_first_half"] < result["team2_goals_first_half"] and 
        #             result["team1_goals"] > result["team2_goals"]):
        #         color_filter = "red"
        # elif filters.get("turn") == "turnNo":
        #     if result["team1_goals_first_half"] < result["team2_goals_first_half"] and \
        #        result["team1_goals"] > result["team2_goals"]:
        #         color_filter = "red"

        # 📌 Filtro 6: Resultado Correto
        # if filters.get("correctResult"):
        #     expected_result = filters["correctResult"]
        #     actual_result = f"{result['team1_goals']}x{result['team2_goals']}"
        #     if actual_result != expected_result:
        #         color_filter = "red"

        if color_filter == 'red':
            return 'red'
        
        return 'green'

    except ValueError:
        return "red"  # Caso haja erro ao processar os dados.

def getGoals(gols):
    if not gols or ' - ' not in gols:
        return 0, 0, 0
    
    goalsA , goalsB = gols.split(' - ')
    goalsA = int(goalsA)
    goalsB = int(goalsB)
    
    soma = goalsA + goalsB
    
    return soma, goalsA, goalsB



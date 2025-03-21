import requests
from django.core.cache import cache
from myapp.utils.cacheHelper import get_cached_response
from myapp.utils.filterUtils import apply_filter, getGoals
import httpx

async def fetchApiData(competition):
    """ Fetch data from the FastAPI service asynchronously. """
    url = f"http://127.0.0.1:3000/scrape/{competition}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


def processData(data, filters):
    """ Process the data, calculate statistics, and apply filters. """


    rows = dict(sorted(data["Linhas"].items(), key=lambda item: int(item[0]), reverse=True))
    hours = sorted(rows.keys(), key=int)
    second_last_hour = hours[-2]
    minutes = sorted([item['Minuto'] for item in rows[second_last_hour]])

    columns_data = {i: {"total": 0, "green": 0} for i in range(20)}
    total_greens = total_reds = 0

    for hour, matches in rows.items():
        total_hour = hour_green = 0
        for idx, match in enumerate(matches[:20]):
            if filters.get('match_result') == "ht":  
                result = match.get('Resultado_HT', '')
                match["Resultado"] = match.get("Resultado_HT", '')
            else:
                result = match.get('Resultado', '')
            
            if not match.get("Resultado"):
                match["Resultado"] = "X"
            
            match['color_result'] = apply_filter(result, filters)
            golstotal, goalsA, goalsB = getGoals(result)
            match["goals"] = golstotal

            total_hour += 1
            minute = match.get("Minuto")

            if idx not in columns_data:
                columns_data[idx] = {"total": 0, "green": 0}

            columns_data[idx]["total"] += 1    
            if match['color_result'] == 'green':
                hour_green += 1
                total_greens += 1
                columns_data[idx]["green"] += 1
            else:
                total_reds += 1

        total_goals = sum(match["goals"] for match in matches)

        while len(matches) < 20:
            matches.append({"Resultado": "", "goals": 0})

        green_hour = int((hour_green / total_hour) * 100) if total_hour > 0 else 0
        matches.append({"hour_green": green_hour})
        matches.append({"total_goals": total_goals})  

    total_results = total_greens + total_reds
    percentages = {
        "green_percentage": f"{(total_greens / total_results) * 100:.2f}" if total_results > 0 else "0.00",
        "red_percentage": f"{(total_reds / total_results) * 100:.2f}" if total_results > 0 else "0.00",
    }

    for idx, data in columns_data.items():
        data["percent_green"] = int((data["green"] / data["total"]) * 100) if data["total"] > 0 else 0  

    return {
        'linhas': rows,
        'minutos': minutes,
        'colunas_data': columns_data,
        "porcentagens": percentages
    }
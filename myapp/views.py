from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.cache import cache

from myapp.services.tableServices import fetchApiData, processData
from myapp.utils.cacheHelper import get_cached_response

import requests
import json
import time
import asyncio


@login_required
def base(request):
    return redirect('betano')

@login_required
def betano(request):
    return render(request, 'betano/inicio_bet.html')

@login_required
def horarios_betano(request): 

    return render(request, 'betano/horarios_bet.html')
    
@csrf_protect
async def tabela(request):
    ALLOWED_ORIGIN = "http://127.0.0.1:8000"
    referer = request.META.get("HTTP_REFERER", "")
    origin = request.META.get("HTTP_ORIGIN", "")

    if not (referer.startswith(ALLOWED_ORIGIN) or origin == ALLOWED_ORIGIN):
        return redirect("horarios_betano")

    competition = request.GET.get("competicao", "britishDerbies")
    
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"Error": "Invalid JSON"}, status=404)

        filters = {
            "hours": body.get("hours"),
            "both": body.get("both"),
            "match_result": body.get("matchResult"),
            "evenOddGoals": body.get("evenOddGoals"),
            "overGoals": body.get("overGoals"),
            "underGoals": body.get("underGoals"),
            "turn": body.get("turn"),
            "correctResult": body.get("correctResult"),
        }

    data = await fetchApiData(competition)
    context = processData(data, filters)
 
    novo_html = render(request, "betano/tabela.html", context).content.decode("utf-8")

    return JsonResponse({"status": "updated", "html": novo_html}, status=200)


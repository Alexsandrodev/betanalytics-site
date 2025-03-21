from django.core.cache import cache
from django.shortcuts import render

def get_cached_response(request, cache_key, context):
    """Check if the generated HTML is cached to avoid unnecessary updates."""
    last_html = cache.get(cache_key, "")

    new_html = render(request, "betano/table.html", context).content.decode("utf-8")

    if new_html == last_html:
        return {"status": "unchanged"}, 304  # No changes

    cache.set(cache_key, new_html, timeout=60)  # Update cache
    return {"status": "updated", "html": new_html}, 200
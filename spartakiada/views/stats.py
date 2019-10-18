from django.shortcuts import redirect, render
from django.views import View
from spartakiada.cron import make_players_cache
from spartakiada.models import PlayerCache

class Stats(View):
    
    def get(self, request):
        cache = PlayerCache.objects.all()
        ctx = {
            'cache': cache,
        }
        return render(request, 'spartakiada/stats.html', ctx)


def refresh_stats(request):
    """
    For an unknown reason kronos is not willing to cooperate with us,
    so here is a possibility to refresh statistic table on click.
    """
    make_players_cache()
    return redirect('/stats/')
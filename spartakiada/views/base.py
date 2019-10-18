from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from spartakiada.models import Cup
from .player import *
from .team import *

class BaseView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)

class AboutView(View):

    def get(self, request):
        return render(request, 'spartakiada/about_view.html')

# main page
class MenuView(View):

    def get(self, request):
        cup = Cup.objects.all().order_by("-date")
        players = best_players()
        teams = best_teams()
        ctx = {
            'cup': cup,
            'players': players,
            'teams': teams
        }
        return render(request, 'spartakiada/menu.html', ctx)
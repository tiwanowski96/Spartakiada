from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from spartakiada.models import Game

class GamesView(View):
    
    def get(self, request):
        game_list = Game.objects.all().order_by('name')
        ctx = {
            'game_list': game_list
        }
        return render(request, 'spartakiada/game_view.html', ctx)


class GameAddView(CreateView):
    model = Game
    fields = [
        'name'
    ]
    success_url = '/games/'


class GamesDeleteView(View):

    def get(self, request):
        game_list = Game.objects.all().order_by('name')
        ctx = {
            'game_list': game_list,
        }
        return render(request, 'spartakiada/games_delete_view.html', ctx)

    def post(self, request):
        for i in request.POST.getlist('game'):
            game = Game.objects.filter(name=i)
            game.delete()
        return redirect('/games/')
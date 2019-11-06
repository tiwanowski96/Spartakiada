from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, TemplateView
from spartakiada.models import Partaker, Player, PlayerCache

def reverse_name(name):
    return " ".join(name.split(" ")[::-1])

def players_alphabetically():
    """
    We chose to have our players names in one word to satisfy the needs of those, who prefer to
    be seen by nickname and also those, who decided to give us their full name.
    Due to this fact to sort them in alphabetic order we need a separate function.
    """
    players = Player.objects.all()
    players_list = []
    for player in players:
        players_list.append(reverse_name(player.name))
    if "Random" in players_list:
        players_list.remove('Random')
    players_list.sort()
    # getting players back to proper name form
    players_list = [reverse_name(player) for player in players_list]
    # making a set of query sets again
    players_list = [Player.objects.get(name=player) for player in players_list]
    return players_list


def best_players():
    all = PlayerCache.objects.all().order_by("-tournament_won")
    players = []
    for player in all:
        if player.partaker.player:
            players.append(player)
    return players


class PlayersView(TemplateView):
    template_name = 'spartakiada/player_view.html'

    def get_context_data(self, **kwargs):
        ctx = super(PlayersView, self).get_context_data()
        ctx['players'] = players_alphabetically()
        return ctx


    # def get(self, request):
    #     players = players_alphabetically()
    #     ctx = {
    #         'players': players
    #     }
    #     return render(request, 'spartakiada/player_view.html', ctx)


class PlayerAddView(CreateView):
    model = Player
    fields = [
        'name'
    ]
    success_url = '/add_player/'


    # we want to have a list of already existing players on the side, so we need some extra ctx
    def get_context_data(self, **kwargs):
        ctx = super(PlayerAddView, self).get_context_data(**kwargs)
        players = players_alphabetically()
        ctx['players'] = players
        return ctx


class PlayerDeleteView(View):

    def get(self, request):
        players = players_alphabetically()
        ctx = {
            'players': players,
        }
        return render(request, 'spartakiada/players_delete_view.html', ctx)

    def post(self, request):
        for i in request.POST.getlist('player'):
            player = Player.objects.filter(name=i)
            player.delete()
        return redirect('/players/')

class PlayerDetailsView(View):

    def get(self, request, id):
        player = Player.objects.get(id=id)
        partaker = Partaker.objects.get_or_create(player=player)[0]
        ctx = {
            'player': player,
            'partaker': partaker
        }
        return render(request, 'spartakiada/player_details_view.html', ctx)
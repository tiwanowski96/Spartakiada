from math import log2
from random import shuffle

from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from spartakiada.models import Player, Tournament, Team, Cup, Game
from spartakiada.models.tournament import *

from .player import *
from .team import *

def knockout_next_round(request, tournament_id, lap):
    """
    Separate function creating another round of duels.
    Redirects to knockout page, where user can add players points.
    """
    tournament = Duel.objects.filter(tournament_id=tournament_id, lap=(int(lap) - 1))
    winners = []
    for duel in tournament:
        # makes random lose every time
        if str(duel.player2.partaker) == 'Random':
            winners.append(duel.player1_id)
        elif str(duel.player1.partaker) == 'Random':
            winners.append(duel.player2_id)

        # basic condition for winning: having more points
        elif duel.points1 > duel.points2:
            winners.append(duel.player1_id)
        elif duel.points1 < duel.points2:
            winners.append(duel.player2_id)
        else:
            return render(request, 'spartakiada/knockout_draw.html')
        link = ('/knockout/%s/%s' % (tournament_id, lap))

    # making new duels, aka generating another round
    if len(winners) == 1:
        Duel.objects.create(tournament_id=tournament_id, player1_id=winners[0], player2_id=winners[0], lap=lap)
    n = 0
    half_of_winners = len(winners) / 2
    for _ in range(int(half_of_winners)):
        Duel.objects.create(tournament_id=tournament_id, player1_id=winners[n], player2_id=winners[n + 1], lap=lap)
        n += 2
    return redirect(link)

# tournament
def make_players_list_for_knockout(tournament_id):
    """
    Returns list of new duels without points.
    Used to generate first lap of duels.
    """
    tournament = Tournament.objects.get(id=tournament_id)
    while not Duel.objects.filter(tournament=tournament).exists():

        # first we set up a random player, who will always lose
        random_player = Player.objects.get_or_create(name='Random')[0]
        random_partaker = Partaker.objects.get_or_create(player=random_player)[0]

        players = []
        tournament = Tournament.objects.get(id=tournament_id)
        for player in Participation.objects.filter(tournament_id=tournament_id):
            players.append(player)

        # top up the list with random players
        while not int(log2(len(players))) == log2(len(players)):
            random = Participation.objects.create(tournament_id=tournament_id, partaker=random_partaker)
            players.append(random)
        shuffle(players)
        a = len(players) / 2
        d = 0

        # if there are two randoms in the same duel separate them
        for _ in range(int(a)):
            if players[d].partaker == players[d + 1].partaker:
                players.insert(d + 2, players.pop(d))

            Duel.objects.create(tournament=tournament, player1=players[d], player2=players[d + 1], lap=1)
            d += 2

        # to make sure that there will never be a duel of two randoms
        last_duel = Duel.objects.last()
        if last_duel.player1.partaker == last_duel.player2.partaker:
            for duel in Duel.objects.filter(tournament=tournament):
                duel.delete()
                continue

    stage = Duel.objects.filter(tournament=tournament).order_by("id")
    return stage

class ParticipationsAddToGameView(View):
    
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        player_list = players_alphabetically()
        ctx = {
            'tournament': tournament,
            'player_list': player_list
        }
        return render(request, 'spartakiada/participations_add_view.html', ctx)

    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        for i in request.POST.getlist('player'):
            player = Player.objects.get(name=i)
            partaker = Partaker.objects.get_or_create(player=player)[0]
            Participation.objects.create(partaker=partaker, tournament=tournament)
        return redirect('/knockout/%s/1' % tournament_id)

class TeamsAddToGameView(View):

    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        team_list = Team.objects.all().order_by('name')
        ctx = {
            'tournament': tournament,
            'team_list': team_list,
        }
        return render(request, 'spartakiada/team_add_game_view.html', ctx)

    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        for i in request.POST.getlist('team'):
            team = Team.objects.get(name=i)
            partaker = Partaker.objects.get_or_create(team=team)[0]
            Participation.objects.create(partaker=partaker, tournament=tournament)
        return redirect('/knockout/%s/1' % tournament_id)

class KnockoutView(View):

    def get(self, request, tournament_id, lap):
        tournament = Tournament.objects.get(id=tournament_id)
        stages = make_players_list_for_knockout(tournament_id)
        ctx = {
            'stages': stages,
            'tournament': tournament,
            'lap': lap
        }
        return render(request, 'spartakiada/knockout.html', ctx)

    def post(self, request, tournament_id, lap):
        tournament = Tournament.objects.get(id=tournament_id)
        duels = Duel.objects.filter(tournament=tournament, lap=lap)
        for duel in duels:
            try:
                odd_player_points = request.POST['%s' % duel.player1.partaker]
                even_player_points = request.POST['%s' % duel.player2.partaker]
                duel.points1 = odd_player_points
                duel.points2 = even_player_points
                duel.save()
                lap = int(duel.lap) + 1
            except MultiValueDictKeyError:
                return render(request, 'spartakiada/except_cup_ended.html')
            except ValueError:
                return render(request, 'spartakiada/except_empty_input.html')

        return redirect('/next_round/%s/%s' % (tournament_id, lap))
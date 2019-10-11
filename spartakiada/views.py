from math import log2
from random import shuffle

from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, TemplateView
from .models import Player, Tournament, Participation, Duel, Team, Member, Cup, Game, Partaker, PlayerCache
from .cron import make_players_cache


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


def best_teams():
    all = PlayerCache.objects.all().order_by("-tournament_won")
    teams = []
    for team in all:
        if team.partaker.team:
            teams.append(team)
    return teams


class BaseView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)


# main page
class AboutView(View):

    def get(self, request):
        return render(request, 'spartakiada/about_view.html')


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


# players
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


# teams
class TeamsView(View):

    def get(self, request):
        team_list = Team.objects.all()
        ctx = {
            'team_list': team_list
        }
        return render(request, 'spartakiada/team_view.html', ctx)


class TeamAddView(View):

    def get(self, request):
        players = players_alphabetically()
        ctx = {
            'players': players,
        }
        return render(request, 'spartakiada/team_form.html', ctx)

    def post(self, request):
        name = request.POST['team_name']
        team = Team.objects.create(name=name)
        for i in request.POST.getlist('player'):
            player = Player.objects.get(name=i)
            Member.objects.create(player=player, team=team)
        request.session['last_team'] = name
        return redirect('/teams/')


class TeamsDeleteView(View):

    def get(self, request):
        team_list = Team.objects.all()
        ctx = {
            'team_list': team_list,
        }
        return render(request, 'spartakiada/teams_delete_view.html', ctx)

    def post(self, request):
        for i in request.POST.getlist('team'):
            team = Team.objects.filter(name=i)
            team.delete()
        return redirect('/teams/')


class TeamDetailsView(View):
    def get(self, request, team_id):
        team_id = int(team_id)
        team = Team.objects.get(id=team_id)
        team_members = Member.objects.filter(team=team)
        ctx = {
            'team': team,
            'team_members': team_members
        }
        return render(request, 'spartakiada/team_detail_view.html', ctx)


class TeamDetailsStatsView(View):
    def get(self, request, team_id):
        team = Team.objects.get(id=team_id)
        partaker = Partaker.objects.get_or_create(team=team)[0]
        ctx = {
            'team': team,
            'partaker': partaker,
        }
        return render(request, 'spartakiada/team_detail_view_stats.html', ctx)


class TeamAddMembersView(View):

    def get(self, request, team_id):
        team_id = int(team_id)
        team = Team.objects.get(id=team_id)
        player_list = players_alphabetically()
        team_members = Member.objects.filter(team=team)
        team_members = [Player.objects.get(name=player.player.name) for player in team_members]
        member_list = []
        for player in player_list:
            if player not in team_members:
                member_list.append(player)
        ctx = {
            'team': team,
            'member_list': member_list,
        }
        return render(request, 'spartakiada/team_add_members.html', ctx)

    def post(self, request, team_id):
        team = Team.objects.get(id=team_id)
        for i in request.POST.getlist('player'):
            player = Player.objects.get(name=i)
            Member.objects.create(player=player, team=team)
        return redirect('/team_details/%s' % team_id)


class TeamRemoveMembersView(View):

    def get(self, request, team_id):
        team = Team.objects.get(id=team_id)
        team_members = Member.objects.filter(team=team)
        print(team_members)
        ctx = {
            'team': team,
            'team_members': team_members,
        }
        return render(request, 'spartakiada/team_remove_members.html', ctx)

    def post(self, request, team_id):
        team = Team.objects.get(id=team_id)
        for i in request.POST.getlist('player'):
            player = Player.objects.filter(name=i)
            member = Member.objects.get(player=player, team=team)
            member.delete()
        return redirect('/team_details/%s' % team_id)


# cups
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


class CupAddView(CreateView):
    model = Cup
    fields = [
        'name', 'date'
    ]


class CupAddGamesView(View):

    def get(self, request, cup_id):
        cup_id = int(cup_id)
        cup = Cup.objects.get(id=cup_id)
        game_list = Game.objects.all().order_by('name')
        tournament = Tournament.objects.filter(cup=cup)

        ctx = {
            'cup': cup,
            'game_list': game_list,
            'tournament': tournament
        }
        return render(request, 'spartakiada/cup_add_games_view.html', ctx)

    def post(self, request, cup_id):
        cup = Cup.objects.get(id=cup_id)
        for i in request.POST.getlist('game'):
            if 'ind_%s' % i in request.POST:
                Tournament.objects.create(cup=cup, game_id=i, individual=True)
            if 'team_%s' % i in request.POST:
                Tournament.objects.create(cup=cup, game_id=i, individual=False)
        tournaments = Tournament.objects.filter(cup=cup)
        if tournaments.count() != 0:
            return redirect('/cup/%s' % cup_id)
        else:
            return render(request, 'spartakiada/except_empty.html')


class CupView(View):

    def get(self, request, cup_id):
        cup = Cup.objects.get(id=cup_id)
        tournament_list = Tournament.objects.filter(cup=cup)
        ctx = {
            'cup': cup,
            'tournament_list': tournament_list,
        }
        if len(tournament_list) != 0:
            return render(request, 'spartakiada/cup_view.html', ctx)
        else:
            return redirect('/cup_add_games/%s' % cup_id)


class CupsListView(ListView):

    model = Cup

    ordering = ['-date']


class CupDeleteView(DeleteView):
    model = Cup
    success_url = '/'
    pk_url_kwarg = 'cup_id'


# gameplay
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


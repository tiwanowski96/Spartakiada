from .player import *
from django.shortcuts import redirect, render
from django.views import View
from spartakiada.models import Member, Partaker, Player, PlayerCache, Team

def best_teams():
    all = PlayerCache.objects.all().order_by("-tournament_won")
    teams = []
    for team in all:
        if team.partaker.team:
            teams.append(team)
    return teams

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
        ctx = {
            'team': team,
            'team_members': team_members,
        }
        return render(request, 'spartakiada/team_remove_members.html', ctx)

    def post(self, request, team_id):
        team = Team.objects.get(id=team_id)
        for i in request.POST.getlist('player'):
            player = Player.objects.filter(name=i)
            member = Member.objects.get(player=player[0], team=team)
            member.delete()
        return redirect('/team_details/%s' % team_id)
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from spartakiada.models import Cup, Game, Tournament

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
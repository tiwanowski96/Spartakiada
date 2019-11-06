from collections import OrderedDict
from django.shortcuts import redirect, render
from django.views import View
from spartakiada.models import Cup, Tournament, Participation, Duel

class CupRankView(View):
    
    def get(self, request, cup_id):
        try:
            cupScore = {}
            grandPrixList = []
            cup = Cup.objects.get(id=cup_id)
            tournament_list = Tournament.objects.filter(cup=cup)
            for tournament in tournament_list:
                participations = Participation.objects.filter(tournament=tournament)
                score = {}
                for participation in participations:
                    if Duel.objects.filter(tournament = tournament, player1 = participation).last():
                        duel_last = Duel.objects.filter(tournament = tournament, player1 = participation).last()
                    else:
                        duel_last = Duel.objects.filter(tournament = tournament, player2 = participation).last()
                    score[participation.partaker]=int(duel_last.lap - 1)
                scoreSorted = sorted(score.items(), key=lambda item: item[1], reverse=True)
                cupScore[tournament]=scoreSorted
                for val in scoreSorted:
                    grandPrixList.append(val)
            
            GPDict = {}
            for t in grandPrixList:
                if t[0] in GPDict:
                    GPDict[t[0]] = GPDict[t[0]]+t[1]
                else:
                    GPDict[t[0]] = t[1]
            GPDictSorted = sorted(GPDict.items(), key=lambda item: item[1], reverse=True)
            participationsCount = len(GPDictSorted)
            rangeCount = range(1, participationsCount+1)
            ctx = {
                'cup': cup,
                'tournament_list': tournament_list,
                'participations': participations,
                'cupScore': cupScore,
                'score': score,
                'scoreSorted': scoreSorted,
                'GPDict': GPDictSorted,
                'range': rangeCount 
            }
            return render(request, 'spartakiada/cupRank_view.html', ctx)
        except AttributeError:
            return render(request, 'spartakiada/except_option_disabled.html')

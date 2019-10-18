from django.db import models
from spartakiada.models import Tournament
from spartakiada.models.tournament import Partaker

# model used for stats
class PlayerCache(models.Model):
    partaker = models.ForeignKey(Partaker, default=None, on_delete=models.CASCADE)
    won = models.IntegerField(null=True)
    played = models.IntegerField(null=True)
    tournament_won = models.IntegerField(null=True)
    tournament_second = models.IntegerField(null=True)
    tournament_participated = models.IntegerField(null=True)

    class Meta:
        app_label = 'spartakiada'
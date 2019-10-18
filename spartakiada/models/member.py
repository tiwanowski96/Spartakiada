from django.db import models
from .player import Player
from .team import Team

# enables players to be team members
class Member(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.player.name

    class Meta:
        app_label = 'spartakiada'
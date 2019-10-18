from django.db import models
from .player import Player

class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    mates = models.ManyToManyField(Player, through='Member')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        app_label = 'spartakiada'
from django.db import models

# type of game/sport
class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        app_label = 'spartakiada'
import kronos

from spartakiada.models import PlayerCache, Tournament, Player
from spartakiada.models.tournament import Duel, Partaker, Tournament, Participation

"""
We're using kronos to generate updates of stats, which takes few seconds when made on demand.
Every 5 minutes kronos creates cache like table of all required stats, that are saved in
dedicated model.
"""


@kronos.register('*/5 * * * *')
def make_players_cache():
    random_player = Player.objects.get_or_create(name="Random")[0]
    partakers = Partaker.objects.all().exclude(player=random_player)
    for player in partakers:
        player_cache = PlayerCache.objects.get_or_create(partaker=player)[0]
        player_cache.won = player.duels['won']
        player_cache.played = player.duels['played']
        player_cache.tournament_won = len(player.tournaments_won)
        player_cache.tournament_second = player.was_second
        player_cache.tournament_participated = player.tournaments_participated
        player_cache.save()


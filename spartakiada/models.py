from django.db import models
from django.urls import reverse


class Player(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('players')


    """
    Not perfect way to get players gender basing on their first name.
    Works only for polish names.
    """
    @property
    def gender(self):
        male_names = ["Bonawentura", "Kuba", "Kosma", "Attyla", "Barnaba", "Seba", "Dyzma", "Zawisza"]
        female_names = ["Miriam", "Nicole", "Noemi", "Beatrycze", "Nel"]
        name = self.name.partition(' ')[0]
        if name.endswith("a") and name not in male_names or name in female_names:
            return "F"
        else:
            return "M"



class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    mates = models.ManyToManyField(Player, through='Member')

    def __str__(self):
        return '%s' % self.name


# enables players to be team members
class Member(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.player.name


# allow us to use the same functions for players and teams
class Partaker(models.Model):
    player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.player:
            return self.player.name
        elif self.team:
            return self.team.name
        else:
            return "unknown partaker"

    @property
    # returns list of dictionaries made of duel-like objects
    def details(self):
        random_player = Player.objects.get(name="Random")
        random = Partaker.objects.get(player=random_player)
        participations = Participation.objects.filter(partaker=self)
        player_info = []
        if participations.count() != 0 and self != random:
            duels = []
            win = []
            for participation in participations:
                duels.append(Duel.objects.filter(player1=participation))
                duels.append(Duel.objects.filter(player2=participation))
            flat_duels = [item for sublist in duels for item in sublist]
            for duel in flat_duels:
                if duel.player1.partaker != random \
                        and duel.player2.partaker != random \
                        and duel.player1 != duel.player2:
                    player_info.append({
                        'player1': duel.player1.partaker,
                        'player2': duel.player2.partaker,
                        'points1': duel.points1,
                        'points2': duel.points2,
                        'game_name': duel.tournament.game.name,
                        'tournament_name': duel.tournament.cup.name,
                        'tournament_date': duel.tournament.cup.date,
                        'lap': duel.lap,
                    })
                elif duel.player1 == duel.player2:
                    win.append({
                        'player1': duel.player1.partaker,
                        'player2': duel.player2.partaker,
                        'points1': duel.points1,
                        'points2': duel.points2,
                        'game_name': duel.tournament.game.name,
                        'tournament_name': duel.tournament.cup.name,
                        'tournament_date': duel.tournament.cup.date,
                        'lap': duel.lap,
                    })
            # won objects are doubled, so we delete every second
            if len(win) > 0:
                del win[::2]

            # join both dictionaries
            player_info += win

        player_info = sorted(player_info, key=lambda k: k['tournament_date'], reverse=True)
        return player_info

    @property
    # returns dictionary
    def duels(self):
        player_info = self.details
        games_won = 0
        games_played = 0
        for duel in player_info:
            if duel['points1'] is not None:
                if duel['player1'] == self and duel['points1'] > duel['points2']:
                    games_won += 1
                    games_played += 1
                elif duel['player2'] == self and duel['points1'] < duel['points2']:
                    games_won += 1
                    games_played += 1
                else:
                    games_played += 1
        return {"won": games_won,
                "played": games_played}

    @property
    # returns list of duel objects
    def tournaments_won(self):
        player_info = self.details
        won_tournaments = []
        for duel in player_info:
            if duel['player1'] == duel['player2']:
                won_tournaments.append(duel)
        return won_tournaments

    @property
    # returns integer
    def was_second(self):
        silver_winners = []
        tournaments_participated = Tournament.objects.filter(participants=self)
        for tournaments in tournaments_participated:
            if tournaments.second is not None:
                silver_winners.append(tournaments.second.partaker)
        return silver_winners.count(self)

    @property
    # returns integer
    def tournaments_participated(self):
        participations = Participation.objects.filter(partaker=self)
        parts = []
        for part in participations:
            parts.append(part.tournament.cup.id)
        return len(set(parts))


# type of game/sport
class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return '%s' % self.name


class Cup(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()

    class Meta:
        unique_together = ("name", "date")

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('cup-add-games', kwargs={'cup_id': self.id})


class Tournament(models.Model):
    participants = models.ManyToManyField('Partaker', through='Participation')
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    cup = models.ForeignKey(Cup, null=True, on_delete=models.CASCADE)
    individual = models.BooleanField(default=True)

    class Meta:
        unique_together = ("cup", "game", "individual")

    @property
    # returns boolean value
    def is_over(self):
        duels = Duel.objects.filter(tournament=self).order_by("-lap")
        if duels[0].player1 is None:
            return False
        else:
            return True

    @property
    # returns duel object
    def winner(self):
        if self.is_over:
            duels = Duel.objects.filter(tournament=self).order_by("-lap")
            return duels[0]

    @property
    # returns participations object
    def second(self):
        if self.is_over:
            duels = Duel.objects.filter(tournament=self).order_by("-lap")
            if duels[0].player1 == duels[0].player2:
                if duels[1].player1 != duels[0].player1:
                    return duels[1].player1
                else:
                    return duels[1].player2

    @property
    # returns integer
    def last_lap(self):
        last_lap = Duel.objects.filter(tournament=self).last().lap
        return last_lap


class Participation(models.Model):
    partaker = models.ForeignKey(Partaker, null=True, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


# atomic event of all games, which is a single duel of two players
class Duel(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Participation, related_name='game_played', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Participation, related_name='game_played2', on_delete=models.CASCADE)
    points1 = models.IntegerField(null=True)
    points2 = models.IntegerField(null=True)
    lap = models.IntegerField(null=True)


# model used for stats
class PlayerCache(models.Model):
    partaker = models.ForeignKey(Partaker, default=None, on_delete=models.CASCADE)
    won = models.IntegerField(null=True)
    played = models.IntegerField(null=True)
    tournament_won = models.IntegerField(null=True)
    tournament_second = models.IntegerField(null=True)
    tournament_participated = models.IntegerField(null=True)
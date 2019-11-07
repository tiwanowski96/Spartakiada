from django.contrib import admin
from spartakiada.models import Cup, Duel, Game, Member, Partaker, Participation, Player, Team, Tournament


class TournamentInline(admin.TabularInline):
    model = Tournament
    extra = 1

class MemberInline(admin.TabularInline):
    model = Member
    extra = 1

class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1

class PartakerInline(admin.TabularInline):
    model = Partaker
    extra = 1

class DuelInline(admin.TabularInline):
    model = Duel
    extra = 1



class CupAdmin(admin.ModelAdmin):
    inlines = [TournamentInline]

class GameAdmin(admin.ModelAdmin):
    inlines = [TournamentInline]

class PartakerAdmin(admin.ModelAdmin):
    inlines = [ParticipationInline]

class PlayerAdmin(admin.ModelAdmin):
    inlines = [MemberInline, PartakerInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [MemberInline, PartakerInline]

class TournamnetAdmin(admin.ModelAdmin):
    inlines = [ParticipationInline, DuelInline]

admin.site.register(Cup, CupAdmin)
admin.site.register(Duel)
admin.site.register(Game, GameAdmin)
admin.site.register(Member)
admin.site.register(Partaker, PartakerAdmin)
admin.site.register(Participation)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament, TournamnetAdmin)




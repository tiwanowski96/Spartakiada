from django import forms
from .models import Player, Team, Game, Cup


class PlayerAddForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'name'
        ]


class PlayerDeleteForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        Player.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Player
        fields = [
            'name'
        ]


class TeamAddForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name', 'mates'
        ]


class TeamsDeleteForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        Team.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Team
        fields = [
            'name'
        ]


class GameAddForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'name'
        ]


class GamesDeleteForm(forms.ModelForm):
    games = forms.ModelMultipleChoiceField(
        Game.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Game
        fields = [
            'name'
        ]


class CupAddForm(forms.ModelForm):

    class Meta:
        model = Cup
        fields = [
            'name', 'date'
        ]

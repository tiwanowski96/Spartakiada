"""competition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from spartakiada import views
from loging import views as loging


urlpatterns = [
    # url(r'^admin/', admin.urls),
    url(r'^$', views.MenuView.as_view(),
        name='menu'),
    url(r'^about/', views.AboutView.as_view(),
        name='about'),
    url(r'^players/', views.PlayersView.as_view(),
        name='players'),
    url(r'^add_player/', views.PlayerAddView.as_view(),
        name='add-player'),
    url(r'^delete_player/', views.PlayerDeleteView.as_view(),
        name='delete-player'),
    url(r'^teams/', views.TeamsView.as_view(),
        name='teams'),
    url(r'^player_details/(?P<id>(\d)+)/$', views.PlayerDetailsView.as_view(),
        name='player'),
    url(r'^stats/$', views.Stats.as_view(),
        name='stats'),
    url(r'refresh_stats/$', views.refresh_stats,
        name='refresh-stats'),
    url(r'^add_team/', views.TeamAddView.as_view(),
        name='add-team'),
    url(r'^delete_teams/', views.TeamsDeleteView.as_view(),
        name='delete-teams'),
    url(r'^team_details/(?P<team_id>(\d)+)', views.TeamDetailsView.as_view(),
        name='team-details'),
    url(r'^team_add_members/(?P<team_id>(\d)+)', views.TeamAddMembersView.as_view(),
        name='team-add-members'),
    url(r'^team_remove_members/(?P<team_id>(\d)+)', views.TeamRemoveMembersView.as_view(),
        name='team-remove-members'),
    url(r'^games/', views.GamesView.as_view(),
        name='games'),
    url(r'^add_game/', views.GameAddView.as_view(),
        name='add-game'),
    url(r'^delete_games/', views.GamesDeleteView.as_view(),
        name='delete-games'),
    url(r'^add_cup/', views.CupAddView.as_view(),
        name='add-cup'),
    url(r'^cup_add_games/(?P<cup_id>(\d)+)', views.CupAddGamesView.as_view(),
        name='cup-add-games'),
    url(r'^knockout/(?P<tournament_id>(\d)+)/(?P<lap>(\d)+)/$', views.KnockoutView.as_view(),
        name='knockout'),
    url(r'^next_round/(?P<tournament_id>(\d)+)/(?P<lap>(\d)+)/$', views.knockout_next_round),
    url(r'^cup/(?P<cup_id>(\d)+)', views.CupView.as_view(),
        name='cup'),
    url(r'^cups_list/$', views.CupsListView.as_view(),
        name='cups'),
    url(r'^participations_add_to_game/(?P<tournament_id>(\d)+)', views.ParticipationsAddToGameView.as_view(),
        name='participations'),
    url(r'^team_add_to_game/(?P<tournament_id>(\d)+)', views.TeamsAddToGameView.as_view(),
        name='team-add-game'),
    url(r'^team_stats/(?P<team_id>(\d)+)', views.TeamDetailsStatsView.as_view(),
        name='team-stats'),
    url(r'^delete_cup/(?P<cup_id>(\d)+)', views.CupDeleteView.as_view(),
        name="cup-delete"),

    url(r'^register/$', loging.UserCreateView.as_view(),
        name='register'),
    url(r'^login/$', loging.UserLoginView.as_view(),
        name='login'),
    url(r'^logout/$', loging.UserLogoutView.as_view(),
        name='logout')
]




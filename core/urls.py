"""
define the url routes of core api
"""
from core.api.player import list_player_info
from core.api.team import list_team_info
from django.urls import path

urlpatterns = [
    #path('user/create', create_user),team_info

    #team
    path('team/team_info', list_team_info),

    #player
    path('player/player_info', list_player_info)
]

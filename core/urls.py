"""
define the url routes of core api
"""
from core.api.comment import get_comment, upload_comment
from core.api.game import list_game_info
from core.api.honor import list_honor
from core.api.player import get_player_photo, get_team_players, list_all_player_info, list_player_info
from core.api.team import list_team_info, list_team
from django.urls import path

urlpatterns = [
    #path('user/create', create_user),team_info

    #team
    path('team/team_info', list_team_info),
    path('team/list_team', list_team),

    #player
    path('player/player_info', list_player_info),
    path('player/list_player', list_all_player_info),
    path('player/get_player_photo', get_player_photo),
    path('player/get_team_players', get_team_players),

    #game
    path('game/game_info', list_game_info),

    #comment
    path('comment/list_comment', get_comment),
    path('comment/upload_comment', upload_comment),
    #path('comment/get_comment', get_comment),

    #honor
    path('honor/list_honor', list_honor),
]

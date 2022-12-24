"""
define the url routes of core api
"""
from core.api.auth import obtain_jwt_token
from core.api.comment import delete_comment, get_comment, upload_comment, upload_star
from core.api.game import list_game_info
from core.api.honor import list_honor
from core.api.player import get_player_photo, get_team_players, list_all_player_info, list_all_player_info_csv, list_player_info
from core.api.team import list_team_csv, list_team_info, list_team
from django.urls import path

from core.api.user_management import create_user, lock_user

urlpatterns = [
    #path('user/create', create_user),team_info

    #user
    path('token-auth', obtain_jwt_token),
    path('user/create', create_user),
    path('user/lock_user', lock_user),

    #team
    path('team/team_info', list_team_info),
    path('team/list_team', list_team),
    path('team/list_team_csv', list_team_csv),

    #player
    path('player/player_info', list_player_info),
    path('player/list_player', list_all_player_info),
    path('player/list_player_csv', list_all_player_info_csv),
    path('player/get_player_photo', get_player_photo),
    path('player/get_team_players', get_team_players),

    #game
    path('game/game_info', list_game_info),

    #comment
    path('comment/list_comment', get_comment),
    path('comment/upload_comment', upload_comment),
    path('comment/delete_comment', delete_comment),
    path('comment/upload_star', upload_star),
    #path('comment/get_comment', get_comment),

    #honor
    path('honor/list_honor', list_honor),
]

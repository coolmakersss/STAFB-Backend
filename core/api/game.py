
from pipes import Template
from sysconfig import get_path_names
from telnetlib import GA

from django.forms import model_to_dict
from core.api.auth import jwt_auth
from core.api.utils import response_wrapper
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Game, Player, PlayerStats, Team, TeamStats
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)

@response_wrapper
@jwt_auth(perms=[])
@require_GET
def list_game_info(request: HttpRequest):
    """List all games

    [route]: /api/game/game_info

    [method]: GET
    """

    games = Game.objects.all()
    games_count = len(games)
    game_details = []

    for game in games:
        tmp = model_to_dict(game,exclude=["host","guest"])
        tmp["host_gym"] = game.host.gym
        tmp["host_name"] = game.host.name
        tmp["host_name_cn"] = game.host.name_cn
        tmp["guest_name"] = game.guest.name
        tmp["guest_name_cn"] = game.guest.name_cn
        game_details.append(tmp)
    def rule(t):
        return t["time"]
    game_details.sort(key=rule)

    gameInfo = {
        "game_count" : games_count,
        "game_details" : game_details
    }

    return success_api_response(gameInfo)

@response_wrapper
@jwt_auth(perms=[])
@require_GET
def game_team_stats(request: HttpRequest):
    """List team stats for a game

    [route]: /api/game/game_team_stats

    [method]: GET
    """

    game = Game.objects.get(id=request.GET.get("gameId"))
    host_team = game.host
    guest_team = game.guest
    host_details = {}
    guest_details = {}

    hoststat = TeamStats.objects.filter(belong_to_game=game, belong_to_team=host_team).first()
    if not hoststat is None:
        host_details = model_to_dict(hoststat,exclude=["belong_to_team","belong_to_game"])
        tmp = model_to_dict(hoststat.belong_to_team,exclude=["id"])
        host_details = { **tmp, **host_details}

    gueststat = TeamStats.objects.filter(belong_to_game=game, belong_to_team=guest_team).first()
    if not gueststat is None:
        guest_details = model_to_dict(gueststat,exclude=["belong_to_team","belong_to_game"])
        tmp = model_to_dict(gueststat.belong_to_team,exclude=["id"])
        guest_details = { **tmp, **guest_details}

    gameInfo = {
        "host_team_details" : host_details,
        "guest_team_details" : guest_details
    }

    return success_api_response(gameInfo)


@response_wrapper
#@jwt_auth(perms=[])
@require_GET
def game_player_stats(request: HttpRequest):
    """List player stats for a game

    [route]: /api/game/game_player_stats

    [method]: GET
    """

    game = Game.objects.get(id=request.GET.get("gameId"))
    host_details = []
    guest_details = []
    host_team = game.host
    guest_team = game.guest

    players_stats = PlayerStats.objects.filter(belong_to_game=game).all()

    for stat in players_stats:
        tmp = model_to_dict(stat,exclude=["belong_to_player","belong_to_game"])
        tmp1 = model_to_dict(stat.belong_to_player,exclude=["id","team"])
        tmp = { **tmp1,**tmp}

        if stat.belong_to_player.team == host_team:
            host_details.append(tmp)
        else:
            guest_details.append(tmp)
    
    def rule(t):
        return t["score"]
    host_details.sort(key=rule)
    guest_details.sort(key=rule)

    gameInfo = {
        "host_player_count" : len(host_details),
        "host_player_details" : host_details,
        "guest_player_count" : len(guest_details),
        "guest_player_details" : guest_details
    }
    return success_api_response(gameInfo)
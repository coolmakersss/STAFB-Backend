from os import stat
from django.forms import model_to_dict
from STATFB.settings import S3_ADDRESS
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Player, PlayerStats, Team
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.db.models import Avg

@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_player_info(request: HttpRequest):
    """List team which meets the need

    [route]: /api/player/player_info

    [method]: GET
    """
    playerName = request.GET.get("playerName")
    player = Player.objects.filter(name=playerName).first()
    if player is None:
        player = Player.objects.filter(name_cn=playerName).first()
        if player is None:
            return failed_api_response(ErrorCode.PLAYER_NOT_FOUND ,"Can't find such a player!")
    
    stats = PlayerStats.objects.filter(belong_to_player=player).aggregate(
        minute = Avg('minute'),
        score = Avg('score'),
        rebound = Avg('score'),
        o_rebound = Avg('o_rebound'),
        d_rebound = Avg('d_rebound'),
        assist = Avg('assist'),
        steal = Avg('steal'),
        block = Avg('block'),
        foul = Avg('foul'),
        turnover = Avg('turnover'),

        field_goals_attempted = Avg('field_goals_attempted'),
        field_goals_made = Avg('field_goals_made'),
        field_goals_rate = Avg('field_goals_made') / Avg('field_goals_attempted'),

        three_points_attempt = Avg('three_points_attempt'),
        three_points_made = Avg('three_points_made'),
        three_points_rate = Avg('three_points_made') / Avg('three_points_attempt'),

        free_throws_attempted = Avg('free_throws_attempted'),
        free_throws_made = Avg('free_throws_made'),
        free_throws_rate = Avg('free_throws_made') / Avg('free_throws_attempted'),

        plus_minus = Avg('plus_minus')
        )
    playerInfo = {
        "name" : player.name,
        "name_cn" : player.name_cn,
        "age" : player.age,
        "hight" : player.hight,
        "weight": player.weight,
        "number" : player.number,
        "team": player.team.name,
        "team_cn": player.team.name_cn,
        "photo": S3_ADDRESS+player.photo
    }
    playerInfo = {**playerInfo, **stats}

    return success_api_response(playerInfo)


@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_all_player_info(request: HttpRequest):
    """List all players

    [route]: /api/player/list_player

    [method]: GET
    """

    players = Player.objects.all()
    players_count = len(players)
    player_details = []

    for player in players:
        tmp = model_to_dict(player,fields=["id","name","name_cn", "age", "hight", "weight","number","photo"])
        tmp["team"] = player.team.name_cn
        player_details.append(tmp)
    def rule(t):
        return t["name"]
    player_details.sort(key=rule)

    playerInfo = {
        "player_count" : players_count,
        "player_details" : player_details
    }

    return success_api_response(playerInfo)
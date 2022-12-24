from os import stat
from django.forms import model_to_dict
import pandas
from STATFB.settings import S3_ADDRESS
from core.api.auth import jwt_auth
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Player, PlayerStats, Team
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.db.models import Avg
from django.utils.encoding import escape_uri_path

@response_wrapper
@jwt_auth(perms=[])
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
        "position" : player.position,
        "number" : player.number,
        "team": player.team.name,
        "team_cn": player.team.name_cn,
        "photo": player.photo
    }
    playerInfo = {**playerInfo, **stats}

    return success_api_response(playerInfo)


@response_wrapper
@jwt_auth(perms=[])
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
        tmp = model_to_dict(player,fields=["id","name","name_cn", "age", "hight", "weight", "position", "number","photo"])
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

@response_wrapper
@jwt_auth(perms=[])
@require_GET
def list_all_player_info_csv(request: HttpRequest):
    """List all players in csv file

    [route]: /api/player/list_player/csv

    [method]: GET
    """

    players = Player.objects.all()
    player_details = []

    for player in players:
        tmp = model_to_dict(player,fields=["id","name","name_cn", "age", "hight", "weight","position","number","photo"])
        tmp["team"] = player.team.name_cn
        tmp["photo"] = "http://43.143.132.12/photo-set/"+player.photo
        player_details.append(tmp)
    def rule(t):
        return t["name"]
    player_details.sort(key=rule)

    data_frames = pandas.DataFrame(player_details)
    meta_info_columns = ["id","name","name_cn", "age", "hight", "weight","position","number","photo"]
    data_frames = data_frames[meta_info_columns]
    ret_data = data_frames.to_csv()

    return HttpResponse(ret_data)


@response_wrapper
@jwt_auth(perms=[])
@require_GET
def get_player_photo(request: HttpRequest):
    """List all players

    [route]: /api/player/get_player_photo

    [method]: GET
    """
    playerName = request.GET.get("playerName")
    player = Player.objects.filter(name=playerName).first()
    if player is None:
        player = Player.objects.filter(name_cn=playerName).first()
        if player is None:
            return failed_api_response(ErrorCode.PLAYER_NOT_FOUND ,"Can't find such a player!")
    

    source_path = "./photo-set{}".format(player.photo)
    print(source_path)
    with open(source_path, "rb") as file:
        response = HttpResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename*=utf-8''{}".format(
        escape_uri_path(source_path.split("/")[-1]))
    return response


@response_wrapper
@jwt_auth(perms=[])
@require_GET
def get_team_players(request: HttpRequest):
    """List all players from a team

    [route]: /api/player/get_team_players

    [method]: GET
    """
    teamName = request.GET.get("teamName")
    team = Team.objects.filter(name=teamName).first()
    if team is None:
        team = Team.objects.filter(name_cn=teamName).first()
        if team is None:
            return failed_api_response(ErrorCode.TEAM_NOT_FOUND ,"Can't find such a team!")
    players = Player.objects.filter(team=team).all()
    player_details=[]
    for player in players:
        tmp = model_to_dict(player)
        player_details.append(tmp)

    playerInfo = {
        "player_count" : len(player_details),
        "player_details" : player_details
    }
    
    return success_api_response(playerInfo)
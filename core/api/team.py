from stringprep import in_table_a1

import pandas
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Coach, Team, Game, TeamStats
from django.http import HttpRequest, HttpResponse
from django.forms import model_to_dict
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.db.models import Avg

@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_team_info(request: HttpRequest):
    """List team which meets the need

    [route]: /api/team/team_info

    [method]: GET
    """
    teamName = request.GET.get("teamName")
    team = Team.objects.filter(name=teamName).first()
    if team is None:
        team = Team.objects.filter(name_cn=teamName).first()
        if team is None:
            return failed_api_response(ErrorCode.TEAM_NOT_FOUND ,"Can't find such a team!")
    stats = TeamStats.objects.filter(belong_to_team=team).aggregate(
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

        )
    coach = Coach.objects.filter(team=team).first()
    coach_info : dict = model_to_dict(coach,fields=["name","name_cn","age","photo"])
    teamInfo = {
        "name" : team.name,
        "name_cn" : team.name_cn,
        "location" : team.location,
        "location_cn" : team.location_cn,
        "division": team.division,
        "subarea" : team.subarea,
        "gym": team.gym,
        "logo": team.logo,
        "coach_info": coach_info
    }
    teamInfo = {**teamInfo, **stats}

    return success_api_response(teamInfo)


@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_team(request: HttpRequest):
    """List all teams and rank

    [route]: /api/team/list_team

    [method]: GET
    """
    teams = Team.objects.all()
    teams_count = len(teams)
    print(teams_count)
    west_team_details = []
    east_team_details = []
    def rule(t):
        return -t["win_poss"]
    for team in teams:
        tmp : dict = model_to_dict(team,fields=["name", "name_cn", "location", "location_cn","division","subarea","gym","logo"])
        game_cout=0
        win_count=0
        games = Game.objects.filter(host=team)
        for game in games:
            game_cout+=1
            if game.host_score > game.guest_score:
                win_count+=1
        games = Game.objects.filter(guest=team)
        for game in games:
            game_cout+=1
            if game.host_score < game.guest_score:
                win_count+=1
        tmp["game_cout"] = game_cout
        tmp["win_count"] = win_count
        tmp["win_poss"] = round(win_count/game_cout,4)
        if tmp["division"] == "west" :
            west_team_details.append(tmp)
        else :
            east_team_details.append(tmp)
    west_team_details.sort(key=rule)
    east_team_details.sort(key=rule)    
    #team_details = list(teams.object_list.values("name", "name_cn", "location", "location_cn","division","subarea","gym"))
    team_data = {
        "team_all" : teams_count,
        "west_teams_count" : len(west_team_details),
        "east_teams_count" : len(east_team_details),
        "west_teams": west_team_details,
        "east_teams": east_team_details
    }

    return success_api_response(team_data)

@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_team_csv(request: HttpRequest):
    """List all teams in csv file

    [route]: /api/team/list_team_csv

    [method]: GET
    """
    teams = Team.objects.all()
    teams_count = len(teams)
    print(teams_count)
    team_details = []
    def rule(t):
        return -t["win_poss"]
    for team in teams:
        tmp : dict = model_to_dict(team,fields=["name", "name_cn", "location", "location_cn","division","subarea","gym","logo"])
        game_cout=0
        win_count=0
        games = Game.objects.filter(host=team)
        for game in games:
            game_cout+=1
            if game.host_score > game.guest_score:
                win_count+=1
        games = Game.objects.filter(guest=team)
        for game in games:
            game_cout+=1
            if game.host_score < game.guest_score:
                win_count+=1
        tmp["logo"] = "http://43.143.132.12/photo-set/"+tmp["logo"]
        tmp["game_cout"] = game_cout
        tmp["win_count"] = win_count
        tmp["win_poss"] = round(win_count/game_cout,4)
        team_details.append(tmp)
    team_details.sort(key=rule)
    data_frames = pandas.DataFrame(team_details)
    meta_info_columns = ["name", "name_cn", "location", "location_cn","division","subarea","gym","logo",
    "win_count","game_cout","win_poss"]
    data_frames = data_frames[meta_info_columns]
    ret_data = data_frames.to_csv()

    return HttpResponse(ret_data)
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Team
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)


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
    teamInfo = {
        "name" : team.name,
        "name_cn" : team.name_cn,
        "location" : team.location,
        "location_cn" : team.location_cn,
        "division": team.division,
        "subarea" : team.subarea,
        "gym": team.gym
    }

    return success_api_response(teamInfo)

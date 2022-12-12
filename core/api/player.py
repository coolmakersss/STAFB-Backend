from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Player, Team
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)


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
    playerInfo = {
        "name" : player.name,
        "name_cn" : player.name_cn,
        "age" : player.age,
        "hight" : player.hight,
        "weight": player.weight,
        "number" : player.number,
        "team": player.team.name,
        "team_cn": player.team.name_cn
    }

    return success_api_response(playerInfo)
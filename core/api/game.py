
from sysconfig import get_path_names
from telnetlib import GA

from django.forms import model_to_dict
from core.api.utils import response_wrapper
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Game, Player, Team
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)

@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
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
        tmp = model_to_dict(game,fields=["id","season","time","host_score","guest_score"])
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
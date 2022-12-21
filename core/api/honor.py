from stringprep import in_table_a1
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import Coach, Player, PlayerHonors, Team, Game, TeamStats
from django.http import HttpRequest
from django.forms import model_to_dict
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.db.models import Avg

@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_honor(request: HttpRequest):
    """List honor for a season

    [route]: /api/honor/list_honor

    [method]: GET
    """
    honor = PlayerHonors.objects.filter(season=request.GET.get("season")).first()
    honor_info = model_to_dict(honor)
    for key in honor_info:
        if key == "id" or key == "season":
            continue
        elif key.find("team") != -1:
            print(key)
            players = []
            ids = honor_info[key].split(",")
            print(ids)
            for i in ids:
                player = Player.objects.filter(id=int(i)).first()
                players.append(model_to_dict(player))
            honor_info[key] = players
        else:
            player = Player.objects.filter(id=honor_info[key]).first()
            honor_info[key] = model_to_dict(player)

    return success_api_response(honor_info)
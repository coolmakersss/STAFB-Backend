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
def upload_comment(request: HttpRequest):
    """List all players

    [route]: /api/player/list_player

    [method]: POST
    """



    return success_api_response(gameInfo)


@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def get_comment(request: HttpRequest):
    """List all players

    [route]: /api/player/list_player

    [method]: get
    """



    return success_api_response(gameInfo)
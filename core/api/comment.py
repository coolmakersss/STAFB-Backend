import json
from os import stat
from django.forms import model_to_dict
from STATFB.settings import S3_ADDRESS
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import CommentStar, Game, Player, PlayerStats, Team, Comment, User
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
    """List comments for a game

    [route]: /api/comment/list_comment

    [method]: get
    """
    game = Game.objects.filter(id=request.GET.get("id")).first()
    comments = Comment.objects.filter(belong_to=game).all()
    comment_detils = []
    for comment in comments:
        tmp = model_to_dict(comment, fields=["create_by","create_time", "text"])
        tmp["create_by"] = comment.create_by.username
        comment_detils.append(tmp)
    def rule(t):
        return t["create_by"]
    comment_detils.sort(key=rule)

    commentInfo = {
        "comment_count": len(comments),
        "comment_detils": comment_detils
    }



    return success_api_response(commentInfo)

@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_POST
def upload_comment(request: HttpRequest):
    """List comments for a game

    [route]: /api/comment/upload_comment

    [method]: post
    """
    data: dict = parse_data(request)
    userId = data.get("create_by")
    gameId = data.get("belong_to")
    data["create_by"] = User.objects.filter(id=userId).first()
    data["belong_to"] = Game.objects.filter(id=gameId).first()
    ans: Comment = Comment.objects.create(**data)

    return success_api_response({'id': ans.id})
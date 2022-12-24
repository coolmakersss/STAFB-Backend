import json
from os import stat
from django.forms import model_to_dict
from STATFB.settings import S3_ADDRESS
from core.api.auth import jwt_auth
from core.api.utils import ErrorCode, failed_api_response, parse_data, response_wrapper, success_api_response
from core.models import CommentStar, Game, Player, PlayerStats, Team, Comment, User
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.db.models import Avg



@response_wrapper
@jwt_auth(perms=[])
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
        tmp = model_to_dict(comment, fields=["id","create_by","create_time", "text"])
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
@jwt_auth(perms=[])
@require_POST
def upload_comment(request: HttpRequest):
    """upload comments for a game

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

@response_wrapper
@jwt_auth(perms=[])
@require_POST
def delete_comment(request: HttpRequest):
    """delete comment for a game

    [route]: /api/comment/delete_comment

    [method]: post
    """
    commentId = parse_data(request)["id"]
    if Comment.objects.filter(id=commentId).first() is None:
        return failed_api_response(ErrorCode.COMMENT_NOT_FOUND ,"该评论不存在或已被删除")
    else:
        Comment.objects.get(id=commentId).delete()
    return success_api_response({'id': commentId})

@response_wrapper
@jwt_auth(perms=[])
@require_POST
def upload_star(request: HttpRequest):
    """upload comment star for a player

    [route]: /api/comment/upload_star

    [method]: post
    """
    data: dict = parse_data(request)
    userId = data.get("create_by")
    gameId = data.get("belong_to")
    playerId = data.get("for_player")
    data["create_by"] = User.objects.filter(id=userId).first()
    data["belong_to"] = Game.objects.filter(id=gameId).first()
    data["for_player"] = Player.objects.filter(id=playerId).first()
    data["score"] = data.get("score")
    ans: CommentStar = CommentStar.objects.create(**data)

    return success_api_response({'id': ans.id})
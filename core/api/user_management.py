"""User Management APIs
"""
from django.apps import apps
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from pymysql import NULL

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            require_item_exist, response_wrapper,
                            success_api_response, wrapped_api, username_checker)
from core.models import UserProfile, User

@response_wrapper
#@jwt_auth(perms=["auth.add_user"])
@require_POST
def create_user(request: HttpRequest):
    """create user

    [method]: POST

    [route]: /api/user/create
    """
    data: dict = parse_data(request)
    print(data)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    username = data.get("username")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    print(email)
    if username is None or password is None or email is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad ID Information.")
    if not username_checker(username):
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Illegal Username.")
    if get_user_model().objects.filter(username=username).exists():
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Username conflicted.")

    new_user = get_user_model().objects.create_user(
        username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_staff=False)
    new_user.save()

    UserProfile.objects.create(**{"user": new_user})

    data = {"id": new_user.id}
    return success_api_response(data)


@response_wrapper
#@jwt_auth(perms=["auth.add_user"])
@require_POST
def lock_user(request: HttpRequest):
    """lock user

    [method]: POST

    [route]: /api/user/lock_user
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    if "userId" in data.keys():
        user = User.objects.get(id=data["userId"])
    elif "userName" in data.keys():
        user = User.objects.get(username=data["userName"])
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user.is_active = 0
    user.save()
    return success_api_response({"id": user.id})

@response_wrapper
#@jwt_auth(perms=["auth.add_user"])
@require_POST
def unlock_user(request: HttpRequest):
    """lock user

    [method]: POST

    [route]: /api/user/unlock_user
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    if "userId" in data.keys():
        user = User.objects.get(id=data["userId"])
    elif "userName" in data.keys():
        user = User.objects.get(username=data["userName"])
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user.is_active = 1
    user.save()
    return success_api_response({"id": user.id})


@response_wrapper
#@jwt_auth(perms=[CORE_EXAM_VIEW])
@require_GET
def list_user(request: HttpRequest):
    """List all players

    [route]: /api/user/list_user

    [method]: GET
    """

    users = UserProfile.objects.all()
    users_count = len(users)
    user_details = []
    for userprofile in users:
        tmp = model_to_dict(userprofile,fields=["home_team"])
        user = userprofile.user
        tmp = model_to_dict(user,exclude=["password"])
        tmp["home_team"] = NULL if userprofile.home_team is None else userprofile.home_team.name_cn
        user_details.append(tmp)

    userInfo = {
        "user_count" : users_count,
        "user_details" : user_details
    }

    return success_api_response(userInfo)
"""User Management APIs
"""
from django.apps import apps
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)

from core.api.auth import jwt_auth
#from core.api.query_utils import query_page, query_filter
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            require_item_exist, response_wrapper,
                            success_api_response, wrapped_api, username_checker)
#from core.models.auth_record import AuthRecord
#from core.models.user_profile import UserProfile

'''
@response_wrapper
@jwt_auth(perms=None)
@require_POST
def change_password(request: HttpRequest):
    """reset password if old password matches

    [method]: POST

    [route]: /api/user/change-password
    """
    user = request.user
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    old_password = data.get("old-password")
    new_password = data.get("new-password")
    if old_password is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Old password required.")
    if new_password is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "New password required.")
    if not user.check_password(old_password):
        return failed_api_response(ErrorCode.REFUSE_ACCESS, "Old password not matched.")
    user.set_password(new_password)
    user.save()
    AuthRecord.objects.filter(user=user).delete()
    return success_api_response({"result": "Ok, password has been updated."})


@response_wrapper
@jwt_auth(perms=["auth.add_user"])
@require_POST
def create_user(request: HttpRequest):
    """create user

    [method]: POST

    [route]: /api/user/create
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    username = data.get("username")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    permission = data.get("permission")
    if username is None or password is None or email is None or permission is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad ID Information.")
    if not username_checker(username):
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Illegal Username.")
    if get_user_model().objects.filter(username=username).exists():
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Username conflicted.")

    permission_all = Permission.objects.all()
    permissions = []
    for perm in permission:
        app_label, codename = perm.split(".")
        perm_obj = permission_all.filter(content_type__app_label=app_label, codename=codename).first()
        if perm_obj is None:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "权限配置不正确，找不到 {}".format(perm))
        permissions.append(perm_obj)

    new_user = get_user_model().objects.create_user(
        username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_staff=True)
    new_user.user_permissions.clear()
    new_user.user_permissions.add(*permissions)
    new_user.save()
    groups: list = data.get('groups', None)
    if groups is not None:
        groups: set = set(filter(lambda x: Group.objects.filter(id=x).first() is not None, groups))
        new_user.groups.clear()
        new_user.groups.add(*groups)

    UserProfile.objects.create(**{"user": new_user})

    data = {"id": new_user.id}

    return success_api_response(data)


@response_wrapper
@jwt_auth(perms=["auth.change_user"])
@require_http_methods(["PUT"])
@require_item_exist(model=get_user_model(), item="user_id", field="id")
def update_user(request: HttpRequest, user_id: int):
    """update user

    [method]: PUT

    [auguments]:
    - groups: required, list of group ids
    - permission: requires, list of permission descriptions

    [route]: /api/user/<int:user_id>
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    permission = data.get("permission")
    groups = data.get('groups')

    if permission is None:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, "permission")
    if groups is None:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, "groups")

    permission_all = Permission.objects.all()
    permissions = []
    for perm in permission:
        app_label, codename = perm.split(".")
        permissions.append(permission_all
                           .filter(content_type__app_label=app_label,
                                   codename=codename)
                           .first())
    user = get_user_model().objects.get(pk=user_id)
    user.user_permissions.clear()
    user.user_permissions.add(*permissions)
    if groups is not None:
        if not isinstance(groups, list):
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR,
                                       "groups should be a list")
        groups = Group.objects.filter(id__in=set(groups))
        user.groups.clear()
        user.groups.add(*groups)
    user.save()
    return success_api_response({"result": "Ok, user update successfully."})


@response_wrapper
@jwt_auth(perms=["auth.delete_user"])
@require_http_methods(["DELETE"])
def delete_user(request: HttpRequest):
    """delete user

    [method]: DELETE

    [route]: /api/user/delete
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    username = data.get("username")
    if not username:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad ID Information.")
    user = get_user_model().objects.filter(username=username).first()
    if not user:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "No such user.")
    user.delete()
    return success_api_response({"result": "Ok, user disabled."})
    '''
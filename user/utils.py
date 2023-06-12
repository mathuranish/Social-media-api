import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException
from django.conf import settings
from rest_framework import status
from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

class APIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Validation Error"
    default_code = "error"

    def __init__(self, detail=None, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        super().__init__(detail, code)

def get_response(
    data={},
    message="",
    error="",
    error_list=[],
    status_code=status.HTTP_200_OK,
    headers={},
):
    response_data = {
        "data": data,
        "message": message,
        "error": error,
        "error_list": error_list,
        "status": status_code,
    }
    return Response(
        response_data,
        status=status_code,
        headers=headers,
    )
class ListPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 200

    def get_paginated_response(self, data):
        return get_response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    data = {}
    data["refresh"] = str(refresh)
    access_token = str(refresh.access_token)
    decodeJTW = jwt.decode(str(access_token), settings.SECRET_KEY, algorithms=["HS256"])

    # add payload here!!
    decodeJTW["user_id"] = user.id
    decodeJTW["name"] = user.name
    decodeJTW["email"] = user.email
    encoded = jwt.encode(decodeJTW, settings.SECRET_KEY, algorithm="HS256")

    data["access"] = encoded
    return data

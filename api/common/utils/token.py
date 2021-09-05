from rest_framework.authtoken.models import Token


def get_token_from_request(request):
    return request.META.get('HTTP_AUTHORIZATION').split(" ")[1]


def get_user_by_token(token):
    return Token.objects.get(key=token).user
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.common.http.request import Request
from api.common.utils.storage import Storage
from api.common.logging.logging import log

from api.disk_space.service import DiskSpaceService

@csrf_exempt
@api_view(['POST'])
def login(request):
    
    body = Request().parse_body(request.body)

    if not body.has_fields(['username', 'password']):
        return Response({
            "status": False,
            "reason": "Invalid body"
        })

    try:

        user = authenticate(
            request, 
            username = body.get('username'),
            password = body.get('password')
        )

        if user:

            token = Token.objects.get(user=user)

            return Response({
                "status": True,
                "token": token.key
            })

        else:
            return Response({
                "status": False,
                "reason": "User does not exist"
            })

    except Exception as e:
        return Response({
            "status": False,
            "reason": "Unexpected error",
            "inner_reason": str(e)
        })


@csrf_exempt
@api_view(['POST'])
def register(request):
    body = Request().parse_body(request.body)

    if not body.has_fields(['username', 'password']):
        return Response({
            "status": False,
            "reason": "Invalid body"
        })

    try:

        user = User.objects.create_user(
            username = body.get('username'),
            password = body.get('password')
        )


        # Folder´s name is username of the user we create before 
        Storage(user.username).create_folder()

        token = Token.objects.create(user=user)

        DiskSpaceService.save(user)

        if user:

            log.info("User created -> ", user.username)

            return Response({
                "status": True,
                "token": token.key
            })

    except Exception as e:
        return Response({
            "status": False,
            "reason": "User already exists",
            "inner_reason": str(e)
        })
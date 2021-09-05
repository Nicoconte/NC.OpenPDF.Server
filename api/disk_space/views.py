from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .service import DiskSpaceService

from api.common.utils.token import ( 
    get_token_from_request,
    get_user_by_token
)

# Create your views here.
@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["GET"])
def get_disk_space(request):
    token = get_token_from_request(request)
    user  = get_user_by_token(token)

    disk_space_obj = DiskSpaceService.get_disk_space_information(user)

    if disk_space_obj:
        return Response({
            "status": True,
            "data": {
                "id": disk_space_obj.id,
                "limit": disk_space_obj.limit,
                "space_used": disk_space_obj.space_used,
                "space_remaining":  disk_space_obj.limit - disk_space_obj.space_used
            }
        })        
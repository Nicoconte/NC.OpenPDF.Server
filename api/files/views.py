from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, api_view
from rest_framework.authentication import TokenAuthentication

from api.common.utils.storage import Storage

from api.common.utils.token import ( 
    get_token_from_request,
    get_user_by_token
)

from api.disk_space.service import DiskSpaceService

from .services import FileService



storage = Storage()

@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def upload_file(request):
    files = request.FILES.getlist('files')

    if len(files) <= 0:
        return Response({
            "status": False,
            "reason": "There's no files"
        })

    token = get_token_from_request(request)
    user  = get_user_by_token(token)    

    files_size = FileService.get_blob_files_size(files)

    if not DiskSpaceService.is_there_space_into_the_disk(user, files_size):
        return Response({
            "status": False,
            "reason": "There's no space remaining in your account. Delete some files"
        })        

    storage.init(user.username)  

    try:
        files_success = []        
        files_error    = []

        #Save multiple files associated with one user 
        files_success, files_error = FileService.save_many(user, files, storage)

        DiskSpaceService.update_disk_space(user, files_size, True)

        return Response({
            "status": True,
            "data": {
                "success": files_success,
                "error": files_error
            } 
         })

    except Exception as e:
        return Response({
            "status": False,
            "reason": "Unexpected error",
            "inner_reason": str(e)
        })


@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["DELETE"])
def delete_file(request, id):

    token = get_token_from_request(request)
    user  = get_user_by_token(token)    

    storage.init(user.username)  

    file = FileService.find_by_id(id)

    FileService.delete(id)

    if not file:
        return Response({
            "status": False,
            "reason": "File does not exist"
        })

    deleted = storage.delete_file(file.filename)

    DiskSpaceService.update_disk_space(user, storage.calculate_disk_space())

    if deleted:
        return Response({
            "status": True
        })


@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["GET"])
def list_files(request):

    token = get_token_from_request(request)
    user  = get_user_by_token(token)    

    files = FileService.find_all(user)
    
    file_response = []

    for file in files:
       
        file_response.append({
            "id": file.id,
            "filename": file.filename,
            "extension": file.extension,
            "path": file.path,
            "size": file.size,
            "uploaded_at": file.uploaded_at
        })

    return Response({
        "status": True,
        "data": file_response
    })

@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["GET"])
def download_file(request, id):

    token = get_token_from_request(request)
    user  = get_user_by_token(token)    

    storage.init(user.username)  

    file = FileService.find_by_id(id)

    if not file:
        return Response({
            "status": False,
            "reason": "File does not exist"
        })

    blob = storage.get_file_blob(file.filename)

    response = HttpResponse(blob, content_type="audio/mpeg")
    response['Content-Disposition'] = 'attachment; filename="%s"' % file.filename

    return response


@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def remove_every_file(request):
    token = get_token_from_request(request)
    user  = get_user_by_token(token)    
    
    try:
        storage.init(user.username)

        storage.clear_dir()

        FileService.delete_all(user)


        DiskSpaceService.update_disk_space(user, storage.calculate_disk_space())

        return Response({
            "status": True
        })
    
    except Exception as e:
        return Response({
            "status": False,
            "reason": "Unexpected error",
            "inner_reason": str(e) 
        })

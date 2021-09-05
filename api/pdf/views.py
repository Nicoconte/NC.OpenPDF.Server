from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, api_view
from rest_framework.authentication import TokenAuthentication

from api.common.open_pdf_helper.pdf import PDF
from api.common.open_pdf_helper.image import Image
from api.common.utils.storage import Storage

from api.common.utils.token import ( 
    get_token_from_request,
    get_user_by_token
)

from api.files.services import FileService

from uuid import uuid4

import json

@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def merge_pdf(request):
    body = json.loads(request.body)

    pdf_id = body['files_id'] # Reference to PDF uploaded before

    if len(pdf_id) < 2:
        return Response({
            "status": False,
            "reason": "You need at least 2 files to merge"
        })

    # Process user from token
    token = get_token_from_request(request)
    user  = get_user_by_token(token)

    # Build output path for pdf file
    output_path = Storage.build_path(user.username) 
    
    pdf = PDF(output_path)
    
    # Build output pdf information
    file_id = str(uuid4())
    filename = f"{file_id}.pdf"

    # Get every path from file by id
    pdf_paths = FileService.build_files_fullpath(pdf_id)

    # Merge them
    saved = pdf.merge(pdf_paths, filename)

    fileObj = FileService.save(user, filename, output_path)

    if saved:
        return Response({
            "status": True,
            "data": {
                "id": fileObj.id, 
                "transaction_id": file_id
            }
        })    
    
    return Response({
        "status": False,
        "reason": "Cannot merge"
    })

@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def encrypt_pdf(request):
    body = json.loads(request.body)
    
    pdf_id = body['file_id']
    password = body['password']
    
    # Process user from token
    token = get_token_from_request(request)
    user  = get_user_by_token(token)

    # Build output path for pdf file
    output_path = Storage.build_path(user.username) 
    
    pdf = PDF(output_path)
    
    # Build output pdf information
    new_file_id = str(uuid4())
    new_filename = f"{new_file_id}.pdf"
    
    fileObj = FileService.find_by_id(pdf_id)
    output_path = f"{fileObj.path}/{fileObj.filename}"

    encrypted = pdf.encrypt(output_path, password, new_filename)
    
    #Save and use ID to download Output PDF file. After operation, we'll be deleting it 
    fileObj = FileService.save(user, new_filename, output_path) 

    if encrypted:
        return Response({
            "status": True,
            "data": {
                "id": fileObj.id, 
                "transaction_id": new_file_id
            }
        })

    return Response({
        "status": False,
        "reason": "Cannot encrypt file"
    })


@csrf_exempt
@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def convert_img_to_pdf(request):
    body = json.loads(request.body)
    
    images_id = body['files_id']
    
    # Process user from token
    token = get_token_from_request(request)
    user  = get_user_by_token(token)

    # Build output path for pdf file
    output_path = Storage.build_path(user.username) 

    images_path = FileService.build_files_fullpath(images_id)

    file_id = str(uuid4())
    filename = f"{file_id}.pdf"

    image = Image(output_path)
    converted = image.convert_to_pdf(images_path, filename)

    fileObj = FileService.save(user, filename, output_path)

    if converted:
        return Response({
            "status": True,
            "data": {
                "id": fileObj.id,
                "transaction_id": file_id
            }
        })

    return Response({
        "status": False,
        "reason": "Cannot convert images to pdf"
    })
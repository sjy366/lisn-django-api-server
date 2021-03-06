from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Share
from api.utils import coerce_to_post
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_note_id_shared

@auth_note_id_shared
def make_sharing(request):
    note_id = int(request.POST.get('note_id'))
    email = str(request.POST.get('email'))

    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse('No Matching Users', status=400)

    user = User.objects.get(email=email)
    note = Note.objects.get(id=note_id)

    if note.user.id == user.id:
        return HttpResponse('Already Exist', status=400)

    share = Share.objects.filter(note_id=note_id, user_id=user.id)

    if share.exists():
        return HttpResponse('Already Exist', status=400)
    else:
        Share.objects.create(
        note_id=note_id,
        user_id=user.id
        )
        return HttpResponse(status=201)

@auth_user_id
@auth_note_id_shared
def delete_sharing(request):
    coerce_to_post(request)
    note_id = int(request.DELETE.get('note_id'))
    user_id = int(request.DELETE.get('user_id'))
    
    share = Share.objects.filter(note_id=note_id, user_id=user_id)
    share.delete()

    return HttpResponse(status=200)

@auth_note_id
def delete_sharing_master(request):
    coerce_to_post(request)
    note_id = int(request.DELETE.get('note_id'))
    user_id = int(request.DELETE.get('user_id'))
    
    share = Share.objects.filter(note_id=note_id, user_id=user_id)
    share.delete()

    return HttpResponse(status=200)

@log
def api_note_shared(request):
    try:
        if request.method == 'POST':
            return make_sharing(request)
        elif request.method == 'DELETE':
            return delete_sharing(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_note_shared_master(request):
    try:
        if request.method == 'DELETE':
            return delete_sharing_master(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

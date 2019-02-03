from django.shortcuts import render
from .models import *
from . import logic
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def create_user(request):
    u = CustomUser()
    u.save()
    return JsonResponse({'status': 'success',
                         'user_id': u.pk})


@csrf_exempt
def follow_user(request):
    if request.method=="POST":
        status, users = logic.validate_users(
            [request.POST['follower'], request.POST['following']])
        if not status:
            return JsonResponse(
                {'status': 'fail', 'reason': 'User {} does not exist'.format(users[0])})
        else:
            follower, following = users
            status = follower.follow(following)
            return JsonResponse(status)
    else:
        return JsonResponse(
                {'status': 'fail', 'reason': 'invalid request'})

@csrf_exempt
def unfollow_user(request):
    if request.method=="POST":
        status, users = logic.validate_users(
            [request.POST['follower'], request.POST['following']])
        if not status:
            return JsonResponse(
                {'status': 'fail', 'reason': 'User {} does not exist'.format(users[0])})
        else:
            follower, following = users
        status = follower.unfollow(following)
        return JsonResponse(status)
    else:
        return JsonResponse(
                {'status': 'fail', 'reason': 'invalid request'})

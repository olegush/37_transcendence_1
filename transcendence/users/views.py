from django.conf import settings
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from sentry_sdk import capture_exception


def show_user(request, user_id):
    return render(request, 'user.html', context={'user_id': user_id})

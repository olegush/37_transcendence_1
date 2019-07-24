from django.conf import settings
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse

def index(request):
    return HttpResponse("index")

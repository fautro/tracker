from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is a future weight tracker.")

def about(request):
    return HttpResponse("This is a future \"About\" page.")

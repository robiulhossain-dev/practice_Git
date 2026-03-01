from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Django")

def show_task(request):
    return HttpResponse("<h1>This is our task page</h1>")


def specific_task(request, id):
    return HttpResponse("<h1>This is our spacefic task</h1>")
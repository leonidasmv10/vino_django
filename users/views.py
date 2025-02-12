from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def login(request):
    template = loader.get_template("users/login.html")
    return HttpResponse(template.render())


def register(request):
    template = loader.get_template("users/register.html")
    return HttpResponse(template.render())

def ranking(request):
    template = loader.get_template("users/ranking.html")
    return HttpResponse(template.render())

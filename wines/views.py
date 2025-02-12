from django.http import HttpResponse
from django.template import loader


def store(request):
    template = loader.get_template("wines/store.html")
    return HttpResponse(template.render())

def collection(request):
    template = loader.get_template("wines/collection.html")
    return HttpResponse(template.render())

def cata(request):
    template = loader.get_template("wines/cata.html")
    return HttpResponse(template.render())
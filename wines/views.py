from django.shortcuts import render


def store(request):
    return render(request, "wines/store.html")


def collection(request):
    return render(request, "wines/collection.html")


def cata(request):
    return render(request, "wines/cata.html")

from django.shortcuts import render


def home(request):
    """Home page view displaying FMU Control Panel - Dev"""
    return render(request, 'home.html')

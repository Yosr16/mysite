from django.shortcuts import render
from django.contrib.auth import views as va

def index(request):
    return render(request, 'acceuil.html')

""" def logout_view(request):
    va.LogoutView(request)
    return render(request, 'registration/logout.html') """
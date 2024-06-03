from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def game_page(request):
    return HttpResponse("Hello world, game time!")

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('login')
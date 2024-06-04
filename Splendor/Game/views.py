from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import GameSession, Player

import string
import random

def game_page(request):
    return HttpResponse("Hello world, game time!")

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('login')

def new_game(request):
    if request.user.is_authenticated:
        return render(request, 'new_game.html')
    else:
        return redirect('login')

def create_game(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a new game session
            form_data = request.POST.dict()
            num_players = form_data.get("num_players")
            new_game_id = generate_game_id()

            context = {"num_players": num_players, "game_id": new_game_id, "game_master_id": request.user.id}
            return render(request, 'waiting_room.html', context)
        

def join_game(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Join an existing game session
            form_data = request.POST.dict()
            game_id = form_data.get("game_id")

            context = {"game_id": game_id}
            return render(request, 'waiting_room.html', context)

def generate_game_id(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def form_new_board():
    pass


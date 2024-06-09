from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import GameSession, Player, WaitingRoom

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
        new_game_id = generate_game_id()
        return render(request, 'new_game.html', context={"game_id": new_game_id})
    else:
        return redirect('login')

def create_game(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a new game session
            form_data = request.POST.dict()
            num_players = form_data.get("num_players")
            new_game_id = form_data.get("game_id")
            WaitingRoom.objects.create(game_id=new_game_id, game_master_id=request.user.id, num_players=num_players)
            return redirect('join_waiting_room', game_id=new_game_id)

def join_waiting_room(request, game_id):
    if request.user.is_authenticated:
        waiting_room = WaitingRoom.objects.get(game_id=game_id)
        players = []
        num_players = 0
        if waiting_room.game_master_id != request.user.id:
            if waiting_room.num_players > waiting_room.get_num_players_joined():
                players = waiting_room.get_player_usernames()
                num_players = waiting_room.get_num_players_joined()
            else:
                return HttpResponse("Game is full")
        
        return render(request, 'waiting_room.html', context={"game_id": game_id, "game_master_id": waiting_room.game_master_id, "max_players": waiting_room.num_players, "num_players": num_players, "players":players})
        
    else:
        return redirect('login')
                
def join_game(request, game_id):
    return HttpResponse(f"Entering game {game_id}....")
    
def generate_game_id(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    print("Length: ",  length)
    id = ''.join(random.choice(letters_and_digits) for _ in range(length))
    print(id)
    return id

def form_new_board():
    pass


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
            waiting_room = WaitingRoom.objects.create(game_id=new_game_id, game_master_id=request.user.id, num_players=num_players)
            context = {"num_players": num_players, "game_id": new_game_id, "game_master_id": request.user.id}
            return redirect('join_waiting_room', game_id=new_game_id)

def join_waiting_room(request, game_id):
    if request.user.is_authenticated:
        waiting_room = WaitingRoom.objects.get(game_id=game_id)
        if not waiting_room.has_already_joined(request.user.id):
            if waiting_room.game_master_id != request.user.id:
                if waiting_room.num_players > waiting_room.get_num_players_joined():
                    waiting_room.add_player(request.user.id)
                else:
                    return HttpResponse("Game is full")
                    
                return render(request, 'waiting_room.html', context={"game_id": game_id, "game_master_id": waiting_room.game_master_id})
                

        return render(request, 'waiting_room.html', context={"game_id": game_id, "game_master_id": waiting_room.game_master_id})
        
    else:
        return redirect('login')
                


def join_game(request):
    pass
    
def generate_game_id(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    print("Length: ",  length)
    id = ''.join(random.choice(letters_and_digits) for _ in range(length))
    print(id)
    return id

def form_new_board():
    pass


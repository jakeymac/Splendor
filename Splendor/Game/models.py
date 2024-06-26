from django.db import models
import json
import random

from django.contrib.auth.models import User

class WaitingRoom(models.Model):
    game_id = models.CharField(max_length=20)
    game_master_id = models.IntegerField()
    num_players = models.IntegerField()
    players = models.CharField(max_length=1000)

    def get_num_players_joined(self):
        if self.players == '':
            return 0
        return len(self.players.split(','))
    
    def get_player_ids(self):
        return self.players.split(',')

    def get_player_usernames(self):
        if self.get_num_players_joined() == 0:
            return []

        ids = self.get_player_ids()
        usernames = []
        for id in ids:
            usernames.append(User.objects.get(id=id).username)

        return usernames

    def has_already_joined(self, user_id):
        return str(user_id) in self.players.split(',')

    def add_player(self, user_id):
        if self.get_num_players_joined() > 0:
            self.players += ","
        self.players += str(user_id)
        self.save()

    def remove_player(self, user_id):
        players = self.players.split(',')
        players.remove(str(user_id))
        self.players = ','.join(players)
        self.save()

class GameSession(models.Model):
    board = models.CharField(max_length=1000)
    gems_available = models.CharField(max_length=500)
    nobles = models.CharField(max_length=200)
    players = models.CharField(max_length=150)
    current_turn = models.OneToOneField('Player', on_delete=models.CASCADE, related_name='current_turn')

    def get_board(self):
        return json.loads(self.board)

    def set_board(self, board):
        self.board = json.dumps(board)

    def get_gems_available(self):
        return json.loads(self.gems_available)
    
    def set_gems_available(self, gems_available):
        self.gems_available = json.dumps(gems_available)
    
    def get_nobles(self):
        return json.loads(self.nobles)

    def set_nobles(self, nobles):
        self.nobles = json.dumps(nobles)
    
    def get_players(self):
        return json.loads(self.players)

    def generate_new_board(self):
        # cards
        level1_cards = Card.objects.filter(level=1)
        indices = [i for i in range(len(level1_cards))]
        random.shuffle(indices)

        row_1 = [str(card) for card in level1_cards[indices[0:4]]]
        stack_1 = [str(card) for card in level1_cards[indices[4:]]]

        level2_cards = Card.objects.filter(level=2)
        indices = [i for i in range(len(level2_cards))]
        random.shuffle(indices)
        row_2 = [str(card) for card in level2_cards[indices[0:4]]]
        stack_2 = [str(card) for card in level2_cards[indices[4:]]]

        level3_cards = Card.objects.filter(level=3)
        indices = [i for i in range(len(level3_cards))]
        row_3 = [str(card) for card in level3_cards[indices[0:4]]]
        stack_3 = [str(card) for card in level3_cards[indices[4:]]]

        


class Player(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    points = models.IntegerField()
    gems = models.CharField(max_length=100)
    purchased_cards = models.CharField(max_length=1000)
    reserved_cards = models.CharField(max_length=1000)
    nobles = models.CharField(max_length=200)
    is_turn = models.BooleanField()

    def get_gems(self):
        return json.loads(self.gems)
    
    def set_gems(self, gems):
        self.gems = json.dumps(gems)

    def get_cards(self):
        return json.loads(self.purchased_cards)
    
    def set_purchased_cards(self, purchased_cards):
        self.purchased_cards = json.dumps(purchased_cards)

    def get_reserved_cards(self):
        return json.loads(self.reserved_cards)
    
    def set_reserved_cards(self, reserved_cards):
        self.reserved_cards = json.dumps(reserved_cards)

    def get_nobles(self):
        return json.loads(self.nobles)
    
    def set_nobles(self, nobles):
        self.nobles = json.dumps(nobles)

    
class Card(models.Model):
    level = models.IntegerField()
    points = models.IntegerField()
    gem = models.CharField(max_length=20, 
        choices=[('diamond', 'Diamond'), 
                 ('sapphire', 'Sapphire'), 
                 ('emerald', 'Emerald'), 
                 ('ruby', 'Ruby'), 
                 ('onyx', 'Onyx')]
    )
    cost = models.CharField(max_length=100)
    
    def get_cost(self):
        return json.loads(self.cost)

    def set_cost(self, cost):
        self.cost = json.dumps(cost)

    def __str__(self):
        return f'Level {self.level},{self.gem}, {self.points} points, cost: {self.cost}'


class Noble(models.Model):
    points = models.IntegerField()
    cost = models.CharField(max_length=100)
    
    def get_cost(self):
        return json.loads(self.cost)

    def set_cost(self, cost):
        self.cost = json.dumps(cost)

    def __str__(self):
        return f"{self.points} points, cost: {self.cost}"



    







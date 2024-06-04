from django.db import models
import json

# Create your models here.

class WaitingRoom(models.Model):
    game_id = models.CharField(max_length=20)
    game_master_id = models.IntegerField()
    num_players = models.IntegerField()
    players = models.CharField(max_length=1000)

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
    
    def set_players(self, players):
        self.players = json.dumps(players)


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



    







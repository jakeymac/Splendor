from django.contrib import admin
from .models import GameSession, Player, Card, Noble, WaitingRoom
# Register your models here.
admin.site.register(GameSession)
admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Noble)
admin.site.register(WaitingRoom)
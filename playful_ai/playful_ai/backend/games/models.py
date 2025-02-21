from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=100) #type: ignore
    created_at = models.DateTimeField(auto_now_add=True)#type: ignore

    def __str__(self):
        return self.name

class GameMove(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)#type: ignore
    move_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)#type: ignore

    def __str__(self):
        return f"Move for {self.game.name} at {self.timestamp}"

class GameHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#type: ignore
    game_data = models.TextField() #type: ignore
    created_at = models.DateTimeField(auto_now_add=True)#type: ignore

    def __str__(self):
        return f"Game history for {self.user.username} on {self.created_at}"

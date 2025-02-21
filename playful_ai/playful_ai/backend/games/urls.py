from django.urls import path
from games.views import (
    get_moves,
    get_chess_move,
    poker_advice,
    chatbot,
    analyze_game,
    get_history
)
from .views import chatbot 

urlpatterns = [
    path("api/moves/<int:game_id>/", get_moves, name="get_moves"),
    path("api/chess-ai-move/", get_chess_move, name="get_chess_move"),
    path("api/poker-advice/", poker_advice, name="poker_advice"),
    path("api/chatbot/", chatbot, name="chatbot"),
    path("api/analyze-game/", analyze_game, name="analyze_game"),
    path("api/get-history/", get_history, name="get_history"),
     path("chatbot/", chatbot, name="chatbot"),
]

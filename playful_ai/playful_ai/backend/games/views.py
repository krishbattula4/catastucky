import os
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stockfish import Stockfish #type: ignore
from django.conf import settings
from django.contrib.auth.decorators import login_required
from games.models import GameHistory
from django.http import JsonResponse

def chatbot(request):
    """
    A simple chatbot API endpoint that returns a placeholder response.
    """
    response_data = {"message": "Hello! How can I assist you?"}
    return JsonResponse(response_data)


# Load Stockfish Engine
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", "backend/stockfish.exe")

try:
    stockfish = Stockfish(STOCKFISH_PATH)
    stockfish.set_skill_level(10)
    print("✅ Stockfish initialized successfully.")
except Exception as e:
    print(f"❌ Error initializing Stockfish: {e}")
    raise

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# AI Chess Analysis
def get_gemini_analysis(fen, best_move):
    prompt = f"""
    Given the chess position (FEN): {fen}, the best move suggested by Stockfish is {best_move}.
    Explain why this move is the best choice in simple terms.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response else "No analysis available."
    except Exception as e:
        print(f"❌ Error with Gemini API: {e}")
        return "Error generating analysis."

# API: Get AI Chess Move
@api_view(["POST"])
def get_chess_move(request):
    board_state = request.data.get("fen")
    difficulty = request.data.get("difficulty", 10)

    if not board_state:
        return Response({"error": "FEN string is required"}, status=400)

    try:
        stockfish.set_fen_position(board_state)
        stockfish.set_skill_level(int(difficulty))
        best_move = stockfish.get_best_move()
        explanation = get_gemini_analysis(board_state, best_move)

        return Response({
            "best_move": best_move,
            "analysis": explanation,
            "difficulty": difficulty
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# API: Get AI Poker Advice
@csrf_exempt
def poker_advice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = f"Analyze this poker situation: {json.dumps(data, indent=2)}"
            response = model.generate_content(prompt)
            return JsonResponse({"advice": response.text.strip()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# API: AI Chess Game Analysis
@csrf_exempt
def analyze_game(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fen = data.get("fen", "")
            prompt = f"Analyze this chess position: {fen}."
            response = model.generate_content(prompt)
            return JsonResponse({"commentary": response.text.strip()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# API: Get Move History
def get_moves(request, game_id):
    return JsonResponse({"moves": [{"move_data": f"Move {i} for game {game_id}"} for i in range(1, 3)]})

# API: Get User Game History
@login_required
def get_history(request):
    history = GameHistory.objects.filter(user=request.user).values("game_data", "created_at")
    return JsonResponse(list(history), safe=False)

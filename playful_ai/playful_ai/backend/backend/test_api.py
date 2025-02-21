import requests

BASE_URL = "http://127.0.0.1:8000/games/"

# Test Save Move
save_response = requests.post(BASE_URL + "save-move/", json={"game_id": 1, "move_data": "Knight to F3"})
print("Save Move Response:", save_response.json())

# Test Get Moves
get_response = requests.get(BASE_URL + "get-moves/1/")
print("Get Moves Response:", get_response.json())

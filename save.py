import json, os

SAVE_FILE = "save.json"

def save_game(coins, wins, better_fireball_counter, player_health, increased_push_counter):
    data = {
        "coins": coins,
        "wins": wins,
        "better_fireball_counter": better_fireball_counter,
        "player_health": player_health,
        "increased_push_counter": increased_push_counter
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return (
            data.get("coins", 50),
            data.get("wins", 0),
            data.get("better_fireball_counter", 0),
            data.get("increased_push_counter", 0),
            data.get("player_health", 100)
        )
    else:
        return 50, 0, 0, 0, 100,   # defaults

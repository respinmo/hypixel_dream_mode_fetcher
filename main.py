import re
import requests
import configparser

game_modes = {
    "lucky": {
    },
    "armed":{
    },
    "swap": {
    },
    "ultimate": {
    },
    "voidless": {
    },
    "rush": {
    },
    "underworld": {
    },
    "castle": {
    }
}


def create_blank_config_file(filename):
    config = configparser.ConfigParser()
    config["ACCESS"] = {
        "hypixel_api_token" : "your_key"
    }
    with open(filename, "w") as f:
        config.write(f)


def get_api_key_from_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config["ACCESS"]["hypixel_api_token"]


def get_hypixel_playercount(api_key):
    headers = {
        "API-Key": api_key
    }
    response = requests.get("https://api.hypixel.net/counts", headers=headers)
    return response


def get_all_dream_mode_names():
    results = []
    for i in game_modes:
        if i != "castle":
            results.append("BEDWARS_FOUR_FOUR_" + i.upper())
            results.append("BEDWARS_EIGHT_TWO_" + i.upper())
        else:
            results.append("BEDWARS_CASTLE")
    return results


def get_dream_modes_count(count_json):
    bedwars_modes = count_json["games"]["BEDWARS"]
    dream_mode_names = get_all_dream_mode_names()
    played_dream_modes = {}
    for i in bedwars_modes["modes"].items():
        if i[0] in dream_mode_names:
            played_dream_modes[i[0]] = i[1]
    return played_dream_modes


def extract_highest_dream_game_mode(count_json):
    dream = get_dream_modes_count(count_json)
    maxmode = (max(dream, key=lambda k: dream[k]))
    maxmode = re.sub("(BEDWARS_FOUR_FOUR_|BEDWARS_EIGHT_TWO_|BEDWARS_)", "", maxmode).lower()
    return maxmode


if __name__ == '__main__':
    json = get_hypixel_playercount(get_api_key_from_file("config.ini")).json()
    print(extract_highest_dream_game_mode(json))
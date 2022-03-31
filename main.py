#!/usr/bin/env python3
import re
import requests
import configparser
import argparse
import sys
import datetime

regular_game_modes = ["BEDWARS_TWO_FOUR", "BEDWARS_EIGHT_ONE", "BEDWARS_EIGHT_TWO"
    , "BEDWARS_FOUR_FOUR", "BEDWARS_EIGHT_TWO_TOURNEY", "BEDWARS_FOUR_THREE"]


def create_blank_config_file(filename):
    config = configparser.ConfigParser()
    config["ACCESS"] = {
        "hypixel_api_token": "your_key"
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


def get_hypxiel_game_modes(api_key):
    headers = {
        "API-Key": api_key
    }
    response = requests.get("https://api.hypixel.net/resources/games", headers=headers)
    return response.json()["games"]["BEDWARS"]["modeNames"]


def get_all_dream_mode_names(config_file="config.ini"):
    results = []
    game_modes = get_hypxiel_game_modes(get_api_key_from_file(config_file))
    for i in game_modes.keys():
        if i not in regular_game_modes:
            results.append(i)
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


def check_api_working(api_key):
    headers = {
        "API-Key": api_key
    }
    response = requests.get("https://api.hypixel.net/key", headers=headers)
    if response.json()["success"]:
        return True
    else:
        return False


def parse_all_args():
    parser = argparse.ArgumentParser(description="Fetch current Hypixel Bedwars dream Gamemode",
                                     epilog="Overengineered? - no...")
    parser.add_argument("configfile", nargs="?", default="config.ini", help="The config file to be used")
    parser.add_argument("--history", default="history.txt", help="The history file to be used(TBI)")
    parser.add_argument("--all", default=False, action="store_true", help="Display All Dream Game Modes along with player Count")
    return parser.parse_args()


def create_config_file_dialog(config_file_name):
    while True:
        choice = input("No config file with specified name found. Create \"" + config_file_name + "\"?(y/n)")
        if choice == "y":
            print("config file created, please fill in your api key now")
            create_blank_config_file(config_file_name)
            exit(0)
        elif choice == "n":
            exit(1)


def main():
    args = parse_all_args()
    api_key = ""
    config_file_name = args.configfile
    try:
        with open(config_file_name) as f:
            api_key = get_api_key_from_file(config_file_name)
    except IOError:
        if not re.match("(.*).ini", config_file_name):
            config_file_name = config_file_name + ".ini"
        create_config_file_dialog(config_file_name)
    if not check_api_working(api_key):
        print("Your api key doesn't work, please verify that everything is in order")
        exit(2)
    json = get_hypixel_playercount(api_key).json()
    if args.all:
        for i in get_dream_modes_count(json).items():
            print(i[0]+ ": " + str(i[1]))

    else:
        print(extract_highest_dream_game_mode(json))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import re
import requests
import configparser
import argparse

# list all the non-dream gamemodes, to exclude them from count.
# This allows to prepare for dream modes that may be added in the future
REGULAR_GAME_MODES = ["BEDWARS_TWO_FOUR", "BEDWARS_EIGHT_ONE", "BEDWARS_EIGHT_TWO"
    , "BEDWARS_FOUR_FOUR", "BEDWARS_EIGHT_TWO_TOURNEY", "BEDWARS_FOUR_THREE"]
API_ENDPOINT_URLS = {
    "api_key": "https://api.hypixel.net/key",
    "games": "https://api.hypixel.net/resources/games",
    "playercount": "https://api.hypixel.net/counts"
}
VERBOSE_MODE = False


# basic setup functions
def parse_all_args():
    parser = argparse.ArgumentParser(description="Fetch current Hypixel Bedwars dream Gamemode",
                                     epilog="Overengineered? - no...")
    parser.add_argument("configfile", nargs="?", default="config.ini", help="The config file to be used")
    parser.add_argument("--key", required=False, help="manually provided API-Key")
    parser.add_argument("--history", default="history.txt", help="The history file to be used(TBI)")
    parser.add_argument("--all", default=False, action="store_true",
                        help="Display All Dream Game Modes along with player Count")
    return parser.parse_args()


# setting up and reading config file
def create_blank_config_file(filename):
    config = configparser.ConfigParser()
    config["ACCESS"] = {
        "hypixel_api_token": "your_key"
    }
    config["API_CONFIG"] = API_ENDPOINT_URLS
    with open(filename, "w") as f:
        config.write(f)


def create_config_file_dialog(config_file_name):
    while True:
        choice = input("No config file with specified name found. Create \"" + config_file_name + "\"?(y/n)")
        if choice == "y":
            print("config file created, please fill in your api key now")
            create_blank_config_file(config_file_name)
            exit(0)
        elif choice == "n":
            exit(1)


def get_api_key_from_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config["ACCESS"]["hypixel_api_token"]


def read_and_replace_url_dict(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    global API_ENDPOINT_URLS
    API_ENDPOINT_URLS = config["API_CONFIG"]


# checking for correctness of elements
def check_api_key_working(api_key):
    headers = {
        "API-Key": api_key
    }
    response = requests.get(API_ENDPOINT_URLS["api_key"], headers=headers)
    if response.json()["success"]:
        return True
    else:
        return False


# api accessing functions
def get_hypixel_playercount(api_key):
    headers = {
        "API-Key": api_key
    }
    response = requests.get(API_ENDPOINT_URLS["playercount"], headers=headers)
    return response


def get_hypxiel_game_modes(api_key):
    headers = {
        "API-Key": api_key
    }
    response = requests.get(API_ENDPOINT_URLS["games"], headers=headers)
    return response.json()["games"]["BEDWARS"]["modeNames"]


def get_all_dream_mode_names(api_key):
    results = []
    game_modes = get_hypxiel_game_modes(api_key)
    for i in game_modes.keys():
        if i not in REGULAR_GAME_MODES:
            results.append(i)
    return results


def get_dream_modes_count(count_json, api_key):
    bedwars_modes = count_json["games"]["BEDWARS"]
    dream_mode_names = get_all_dream_mode_names(api_key)
    played_dream_modes = {}
    for i in bedwars_modes["modes"].items():
        if i[0] in dream_mode_names:
            played_dream_modes[i[0]] = i[1]
    return played_dream_modes


# data processing
def extract_highest_dream_game_mode(count_json, api_key):
    dream = get_dream_modes_count(count_json, api_key)
    maxmode = (max(dream, key=lambda k: dream[k]))
    maxmode = re.sub("(BEDWARS_FOUR_FOUR_|BEDWARS_EIGHT_TWO_|BEDWARS_)", "", maxmode).lower()
    return maxmode


# main routine functions

def try_read_create_config_file(config_file_name):
    try:
        with open(config_file_name) as f:
            return get_api_key_from_file(config_file_name)
    except IOError:
        if not re.match("(.*).ini", config_file_name):
            config_file_name = config_file_name + ".ini"
        create_config_file_dialog(config_file_name)


def main():
    args = parse_all_args()
    api_key = ""
    if not args.key:
        config_file_name = args.configfile
        api_key = try_read_create_config_file(config_file_name)
        read_and_replace_url_dict(config_file_name)
        print(API_ENDPOINT_URLS)
    elif args.key:
        api_key = args.key

    if not check_api_key_working(api_key):
        print("Your api key doesn't work, please verify that everything is in order")
        exit(2)
    json = get_hypixel_playercount(api_key).json()
    if args.all:
        for i in get_dream_modes_count(json, api_key).items():
            print(i[0] + ": " + str(i[1]))
    else:
        print(extract_highest_dream_game_mode(json, api_key))


if __name__ == '__main__':
    main()

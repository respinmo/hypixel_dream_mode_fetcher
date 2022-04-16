#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests
import configparser
import argparse
import logging

# list all the non-dream gamemodes, to exclude them from count.
# This allows to prepare for dream modes that may be added in the future
REGULAR_GAME_MODES = ["BEDWARS_TWO_FOUR", "BEDWARS_EIGHT_ONE", "BEDWARS_EIGHT_TWO"
    , "BEDWARS_FOUR_FOUR", "BEDWARS_EIGHT_TWO_TOURNEY", "BEDWARS_FOUR_THREE"]
# other global stuff
API_ENDPOINT_URLS = {
    "api_key": "https://api.hypixel.net/key",
    "games": "https://api.hypixel.net/resources/games",
    "playercount": "https://api.hypixel.net/counts"
}

logging.basicConfig()
log = logging.getLogger("bedwar_fetch")


# basic setup functions
def parse_all_args():
    parser = argparse.ArgumentParser(description="Fetch current Hypixel Bedwars dream Gamemode",
                                     epilog="Overengineered? - no...")
    parser.add_argument("configfile", nargs="?", default="config.ini", help="The config file to be used")
    parser.add_argument("--short", "-s", default=False, action="store_true", help="Do not wait for a button to be pressed after running")
    parser.add_argument("--key", "-k", required=False, help="manually provided API-Key")
    parser.add_argument("--history", default="history.txt", help="The history file to be used(TBI)")
    parser.add_argument("--all", "-a", default=False, action="store_true",
                        help="Display All Dream Game Modes along with player Count")
    parser.add_argument("--verbose", "-v", default=False, action="store_true",
                        help="Enable additional potentially helpfull output")
    parser.add_argument("--prettify", "-p", default=False, action="store_true", help="Output Gamemode in a fancy ASCII-Font (requires pyfiglet to be installed)")
    return parser.parse_args()


def setup_logger(args):
    log.setLevel(logging.INFO if args.verbose else logging.WARNING)


# setting up and reading config file
def create_blank_config_file(filename):
    config = configparser.ConfigParser()
    config["ACCESS"] = {
        "hypixel_api_token": "your_key"
    }
    config["API_CONFIG"] = API_ENDPOINT_URLS
    log.info("Attempting to Create Config file...")
    with open(filename, "w") as f:
        config.write(f)
    log.info("Success!")


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
    log.info("Attempting to retrieve key from config file " + filename + "...")
    config = configparser.ConfigParser()
    config.read(filename)
    log.info("Success")
    log.info("Read API-key: " + config["ACCESS"]["hypixel_api_token"])
    return config["ACCESS"]["hypixel_api_token"]


def read_and_replace_url_dict(filename):
    log.info("Attempting to read API-URLs from file " + filename + "...")
    config = configparser.ConfigParser()
    config.read(filename)
    log.info("Success!")
    global API_ENDPOINT_URLS
    if API_ENDPOINT_URLS != config["API_CONFIG"]:
        log.info("Overwriting internal URL-Configuration...")
        API_ENDPOINT_URLS = config["API_CONFIG"]


# checking for correctness of elements
def check_api_key_working(api_key):
    headers = {
        "API-Key": api_key
    }
    log.info("Checking if API-key " + api_key + "is valid...")
    response = requests.get(API_ENDPOINT_URLS["api_key"], headers=headers)
    if response.json()["success"]:
        log.info("API-key valid!")
        return True
    else:
        log.info("API-key invalid!")
        return False


def check_validness_of_request(response, url):
    if response.json()["success"]:
        log.info("Url: " + url + "is valid!")
    else:
        log.error("Url: " + url + "did not return a valid result!")
        if __name__ == "__main__":
            exit(3)

# api accessing functions
def get_hypixel_playercount(api_key):
    headers = {
        "API-Key": api_key
    }
    log.info("Attempting to retrieve playercounts...")
    response = requests.get(API_ENDPOINT_URLS["playercount"], headers=headers)
    check_validness_of_request(response, API_ENDPOINT_URLS["playercount"])
    log.info("Success!")
    return response


def get_hypxiel_game_modes(api_key):
    headers = {
        "API-Key": api_key
    }
    log.info("Attempting to retrieve names of all game modes...")
    response = requests.get(API_ENDPOINT_URLS["games"], headers=headers)
    check_validness_of_request(response, API_ENDPOINT_URLS["games"])
    log.info("Success!")
    return response.json()["games"]["BEDWARS"]["modeNames"]


def get_all_dream_mode_names(api_key):
    results = []
    game_modes = get_hypxiel_game_modes(api_key)
    log.info("Extracting names of Dream game modes...")
    for i in game_modes.keys():
        if i not in REGULAR_GAME_MODES:
            results.append(i)
    log.info("Done!")
    return results


def get_dream_modes_count(count_json, api_key):
    bedwars_modes = count_json["games"]["BEDWARS"]
    dream_mode_names = get_all_dream_mode_names(api_key)
    log.info("Extracting playercounts for dream game-modes...")
    played_dream_modes = {}
    for i in bedwars_modes["modes"].items():
        if i[0] in dream_mode_names:
            played_dream_modes[i[0]] = i[1]
    log.info("Done!")
    return played_dream_modes


# data processing
def extract_highest_dream_game_mode(count_json, api_key):
    dream = get_dream_modes_count(count_json, api_key)
    log.info("Determining dream mode with highest playercount....")
    maxmode = (max(dream, key=lambda k: dream[k]))
    log.info("Formatting game mode name...")
    maxmode = re.sub("(BEDWARS_FOUR_FOUR_|BEDWARS_EIGHT_TWO_|BEDWARS_)", "", maxmode).lower()
    log.info("Determined gamemode: " + maxmode)
    return maxmode


def convert_to_ascii_text_art(text):
    try:
        log.info("Attempting to import pyfiglet...")
        from pyfiglet import Figlet, FigletFont
        import random
        log.info("Success!")
        f = Figlet(font=random.choice(FigletFont.getFonts()))
        return f.renderText(text)
    except ImportError as error:
        log.error("Using the pretty option requires pyfiglet to be installed")
        return text


def get_current_gammeode_name(api_key):
    json = get_hypixel_playercount(api_key).json()
    return extract_highest_dream_game_mode(json, api_key)
# main routine functions

def try_read_create_config_file(config_file_name):
    try:
        log.info("Attempting to read config file " + config_file_name + "...")
        with open(config_file_name) as f:
            log.info("Success!")
            return get_api_key_from_file(config_file_name)
    except IOError:
        log.info("Failed to read and/or find config file!")
        if not re.match("(.*).ini", config_file_name):
            config_file_name = config_file_name + ".ini"
        create_config_file_dialog(config_file_name)


def main():
    args = parse_all_args()
    setup_logger(args)
    api_key = ""
    if not args.key:
        config_file_name = args.configfile
        api_key = try_read_create_config_file(config_file_name)
        read_and_replace_url_dict(config_file_name)
    elif args.key:
        api_key = args.key

    if not check_api_key_working(api_key):
        log.error("Invalid API-Key")
        exit(2)
    json = get_hypixel_playercount(api_key).json()
    if args.all:
        for i in get_dream_modes_count(json, api_key).items():
            print(i[0] + ": " + str(i[1]))
    elif args.prettify:
        print(convert_to_ascii_text_art(extract_highest_dream_game_mode(json, api_key)))
    else:
        print(extract_highest_dream_game_mode(json, api_key))
    if not args.short:
        input("press any key to exit")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import requests
import jsonpickle
import os
from global_variables import *
import textwrap


restHost = os.getenv("REST_HOST") or REST_HOST
restPort = os.getenv("REST_PORT") or REST_PORT
rest_addr = f"{restHost}:{restPort}"
rest_methods = {
    "GET" : requests.get,
    "POST" : requests.post
}

def sendRequest(req):
    reqmethod = rest_methods[req["req_type"]]
    endpoint = req["endpoint"]
    jsonData = jsonpickle.encode(req["json"])
    if DEBUG_MODE:
        print("=" * 30)
        print(f"sending request to http://{rest_addr}/{endpoint}")
    response = reqmethod(f"http://{rest_addr}/{endpoint}", 
                         data=jsonData,
                         headers={'Content-type': 'application/json'})
    if response.status_code == 200:
        jsonResponse = response.json()
        if DEBUG_MODE:
            # print(jsonResponse)
            print(jsonpickle.dumps(response.json(), indent=4))
            print("=" * 30)
        return jsonResponse
    else:
        if DEBUG_MODE:
            print(f"response code is {response.status_code}, raw response is: \n {response.text}")
            print("=" * 30)
        return response.text


def get_ui_sep_main_str(ch="=", size=UI_MAIN_WIDTH):
    return ch * (size // len(ch))

def get_ui_sep_sub_str(ch="- ", size=UI_MAIN_WIDTH):
    return ch * (size // len(ch))

def get_ui_decoration_str(s, style):
    ansi_end = "\033[0;0m"
    if style == "bold":
        ansi_begin = "\033[1m"
    elif style == "underline":
        ansi_begin = "\033[4m"
    elif style == "purple":
        ansi_begin = "\033[35m"
    elif style == "cyan":
        ansi_begin = "\033[36m"
    elif style == "blue":
        ansi_begin = "\033[34m"
    elif style == "green":
        ansi_begin = "\033[32m"
    elif style == "yellow":
        ansi_begin = "\033[33m"
    elif style == "red":
        ansi_begin = "\033[31m"
    else:
        # return without any decoration
        return s

    return ansi_begin + s + ansi_end


def get_ui_center_aling_str(s, size):
    if len(s) < size:
        spaces = " " * ((size - len(s)) // 2)
        s = spaces + s
    return s


def get_ui_title_str(title, ch="=", size=UI_MAIN_WIDTH):
    s = ch * size
    s += "\n" + get_ui_center_aling_str(title, size) + "\n"
    s += ch * size
    return s


def get_ui_formatted_game_state(interactions):
    game_state = "\n"
    for interaction in interactions:
        for k, v in interaction.items():
            st = k
            if UI_USE_COLOR:
                st = get_ui_decoration_str(st, UI_DM_KEY_COLOR) if k == GAME_DM_KEY else get_ui_decoration_str(st, UI_PLAYER_KEY_COLOR)
                st = get_ui_decoration_str(st, "underline")
                
            st += ": " + v
            st = textwrap.wrap(st, width=UI_MAIN_WIDTH)
            for line in st:
                game_state += line + '\n'
            game_state += '\n' 
    
    return game_state
    


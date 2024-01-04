#!/usr/bin/env python3

import os
import sys
import time
from global_variables import *
from utils import *


class Client():
    def __init__(self) -> None:
        self.user = None
        self.session_id = None

    def create_account(self):
        user_name = input("Enter user_name: ")
        password = input("Enter password: ")
        json_data = {
            "user_name": user_name,
            "password": password,
        }

        req = REST_END_POINTS["create_account"]
        req["json"] = json_data
        response = sendRequest(req)

        success = True 
        ui_message = "New Account Created!"
        
        response = {"success": success, "server_response": response}
        return response
    
    def login(self):
        user_name = input("Enter user_name: ")
        password = input("Enter password: ")
        json_data = {
            "user_name": user_name,
            "password": password,
        }

        req = REST_END_POINTS["login"]
        req["json"] = json_data
        response = sendRequest(req)
        
        success = response["success"] # if the request was successful or not
        if success:
            ui_message = "Login Successful" 
            self.user = Player(user_name=json_data["user_name"])
        else:
            ui_message = "Wrong Credentials" 
       
        response = {"success": success, "server_response": response}
        return response

    def start_game(self):
        if self.user is None:
            print("Login required")
        else:
            self.user.player_screen_ui() # start player UI
            self.print_ui_title()

    def print_ui_title(self):
        title = "Polybius"
        cmd_str = (
                "login \t : \t Login to your acount" + '\n' +
                "new \t : \t Create a new account"  + '\n' +
                "start \t : \t Start the game"  + '\n' +
                "exit \t : \t Exit Game"  + '\n' +
                get_ui_sep_main_str()
            )
        
        if UI_REFRESH_SCREEN:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(get_ui_title_str(title))
        print(cmd_str)
        
    def client_screen_ui(self):
        cmd = None
        self.print_ui_title()
        while(cmd != 'exit'):
            cmd = input("> ")
            if(cmd == 'login'):
                print(get_ui_sep_sub_str())
                response = self.login()
                if response["success"]:
                    self.start_game()
            elif(cmd == 'new'):
                print(get_ui_sep_sub_str())
                response = self.create_account()
            elif(cmd == 'start'):
                print(get_ui_sep_sub_str())
                self.start_game()
            elif(cmd == 'exit'):
                break
            else:
                print("Invalid Command")
            
            print(get_ui_sep_sub_str())

        print(get_ui_title_str("Exited Polybius"))
        

class Player():
    def __init__(self, user_name=None) -> None:
        self.user_name = user_name
        self.game = None  
        
    
    def get_user_games(self):
        json_data = {
            "user_name": self.user_name,
        }
        req = REST_END_POINTS["get_user_games"]
        req["json"] = json_data
        response = sendRequest(req)

        prev_games = response["games"]
        if(len(prev_games) == 0):
            print("No Previous Games Found!")
        else:
            print("Previous Games:")
            for game in prev_games:
                print(game)

        success = True
        response = {"success": success, "server_response": response}
        return response
    
    def create_new_game(self):
        user_name = self.user_name
        game_name = input("Enter a name for your new game: ")
        setting = "fantasy"
        ## currently only tested with fantasy setting
        # setting = input("Enter theme for your new game (fantasy/cyberpunk): ")
        json_data = {
            "user_name": user_name,
            "game_name": game_name,
            "setting": setting,
        }

        req = REST_END_POINTS["create_new_game"]
        req["json"] = json_data
        response = sendRequest(req)

        success = True
        response = {"success": success, "server_response": response}
        return response
    

    def play_game(self, game_id=None):
        if game_id is None:
            game_id = input("Enter previous game's id: ")
        self.game = Game(game_id=game_id)
        self.game.game_screen_ui()
        self.print_ui_title()


    def print_ui_title(self):
        title = f"Player: {self.user_name}"
        cmd_str = (
                "list \t : \t List all your games" + '\n' +
                "new \t : \t Create a new game"  + '\n' +
                "resume \t : \t Continue a previous game"  + '\n' +
                "exit \t : \t Exit this menu"  + '\n' +
                get_ui_sep_main_str()
            )
        
        if UI_REFRESH_SCREEN:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(get_ui_title_str(title))
        print(cmd_str)
        

    def player_screen_ui(self):
        cmd = None
        self.print_ui_title()
        while(cmd != 'exit'):
            cmd = input("> ")
            print(get_ui_sep_sub_str())
            if(cmd == 'list'):
                response = self.get_user_games()
            elif(cmd == 'new'):
                response = self.create_new_game()
                if response["success"]:
                    self.play_game(game_id=response["server_response"]["game_id"])
            elif(cmd == 'play'):
                self.play_game()
            elif(cmd == 'exit'):
                break
            else:
                print("Invalid Command")

            print(get_ui_sep_sub_str())



class Game():
    def __init__(self, game_id) -> None:
        self.game_id = game_id
        self.seq_num = 0 # init to 0; should be len(interactions) at all times
        self.game_dict = None
        self.game_name = None
        self.last_action_prompt = None

    def update_seq_num(self):
        self.seq_num = len(self.game_dict["interactions"])

    def take_action(self, prompt):
        ## save prompt for retry later if required
        self.last_action_prompt = prompt

        json_data = {
            "game_id": self.game_id,
            "seq_num": self.seq_num,
            "player_prompt": prompt,
        }

        req = REST_END_POINTS["take_action"]
        req["json"] = json_data
        response = sendRequest(req)

        success = True
        response = {"success": success, "server_response": response}
        return response

    def redo_last(self):
        ## remove an interaction and update seq_num
        self.game_dict["interactions"].pop()
        self.update_seq_num()

        json_data = {
            "game_id": self.game_id,
            "seq_num": self.seq_num,
        }

        req = REST_END_POINTS["redo_last"]
        req["json"] = json_data
        response = sendRequest(req)

        success = True
        response = {"success": success, "server_response": response}
        return response
         

    def get_game_state(self):
        for _ in range(EXTENDED_REST_NUM_RETRIES):
            try:
                time.sleep(RETRY_TIME_DELAY) 
                json_data = {
                    "game_id": self.game_id,
                    "seq_num": self.seq_num,
                }
                req = REST_END_POINTS["get_game_state"]
                req["json"] = json_data
                response = sendRequest(req)

                assert response["interactions"] is not None, 'expected new interaction from server'

                ## update local game state
                if self.game_dict is None:
                    self.game_dict = {
                        "info": response["info"],
                        "interactions": response["interactions"],
                    }
                    self.game_name = response["info"]["game_name"]
                else:
                    # last interaction is overwritten, required for getting action from server
                    self.game_dict["interactions"] = self.game_dict["interactions"][:-1] + response["interactions"]

                ## added an interaction so update seq_num
                self.update_seq_num()
                break
            
            except:
                pass

        success = True
        response = {"success": success, "server_response": response}
        return response
    
    def retry(self):
        ## handles two failure modes
        ## 1. if server fails to add last action in DB or LLM fails to update game state
        ## 2. if we don't get response from server in time in get_game_state()
        if self.last_action_prompt is not None and len(self.last_action_prompt) > 0:
            self.take_action(self.last_action_prompt)

    def print_ui_title(self):
        title = f"Game: {self.game_name}"
        if UI_REFRESH_SCREEN:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(get_ui_title_str(title))

    def print_game_state(self):        
        self.print_ui_title()
        print(get_ui_formatted_game_state(self.game_dict["interactions"]), end='')      

    def game_screen_ui(self):
        prompt = None        
        while(prompt != 'exit'):
            self.get_game_state()
            self.print_game_state()
            prompt = input("> ")
            if(prompt == 'exit'):
                break
            elif(prompt == 'redo'):
                self.redo_last()
            elif(prompt == 'retry'):
                self.retry()
            elif len(prompt) > 0:
                self.take_action(prompt)


if __name__ == '__main__':
    polybius_client = Client()
    polybius_client.client_screen_ui()


"""

------------------------------------------------------------
How to Run:
------------------------------------------------------------


Install MinIO

no need to make build images


./deploy-cloud.sh

kubectl apply -f expose-rest.yaml    # expose service to outside 




create venv

install client requirements








------------------------------------------------------------
Useful Kubectl commands:
------------------------------------------------------------

kubectl exec -it pod/llm-deployment  -- /bin/bash

kubectl get deployments -o wide

kubectl get pods --all-namespaces -o jsonpath="{.items[*].status.containerStatuses[*].imageID}" | tr -s '[[:space:]]' '\n' | sort | uniq -c

gcloud container clusters resize dcsc-project --region us-central1-b --num-nodes=0

kubectl port-forward service/rest-svc 5005:5005

"""




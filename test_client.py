#!/usr/bin/env python3

import requests
import jsonpickle
import os
import sys
import time
from global_variables import *
from utils import *


# endpoint 
request_list = [

    ##------------------------------
    {
        "endpoint" : "/apiv1/test/minio/removeall",
        "req_type" : "GET",
        "json" : {
            "user_name": "",
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/test/minio/createall",
        "req_type" : "GET",
        "json" : {
            "user_name": "",
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/user/new",
        "req_type" : "POST",
        "json" : {
            "user_name": "user10",
            "password": "pass10",
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/user/new",
        "req_type" : "POST",
        "json" : {
            "user_name": "user20",
            "password": "pass20",
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/test/minio/list/users",
        "req_type" : "GET",
        "json" : {
            "user_name": "",
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/game/new",
        "req_type" : "POST",
        "json" : {
            "user_name": "user10",
            "game_name": "game10",
            "setting": "fantasy"
        }
    },


    ###------------------------------
    {
        "endpoint" : "/apiv1/game/new",
        "req_type" : "POST",
        "json" : {
            "user_name": "user20",
            "game_name": "game20",
            "setting": "fantasy"
        }
    },


    ###------------------------------
    {
        "endpoint" : "/apiv1/user/games",
        "req_type" : "GET",
        "json" : {
            "user_name": "user10",
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/user/games",
        "req_type" : "GET",
        "json" : {
            "user_name": "user10",
        }
    },


    ###------------------------------
    {
        "endpoint" : "/apiv1/game/state",
        "req_type" : "GET",
        "json" : {
            "game_id": "game10",
            "seq_num": 0,
        }
    },



    ###------------------------------
    {
        "endpoint" : "/apiv1/game/state",
        "req_type" : "GET",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 0,
        }
    },
    {
        "endpoint" : "/apiv1/game/action",
        "req_type" : "POST",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 0,
            "player_prompt": "action 0"
        }
    },


    ###------------------------------
    {
        "endpoint" : "/apiv1/game/state",
        "req_type" : "GET",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 1,
        }
    },
    {
        "endpoint" : "/apiv1/game/action",
        "req_type" : "POST",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 1,
            "player_prompt": "action 1"
        }
    },

    ###------------------------------
    {
        "endpoint" : "/apiv1/game/state",
        "req_type" : "GET",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 2,
        }
    },
    {
        "endpoint" : "/apiv1/game/action",
        "req_type" : "POST",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 2,
            "player_prompt": "action 2"
        }
    },


    ###------------------------------
    {
        "endpoint" : "/apiv1/game/state",
        "req_type" : "GET",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 3,
        }
    },
    {
        "endpoint" : "/apiv1/game/action",
        "req_type" : "POST",
        "json" : {
            "user_name": "user10",
            "game_id": "game10",
            "seq_num": 3,
            "player_prompt": "action 3"
        }
    },



    # ###------------------------------
    # {
    #     "endpoint" : "/apiv1/test/minio/removeall",
    #     "req_type" : "GET",
    #     "json" : {
    #         "user_name": "",
    #     }
    # },

]


for req in request_list:
    jsonResponse = sendRequest(req)
    time.sleep(RETRY_TIME_DELAY)



sys.exit(0)




"""

kubectl exec -it pod/worker-deployment-7684d4fb9-m898q  -- /bin/bash



JSON objects

request_list = [
    {
        "endpoint" : "/apiv1/test/minio/remove",
        "req_type" : "GET",
        "json" : {
            "user_name": "",
        }
    },

    {
        "endpoint" : "/apiv1/test/minio/put",
        "req_type" : "POST",
        "json" : {
            "game_id": 1,
            "user_name": "user1",
            "game_name": "game1",
        }
    },

    {
        "endpoint" : "/apiv1/test/minio/get",
        "req_type" : "GET",
        "json" : {

        }
    },


    {
        "endpoint" : "/apiv1/game/new",
        "req_type" : "GET",
        "json" : {
            
        }
    },

]


"""



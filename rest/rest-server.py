#!/bin/python3

import os
import logging
from flask import Flask, request, Response
import jsonpickle
import pickle
import io
import redis
from minio import Minio
import hashlib
import time
from datetime import datetime
from global_variables import *

# Initialize the Flask application
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


restHost = os.getenv("REST_HOST") or REST_HOST
restPort = os.getenv("REST_PORT") or REST_PORT

minioHost = os.getenv("MINIO_HOST") or MINIO_HOST
minioPort = os.getenv("MINIO_PORT") or MINIO_PORT
minioUser = os.getenv("MINIO_USER") or MINIO_USER
minioPasswd = os.getenv("MINIO_PASS") or MINIO_PASS

redisHost = os.getenv("REDIS_HOST") or REDIS_HOST
redisPort = os.getenv("REDIS_PORT") or REDIS_PORT


print("+" * 60)
print("running REST server")
print("rest addr:", restHost, restPort)
print("redis addr:", redisHost, redisPort)
print("minio addr:", minioHost, minioPort)
print("+" * 60)


redisClient = redis.StrictRedis(host=redisHost, port=redisPort, decode_responses=True)

redisClient.flushdb() ############### REMOVE IN FINAL ############### !!!!!


minioClient = Minio(f"{minioHost}:{minioPort}",
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)


for bucket in MINIO_BUCKET_LIST:
    if not minioClient.bucket_exists(bucket):
        minioClient.make_bucket(bucket)



######################## util functions ########################

def get_hash(data):
    data_hash = hashlib.md5(data.encode('utf-8')).hexdigest()
    return data_hash

def check_login_creds(user_name, password):
    try:
        user_dict = minio_get_json(MINIO_USERS_BUCKET, user_name)
        return user_dict["password"] == password
    except:
        return False
    
def create_session(user_name):
    # TO DO
    return 42

def check_session(session_id):
    # TO DO
    # use session id to return user_id else None
    # use timestamp to delete old sessions
    return True


def minio_put_json(bucket, id, json_dict):
    data = pickle.dumps(json_dict)    
    ioBuffer = io.BytesIO(data)
    data_size = len(data)
    minioClient.put_object(bucket, id, ioBuffer, data_size)
    return

def minio_get_json(bucket, id):
    response = minioClient.get_object(bucket, id)
    json_dict = pickle.loads(response.data)
    return json_dict


def minio_remove_non_empty_bucket(bucket):
    if minioClient.bucket_exists(bucket):
        objs = [str(obj._object_name) for obj in minioClient.list_objects(bucket)]
        for o in objs:
            minioClient.remove_object(bucket, o)
        minioClient.remove_bucket(bucket)


def _create_new_game(req):
    user_name = req['user_name']
    game_name = req['game_name']
    setting = req['setting']
    start_time = datetime.now().replace(microsecond=0)
    start_time_str = start_time.strftime("%y-%m-%d-%H-%M-%S")
    
    # game_id = get_hash(user_name + game_name + start_time_str)

    game_id = game_name

    game = {
        "info":{
            "user_name": user_name,
            "game_name": game_name,
            "game_id": game_id,
            "setting": setting,
            "completed": False,
            "num_interactions": 0,
        },
        "interactions": [],
        # "interactions": [0, 1, 2, 3, 4, 5, 6],
    }

    return game_id, game


def _create_new_user(req):
    user = {
        "user_name": req['user_name'],
        "password": req['password'],
        "games": [],
    }
    return user

 


######################## User Endpoints ########################

@app.route(REST_END_POINTS["create_account"]["endpoint"], methods=[REST_END_POINTS["create_account"]["req_type"]])
def create_account():
    req = request.json
    user = _create_new_user(req)

    # add in DB
    minio_put_json(MINIO_USERS_BUCKET, user["user_name"], user)

    response = {
        'message' : "account created",
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route(REST_END_POINTS["login"]["endpoint"], methods=[REST_END_POINTS["login"]["req_type"]])
def login():
    req = request.json
    user_name = req['user_name']
    password = req['password']

    success = check_login_creds(user_name, password)

    # TO DO
    # sess_id = None
    # if (success):
    #     sess_id = create_session(user_name)
    
    # response = {
    #     'session_id' : sess_id,
    #     }

    if success:
        response = {
            "message": "login successful",
            "success": True,
            }
    else:
        response = {
            "message": "login unsuccessful",
            "success": False,
            }

    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# route http posts to this method
@app.route(REST_END_POINTS["get_user_games"]["endpoint"], methods=[REST_END_POINTS["get_user_games"]["req_type"]])
def get_user_games():
    req = request.json
    user_name = req['user_name']
    user_dict = minio_get_json(MINIO_USERS_BUCKET, user_name)
    prev_games = []
    for game_id in user_dict["games"]:
        game_dict = minio_get_json(MINIO_GAMES_BUCKET, game_id)
        prev_games.append({
            "game_id": game_id,
            "game_name": game_dict["info"]["game_name"],
            "setting": game_dict["info"]["setting"],
            "num_interactions": game_dict["info"]["num_interactions"],
            "completed": game_dict["info"]["completed"],
        })

    response = {
        "games": prev_games,
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")




######################## Game Endpoints ########################


# route http posts to this method
@app.route(REST_END_POINTS["create_new_game"]["endpoint"], methods=[REST_END_POINTS["create_new_game"]["req_type"]])
def create_new_game():
    req = request.json
    user_name = req["user_name"]
    game_id, game_dict = _create_new_game(req)

    # add new game in DB
    minio_put_json(MINIO_GAMES_BUCKET, game_id, game_dict)
    user_dict = minio_get_json(MINIO_USERS_BUCKET, user_name)
    user_dict["games"].append(game_id)
    minio_put_json(MINIO_USERS_BUCKET, user_name, user_dict)

    ## queue for processing by LLM handler
    redisClient.rpush(REDIS_LLM_QUEUE, game_id)

    response = {
        "message": "new game created!",
        "game_id": game_id,
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# route http posts to this method
@app.route(REST_END_POINTS["take_action"]["endpoint"], methods=[REST_END_POINTS["take_action"]["req_type"]])
def take_action():
    req = request.json
    game_id = req["game_id"]
    seq_num = req["seq_num"]
    player_prompt = req["player_prompt"]

    ## add that in DB
    game_dict = minio_get_json(MINIO_GAMES_BUCKET, game_id)

    ## check if seq num from client is same as in DB and 
    ## also check if the player prompt for that seq num is empty.
    if len(game_dict["interactions"]) == seq_num and GAME_PLAYER_KEY not in game_dict["interactions"][-1]:
        game_dict["interactions"][-1][GAME_PLAYER_KEY] = player_prompt
        minio_put_json(MINIO_GAMES_BUCKET, game_id, game_dict)
    
    else:
        print("WARNING: last action not added to DB")
        print("prompt: ", player_prompt)
        print("client seq_num: ", seq_num)
        print("DB seq_num", len(game_dict["interactions"]))
        print("action in DB", GAME_PLAYER_KEY not in game_dict["interactions"][-1])

    ## queue for processing by LLM handler
    redisClient.rpush(REDIS_LLM_QUEUE, game_id)

    response = {
        "message": "action queued",
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")



# route http posts to this method
@app.route(REST_END_POINTS["redo_last"]["endpoint"], methods=[REST_END_POINTS["redo_last"]["req_type"]])
def redo_last():
    req = request.json
    game_id = req["game_id"]
    seq_num = req["seq_num"]

    ## add that in DB
    game_dict = minio_get_json(MINIO_GAMES_BUCKET, game_id)

    ## check if seq num from client is one more than that in DB and 
    if len(game_dict["interactions"]) == seq_num + 1:
        game_dict["interactions"].pop()
        minio_put_json(MINIO_GAMES_BUCKET, game_id, game_dict)
    else:
        print("WARNING: last action not added to DB")


    ## queue for processing by LLM handler
    redisClient.rpush(REDIS_LLM_QUEUE, game_id)

    response = {
        "message": "action queued",
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")



# route http posts to this method
@app.route(REST_END_POINTS["get_game_state"]["endpoint"], methods=[REST_END_POINTS["get_game_state"]["req_type"]])
def get_game_state():
    req = request.json
    game_id = req["game_id"]
    seq_num = req["seq_num"]
    
    game_dict = minio_get_json(MINIO_GAMES_BUCKET, game_id)
    info = game_dict["info"] if seq_num == 0 else None
    
    ## if seq_num of client is greater or equal to DB seq_num then 
    ## need return None, client needs to wait until LLM handler completes request and add another interaction        
    if seq_num >= len(game_dict["interactions"]):
        interactions_begin_seq_num = None
        interactions = None
    else:
        interactions_begin_seq_num = seq_num - 1 if seq_num > 0 else 0
        interactions = game_dict["interactions"][interactions_begin_seq_num:]

    print("seq_num", seq_num)
    print("len of game dict interactions", len(game_dict["interactions"]))


    print("game_dict['interactions']", game_dict["interactions"])

    print("interactions", interactions)

    response = {
        "info": info,
        "interactions_begin_seq_num": interactions_begin_seq_num,
        "interactions": interactions,
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")




######################## Testing Endpoints ########################


@app.route(REST_END_POINTS["test_minio_put"]["endpoint"], methods=[REST_END_POINTS["test_minio_put"]["req_type"]])
def test_minio_put(): 
    req = request.json
    bucket = req["bucket"]
    id = req["id"]
    json_dict = req["json"]
    minio_put_json(bucket, id, json_dict)

    response = {
        'miniolist' : [],
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route(REST_END_POINTS["test_minio_get"]["endpoint"], methods=[REST_END_POINTS["test_minio_get"]["req_type"]])
def test_minio_get(): 
    response = {
        'miniolist' : [],
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route(REST_END_POINTS["test_minio_list"]["endpoint"], methods=[REST_END_POINTS["test_minio_list"]["req_type"]])
def test_minio_list(bucketname): 
    response = {
        'miniolist' : [obj._object_name for obj in minioClient.list_objects(bucketname)],
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route(REST_END_POINTS["test_minio_remove_all"]["endpoint"], methods=[REST_END_POINTS["test_minio_remove_all"]["req_type"]])
def test_minio_remove_all(): 
    for bucket in MINIO_BUCKET_LIST:
        minio_remove_non_empty_bucket(bucket)
    response = {
        'removed_buckets' : MINIO_BUCKET_LIST,
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route(REST_END_POINTS["test_minio_create_all"]["endpoint"], methods=[REST_END_POINTS["test_minio_create_all"]["req_type"]])
def test_minio_create_all(): 
    for bucket in MINIO_BUCKET_LIST:
        if not minioClient.bucket_exists(bucket):
            minioClient.make_bucket(bucket)
    response = {
        'created_buckets' : MINIO_BUCKET_LIST,
        }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")




######################## start flask app ########################

app.run(host=restHost, port=restPort)





#!/bin/python3

import os
import argparse
import random
import string
import io
import redis
from minio import Minio
import pickle
from global_variables import *
from llm_api_helper_vertex_ai import generate_text


minioHost = os.getenv("MINIO_HOST") or MINIO_HOST
minioPort = os.getenv("MINIO_PORT") or MINIO_PORT
minioUser = os.getenv("MINIO_USER") or MINIO_USER
minioPasswd = os.getenv("MINIO_PASS") or MINIO_PASS

redisHost = os.getenv("REDIS_HOST") or REDIS_HOST
redisPort = os.getenv("REDIS_PORT") or REDIS_PORT


print("+" * 60)
print("running LLM Handler")
print("redis addr:", redisHost, redisPort)
print("minio addr:", minioHost, minioPort)
print("+" * 60)


redisClient = redis.StrictRedis(host=redisHost, port=redisPort, decode_responses=True)

minioClient = Minio(f"{minioHost}:{minioPort}",
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

for bucket in MINIO_BUCKET_LIST:
    if not minioClient.bucket_exists(bucket):
        minioClient.make_bucket(bucket)


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


def gen_llm_task_context():
    # create llm context with some randomness 
    random_string = ""
    for s in random.sample(LLM_EXAMPLE_STORIES, 4):
        random_string += '\n' + GAME_DM_KEY + ": " + s
    random_string += '\n'
    for _ in range(random.randint(20, 30)):
        random_string +=  " " + ''.join(random.choices(string.ascii_letters, k=10))

    return LLM_TASK_CONTEXT + random_string + '\n' + LLM_GAME_DIRECTION


def generate_interaction_context(interactions):
    context = ""
    for interaction in interactions:
        for k, v in interaction.items():
            context += k + ': '
            context += v + '\n\n' 
    
    # random_string = ""
    # for _ in range(random.randint(5, 10)):
    #     random_string +=  " " + ''.join(random.choices(string.ascii_letters, k=10))
    # random_string += '\n\n'

    return context 


def new_game():
    prompt = gen_llm_task_context() + LLM_NEW_GAME_CONTEXT + '\n' + GAME_DM_KEY + ": "
    return generate_text(prompt)
    # return "state 0 new game"

def take_action(interactions):
    prompt = gen_llm_task_context() + LLM_CONTINUE_GAME_CONTEXT + '\n' + generate_interaction_context(interactions) + GAME_DM_KEY + ": "
    game_completed = False
    if len(prompt) > TEXT_GEN_MODEL_MAX_CHARACTERS:
        game_completed = True
        response = "Game ended due to max word limit!"
    else:
        response = generate_text(prompt)
        # response = "state " + str(len(interactions))

    return response, game_completed


while True:
    _, game_id = redisClient.blpop(REDIS_LLM_QUEUE, timeout=0)

    print("=" * 60)
    print("> processing game_id:", game_id)

    game_dict = minio_get_json(MINIO_GAMES_BUCKET, game_id)

    ## new game
    if len(game_dict["interactions"]) == 0:
        response = new_game()
        game_dict["interactions"].append({GAME_DM_KEY: response})
        game_dict["info"]["num_interactions"] += 1
        minio_put_json(MINIO_GAMES_BUCKET, game_id, game_dict)
    
    ## else continuing game but ensure player prompt exists
    elif GAME_PLAYER_KEY in game_dict["interactions"][-1]:
        response, game_completed = take_action(game_dict["interactions"])
        game_dict["interactions"].append({GAME_DM_KEY: response})
        game_dict["info"]["num_interactions"] += 1
        game_dict["info"]["completed"] = game_completed
        minio_put_json(MINIO_GAMES_BUCKET, game_id, game_dict)
        
    else:
        print("> ERROR: received request to generate without user prompt for game_id: ", game_id)
    

    print("=" * 60)


import tweepy
import json
from itertools import islice
import os
import time
import pprint
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools 
import time

data_folder = "data_ids"
pp=pprint.PrettyPrinter()

def serialize_json(folder, filename, data):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/{filename}", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()
    print(f"Data serialized to path: {folder}/{filename}")

def read_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as file:
            data = json.load(file)
        print(f"Data read from path: {path}")
        return data
    else:
        print(f"No data found at path: {path}")
        return {}

api_key="27DtXSRNidanfmJBeRgzAmFol"
api_secret="d65ShkMPCO8xZTYvMhxlmExPOjLCRWm6Msu02h8hYSCjCU4Yxh"

access_token="540729727-ZVuTnExVb1Lr7g8BIn4Een3cncwXmGPjhhaxH6mN"
access_secret="es2fwyNji3GIDhrbUirB3su5CwU8En1KndkkSg5XmjPrh"

bearer_token="AAAAAAAAAAAAAAAAAAAAAFITJQEAAAAABnzKRPdGpHXZG1ENi5MRbvkUWeQ%3Dqz9RXuyv2I7jqqfsne4GPDwWqzDNBXIF37G1r3Egs7RPM46Y1I"




followers_ids=read_json("data_ids/followers_5_utenti.json")
following_ids=read_json("data_ids/following_5_utenti.json")
followers_of_followers_ids=read_json("data_ids/followers_of_followers.json")
following_of_following_ids=read_json("data_ids/following_of_following.json")
lista_json=[followers_ids,following_ids,followers_of_followers_ids,following_of_following_ids]
s,stot=0,0
for jsonn in lista_json:
    for user in jsonn:
        s+=len(jsonn[user])
        print(len(jsonn[user]))
    print(" tot json: {}".format(s))
    stot+=s
    s=0
print("totale pre pulizia:{}".format(stot))

fin=[]

duplicati=0
for jsonn in lista_json:
    for user in jsonn:
        for el in jsonn[user]:

            if el in fin:
                duplicati+=1
            else:
                fin.append(el)
print("ci sono {} utenti unici, con {} duplicati rimossi da {}".format(len(fin),duplicati,stot))

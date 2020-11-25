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

auth=tweepy.OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,access_secret)
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if(api.verify_credentials):
    print("Auth success")


users=["mizzaro","damiano10","miccighel_","eglu81","KevinRoitero"]
users_id=[18932422, 15750573, 15750573, 19659370, 3036907250]


followers_ids=read_json("data_ids/followers_5_utenti.json")
following_ids=read_json("data_ids/following_5_utenti.json")
followers_of_followers_ids=read_json("data_ids/followers_of_followers.json")
following_of_following_ids=read_json("data_ids/following_of_following.json")
print("Json caricati")

#unione in unico json finale senza ripetizioni, tanto abbiamo già estratto i follower random ed è più comodo per la chiamata api.show_friendship
#Logicamente, se non fosse stato per la consegna, avremmo avuto già le relazioni scaricando i followers dei 5 nodi principali

lista_json=[followers_ids,following_ids,followers_of_followers_ids,following_of_following_ids]
id_nodi_revisionati=[]
#print(lista_json)
for json_2 in lista_json:
    for utente in json_2:
        for user_id in json_2[utente]:
            if not user_id in id_nodi_revisionati:
                id_nodi_revisionati.append(user_id['id'])

#print(id_nodi_revisionati)

i=0
tot=len(id_nodi_revisionati)

nodes=read_json("data_ids/nodes_of_twitter_graph.json")
friendships=[]
def returnTime(tempo):
    h,m=divmod(tempo,3600)
    m=m//60
    return "ETA H:{} M:{}".format(h,m)
ETA=15500
startTime=time.time()

for node_id in id_nodi_revisionati:
    print(returnTime(int(ETA-(time.time()-startTime))))
    print(round(i*100/tot,3),"%")
    time.sleep(1)
    try:
        relationship = api.show_friendship(source_id=node_id,target_id=15750573)
        relation = relationship[0]
        infos_of_relation={}
        #Controllo nell'oggetto relationship delle relazioni di follow e following
        if(relation.following == True): # node follows the user
            infos_of_relation["source"] = node_id
            infos_of_relation["type"] = "following"
            infos_of_relation["target"] = 15750573
            friendships.append(infos_of_relation)
        if(relation.followed_by == True): # user follows the node
            infos_of_relation["source"] = 15750573
            infos_of_relation["type"] = "follows"
            infos_of_relation["target"] = node_id
            friendships.append(infos_of_relation)
    except:
        print(node_id)
    i+=1
serialize_json("data_ids", "miccighel_edges_of_twitter_graph.json", friendships)
print("Completamento controllo relazioni terminato")
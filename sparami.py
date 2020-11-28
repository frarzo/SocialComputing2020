import tweepy
import json
from itertools import islice
import os
import time
import pprint
import requests
import random
import networkx as nx
from networkx.algorithms.approximation import clique
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pyvis.network import Network
import itertools 
from scipy import stats

print("Librerie caricate!")
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
        #Fase di autenticazione
api_key="cvoM8D7hXXxlvBXTM8aH9X2ec"
api_secret="Uk2UvH0FJY7KaDzkXYLfgiYkA1OuCwbLlGFPyodB5wcQ5bsItN"
access_token="3303466053-OLuExo5KcP8UQCVwZwmyakZs8b91Fpl2lMOUDAe"
access_secret="1lMXufu42KN8JvJjYT7c0zI3Q57CkN09BxkNXZuNQ0Dej"
bearer_token="AAAAAAAAAAAAAAAAAAAAAHsVJQEAAAAAQ4vYb83r6ueD8QvjJ4Zpx9R7Kbw%3DQuLzsmDYOvpff7lRHGXhNJSOXTFuPyOwLHZv7HPSj9WF34h1E8"

auth=tweepy.OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,access_secret)
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if(api.verify_credentials):
    print("Auth success")
users_screen_name=["mizzaro","damiano10","miccighel_","eglu81","KevinRoitero"]
users_id=[18932422, 132646210, 15750573, 19659370, 3036907250]
#Unione di tutti gli id rilevati e rimozione dei duplicati

#Caricamento json contenente tutti gli ID dei nodi interessati
followers_ids=read_json("data_ids/followers_5_utenti.json")
following_ids=read_json("data_ids/following_5_utenti.json")
followers_of_followers_ids=read_json("data_ids/followers_of_followers.json")
following_of_following_ids=read_json("data_ids/following_of_following.json")

print("Json caricati")

lista_json=[followers_ids,following_ids, followers_of_followers_ids,following_of_following_ids]

id_nodi_grafo=[]
#Eliminazione duplicati e conteggio di essi.
for jsonn in lista_json:
    for user in jsonn:
        for user_id in jsonn[user]:
            if not user_id in id_nodi_grafo:
                id_nodi_grafo.append(user_id)

print(len(id_nodi_grafo))
# Unione delle relazioni scaricate per ogni utente, necessario per parallelizzare il download
damiano_edges=read_json("data_ids/api_show_friendship/damiano_edges.json")
eglu_edges=read_json("data_ids/api_show_friendship/eglu_edges.json")
kevin_edges=read_json("data_ids/api_show_friendship/kevin_edges.json")
micch_edges=read_json("data_ids/api_show_friendship/micch_edges.json")
mizzaro_edges=read_json("data_ids/api_show_friendship/mizzaro_edges.json")

lista_edges=[damiano_edges,eglu_edges, kevin_edges,micch_edges,mizzaro_edges]

main_edges = []
#Unione json
for main in lista_edges:
    for relation in main:
        main_edges.append(relation)
serialize_json("data_ids", "edges_of_twitter_graph.json", main_edges)
#5.2 Creazione del grafo


twitter_graph = nx.DiGraph(team="Loris Parata 144338, Francesco Arzon 142439, Lorenzo Dal Fabbro, Matteo Galvan")
#Aggiunta dei nodi al grafo
nodes_of_graph=read_json("data_ids/nodes_of_twitter_graph.json")
for ids, node in nodes_of_graph.items():
    if ids in ["18932422", "132646210", "15750573", "19659370", "3036907250"]:
        color="magenta"
    else:
        color='cyan'

    twitter_graph.add_node(ids,
                        id= ids,
                        title= node["name"],
                        color =color,
                        width=width,
                        physics=False,
                        name=node['name'],
                        screen_name=node['screen_name'],
                        location=node['location'],
                        followers_count=node["followers_count"],
                        following_count=node["friends_count"],
                        number_of_twitts=node["statuses_count"],
                        data_creazione_profilo=node["created_at"]
                        ) 
#Aggiunta degli archi al grafo, con controllo se è presente nel grafo il nodo source, per rilevare eventuali incongurenze
for edge in main_edges:
    if edge['type'] == 'following': #non follows, a causa dell'inversione source - targhet nella funzione di show_frienship
        if twitter_graph.has_node(str(edge['source'])):
            twitter_graph.add_edge(str(edge['source']),str(edge['target']))
        else:
            print("Relazione relativa ad un nodo non presente nel grafo")
            
print(twitter_graph.number_of_nodes())
print(twitter_graph.number_of_edges())
#6 Creazione grafo interattivo con pyvis

def disegna_grafo(grafo):
    nt = Network(
        height ="80%",
        width = "80%",
        bgcolor="#222222",
        font_color="white",
        heading= grafo,
        directed=True,
    )
    nt.options(set_tree_spacing)
    nt.set_trees
    nt.show_buttons(filter_=None)
    nt.from_nx(grafo)
    # nt.barnes_hut()
    nt.inherit_edge_colors(False)
    # nt.set_edge_smooth("continuous") #cambia formato di visualizzazione degli archi
    neighbor_map = nt.get_adj_list()
    
    for node in nt.nodes:
            node["value"] = len(neighbor_map[node["id"]])
    nt.show("grafo.html")

disegna_grafo(twitter_graph)
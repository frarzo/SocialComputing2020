# SocialComputing2020
def follower_graph(df_followers):
    #creazione grafo dei follower ed aggiunta dei nodi
    follower_graph = nx.DiGraph()
    for index,row in df_followers.iterrows():
            follower_graph.add_node(row["id"],
                           id= row["id"],
                           title=[row['name']+" \n |Screen Name:"+ row['screen_name']+" \n |Location: "+ row['location']],
                           color ="#2e00ff"
                           )            
    #aggiunta degli archi al grafo dei follower
    for index,row in df_followers.iterrows():
        follower_graph.add_edge(row["id"],row['target'])
        
    return follower_graph
	
	
	
followers_count=row['followers_count'],
friends_count=row['friends_count'],
statuses_count = row['statues_count']
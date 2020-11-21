 for result in relation[relationship]
        if(result["source"]["followed_by"]== "true" | result["source"]["following"]== "true" ):
            if(result["source"]["followed_by"] == true):
                result["source"] = result["source"]["id"]
                result["followed"] = True
            if(result["source"]["following"] == true):
                result["target"] = result["target"]["id"]
                result["following"] = True
            friendships.append(result)
import json #Import library to convert string to dict
import requests
import sys
import csv
import time

most_pop_300 = []
url = "https://api.themoviedb.org/3/discover/movie"
payload = {"api_key": sys.argv[1], "language": "en-US", "sort_by": "popularity.desc", "page": 1, "primary_release_date.gte": "2000-01-01", "with_genres": "35"}
while len(most_pop_300) < 300: 
    response = requests.get(url, params=payload) #make a get rquest to the api which will give Json string response
    response_dict = json.loads(response.text) #convert response to dict
    most_pop_300 = most_pop_300 + response_dict["results"] #Get only Result list from dict and add to most pop 300 list
    payload["page"] += 1 #Increment page # by one
#print(most_pop_300)

id_title_list = [[movie["id"], movie["title"]] for movie in most_pop_300]
#print(id_title_list)   
    
#Question 1b
with open("movie_ID_name.csv", "w", newline = "") as myfile:
     wr = csv.writer(myfile)
     wr.writerows(id_title_list)
     
#Question 1c
counter = 0
sim_movies_dict = {}
start = time.time()
for movie in id_title_list:
    movie_id = movie[0]
    url2 = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/similar"
    payload2 = {"api_key": sys.argv[1], "language": "en-US", "page": 1}
    response2 = requests.get(url2, params=payload2) #make a get rquest to the api which will give Json string response
    response_dict2 = json.loads(response2.text) #convert response to dict
    sim_movies = response_dict2["results"][:5] if "results" in response_dict2 else [] #first five results list
    sim_movies_id_list = [sim_movie["id"] for sim_movie in sim_movies]
    sim_movies_dict[movie_id] = sim_movies_id_list
    counter += 1
    if counter % 40 == 0:
        time.sleep(10)
end = time.time()    

#print(sim_movies_dict)
#print(end - start)
#print(counter)

list_of_pairs = []
for movie_id in sim_movies_dict:
    for sim_movie_id in sim_movies_dict[movie_id]:
        list_of_pairs.append((movie_id,sim_movie_id))
        
        
unique_pairs = set(tuple(sorted(pair)) for pair in list_of_pairs)
#print(unique_pairs)

#Question 1c
with open("movie_ID_sim_movie_ID.csv", "w", newline = "") as myfile:
     wr = csv.writer(myfile)
     wr.writerows(unique_pairs)
     
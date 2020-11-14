import requests

artist_search_end_point = "https://musicbrainz.org/ws/2/artist?fmt=json&query="; # The data for the artist (The end point)
artist_song_lyric_end_point = "https://api.lyrics.ovh/v1/"
repeat = "y";

while repeat.lower() == "y" :

    artist_name = input("Who do you want to look up?: "); # Search for an artist
    artist_search_uri = artist_search_end_point + artist_name;
    artist_data = requests.get(artist_search_uri).json(); # Get the atists data from the API and extract json
    artist_number = 1;

    for item in artist_data["artists"][:5] : # Get the top 5 results from artist json
        print(artist_number, item["name"]);
        if "disambiguation" in item.keys():
            print(item["disambiguation"]);
                
        print("");
        artist_number += 1;
        
    switch_case = input("Which artist would you like?: ");
    artist = artist_data["artists"][int(switch_case)-1];

    for key in artist.keys() :
        print(artist[key]);

        
    print("");
    repeat = input("Do you want to search again?: ");
    
    








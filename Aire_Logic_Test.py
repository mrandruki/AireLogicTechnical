import requests

def option_choice(option_type):

    return int(input("Which " + option_type + " would you like?: "));

def get_artist_data(artist_name):

    artist_search_uri = artist_search_end_point + artist_name;
    artist_data = requests.get(artist_search_uri).json(); # Get the atists data from the API and extract json
    artist_number = 1;

    for item in artist_data["artists"][:5] : # Get the top 5 results from artist json
        print(artist_number, item["name"]);
        if "disambiguation" in item.keys():
            print(item["disambiguation"]);
                
        print("");
        artist_number += 1;
        
    switch_case = option_choice("artist")
    return artist_data["artists"][switch_case-1];

def get_artist_works():

    artist_works_uri = "https://musicbrainz.org/ws/2/work?artist=" + artist["id"] + "&fmt=json&limit=100"; # Get the works for the artist
    ## print(artist_works_uri);
    artist_works_json = requests.get(artist_works_uri).json(); # Get the artists work from the API and extract json
    return artist_works_json

def get_artist_recordings(artist_song_id):

    artist_recordings_uri = "https://musicbrainz.org/ws/2/recording?work=" + artist_song_id + "&fmt=json&limit=100"; # Get the recording for each work of the artist
    ## print(artist_recordings_uri);
    artist_recordings_json = requests.get(artist_recordings_uri).json(); # Get the artists work from the API and extract json
    return artist_recordings_json

##def lyrics_call(artist_songlist):

    

artist_search_end_point = "https://musicbrainz.org/ws/2/artist?fmt=json&query="; # The data for the artist (The end point)
artist_song_lyric_end_point = "https://api.lyrics.ovh/v1/"
repeat = "y";

while repeat.lower() == "y" :

    artist_name = input("Who do you want to look up?: "); # Search for an artist
    artist = get_artist_data(artist_name) # Get the artists' information

##    for key in artist.keys() :
##        print(artist[key]); 

    # Get works by artist ID then get the top 10 songs by the artist, search if a song is not there
    artist_songlist = get_artist_works();
    artist_recording_data = [];

    print("Getting song data...")
    for item in artist_songlist["works"][:5]:
        print(item["title"]);
        artist_song_id = item["id"];
        artist_recordings = get_artist_recordings(artist_song_id);
        song_recording_data = [];
        sum_length = 0;
        if "recordings" in artist_recordings.keys():
            for artist_recording in artist_recordings["recordings"]:
                if artist_recording["length"] != None:
                    ## print(artist_recording["disambiguation"], artist_recording["length"]);
                    song_recording_data.append(artist_recording); # Artist recording data
                    sum_length += artist_recording["length"];

            artist_recordings["average_song_length"] = sum_length / len(song_recording_data);

    print("Found %d songs and %d recordings." % (len(artist_songlist["works"]), len(artist_recording_data)))

    # Create a data structure from our end, using classes
            
    print("");
    repeat = input("Do you want to search again?: ");
    
    








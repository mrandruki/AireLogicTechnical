import requests
import math
import matplotlib

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

def lyrics_call(artist_name, song_name):

    lyrics_song_uri = "https://api.lyrics.ovh/v1/" + artist_name + "/" + song_name
    artist_lyrics_json = requests.get(lyrics_song_uri).json(); # Get the artists work from the API and extract json
    return artist_lyrics_json
    

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
    artist_sample_size = int(input("How many tracks would you like?: "));
    counter = 0;
    song_index = 0;
    artist_usable_data = [];

    print("Getting song data...")
    while counter < artist_sample_size and counter < len(artist_songlist["works"]):
        item = artist_songlist["works"][song_index]
        artist_song_id = item["id"];
        artist_recordings = get_artist_recordings(artist_song_id);
        song_recording_data = [];
        sum_length = 0;
        item["lyrics"] = lyrics_call(artist_name, item["title"])
        if "recordings" in artist_recordings.keys() and len(item["lyrics"]["lyrics"]) > 0:
##            print(item["title"]);
##            print(item["lyrics"]);
            counter += 1;
            for artist_recording in artist_recordings["recordings"]:
                if artist_recording["length"] != None:
                    ## print(artist_recording["disambiguation"], artist_recording["length"]);
                    song_recording_data.append(artist_recording); # Artist recording data
                    sum_length += artist_recording["length"]/1000;

            item["average_song_length"] = sum_length / len(song_recording_data);
            usable_data = {"title": item["title"], "lyrics": item["lyrics"], "length": sum_length / len(song_recording_data)};
            artist_usable_data.append(usable_data);
            
        song_index += 1;

    sum_lyrics = 0;
    number_of_tracks = len(artist_usable_data);
    
    for item in artist_usable_data:
        new_lyrics = item["lyrics"]["lyrics"].replace("\n", " ");
        new_lyrics = new_lyrics.replace("\r", " ");
        new_lyrics = new_lyrics.replace("  ", " ");
        new_lyrics = new_lyrics.split(" ");
        item["lyric_count"] = len(new_lyrics);
        sum_lyrics += item["lyric_count"];

    average_lyrics = sum_lyrics / number_of_tracks;
    
    total_song_length = 0;
    sum_of_squares = 0;
    
    for item in artist_usable_data:
        total_song_length += item["length"];

    artist_sample_mean = total_song_length / number_of_tracks;

    for item in artist_usable_data:
        sum_of_squares += (item["length"] - artist_sample_mean) ** 2;

    artist_sample_variance = sum_of_squares / number_of_tracks;
    artist_sample_sd = math.sqrt(artist_sample_variance);

    print(" ");
    print("The artist statistics are:");
    print("Mean lyrics within a song = %3.2f" % (average_lyrics));
    print("Mean in seconds = %3.2f" % (artist_sample_mean));
    print("Variance in seconds = %3.2f" % (artist_sample_variance));
    print("Standard deviation in seconds = %3.2f" % (artist_sample_sd));
            
    print("");
    repeat = input("Do you want to search again?: ");
    
    








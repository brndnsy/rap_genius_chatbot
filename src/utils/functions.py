import os
from string import punctuation

import lyricsgenius
from tqdm import tqdm
import pandas as pd

from utils.lyric_preprocessor import LyricPreprocessor


def preprocess(token):
    "preprocess individual tokens by stripping whitespace and removing irrelevant info"
    preprocessed = LyricPreprocessor(token)
    return preprocessed.fully_preprocess().text

def preprocess_lyrics(lyrics):
    "iteratively tokenise sentences within the lyrics so that they can be preprocessed"
    tokens = tokenise(lyrics)
    # df = import_dataset()
    preprocessed_tokens = []
    print("\nCleaning and parsing lyrics...\n")
    for token in tqdm(tokens, desc="Progress", unit="tokens"):
        
        preprocessed_tokens.append(preprocess(token))
    # remove empty strings
    preprocessed_lyrics = list(filter(None, preprocessed_tokens))
    return preprocessed_lyrics


def get_song_lyrics(api, artist=None, song=None, specify=False):
    "query the lyrics of a specific song" 
    if specify:
        artist = str(input("Enter name of artist: "))
        song = str(input("Enter name of song to search for: "))
    # attempt to find lyrics using lyriggenius api
    song_lyrics = api.search_song(song, artist).lyrics
    # preprocess tokens in each song lyric
    preprocessed_lyrics = preprocess_lyrics(lyrics=song_lyrics)
    #  # store preprocessed lyrics in pandas df 
    df = pd.DataFrame(preprocessed_lyrics, columns=['lyric'])
    # call function to generate outputs
    export_lyrics(df, artist=artist, song=song)
    return df
    

def export_lyrics(df, artist, song):
    "export preprocessed lyrics as a csv, and return dataframe for visualisation"
    
    # locate notebook directory
    ipynb_path = os.path.dirname(os.path.realpath("__file__")) 
    #  define output paths
    output_path = f'{ipynb_path}/output'
    lyrics_path = f'{output_path}/lyrics'
    for dir in [output_path, lyrics_path]:
        # create output folders if not already apparent
        if not os.path.exists(dir):
            os.mkdir(dir)

    # label output by artist and song title
    csv_name = '_'.join(artist.split()+song.split())
    # export to csv
    df.to_csv(f'{lyrics_path}/{csv_name}.csv', encoding='utf-8', index=False)
    print(f"""exported "{csv_name}.csv" to output directory""")
    return df


def get_songs(genius, artist_name, max_songs=5):
    "get top 5 songs for artist"
    songs = genius.search_artist(artist_name, max_songs=max_songs, sort="popularity", include_features=False).songs
    # s = [song.lyrics for song in songs]
     # song = artist.song(song_name) - optionally ask to get more songs
    return songs

def tokenise(lyrics):
    "convert lyrical corpus into tokens delinated by lines"
    # ignore first element which contains the song name
    tokens = lyrics.splitlines()[1:]
    # remove 'Embed' tag from last element
    tokens[-1] = tokens[-1].replace('Embed', '')

    find_punc = set([tokens[-1].rfind(i) for i in punctuation if not i.isdigit()])
    if len(find_punc) > 1:
        # print(max(find_punc))
        last_punc_ind = max(find_punc)
        tokens[-1] = tokens[-1][:last_punc_ind+1]

    else:
        # the api's output contained anomalies at the end
        # remove anomalous numbers at end of lyrics
        tokens[-1] = tokens[-1][:len(tokens[-1].rstrip('0123456789'))]
 
    return tokens
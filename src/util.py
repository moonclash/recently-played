import string
from random import shuffle
from base64 import b64encode
from datetime import datetime
import google.generativeai as genai
import os



def generate_activity_name(activity_type, songs):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""
        Come up with a witty Strava activity title based on this
        activity - {activity_type} and these songs - {songs},
        and please just respond with one singular line of text,
        that is the title itself.
    """)
    return response.text

def generate_random_string(len=16):
    alphabet = string.ascii_lowercase
    letters = list(alphabet)[0:len]
    shuffle(letters)
    return letters


def encode_string(*args):
    joined_args = ":".join(args)
    encoded_string = b64encode(joined_args.encode()).decode()
    return encoded_string


def format_songs(spotify_items, before=None, after=None):
    formatted_songs = []
    if before and after:
        spotify_items = [
            item
            for item in spotify_items
            if string_to_date(item.get("played_at")) >= string_to_date(after)
            and string_to_date(item.get("played_at")) <= string_to_date(before)
        ]
    for item in spotify_items:
        track = item.get("track")
        artists = track.get("artists")
        track_name = track.get("name")
        formatted_songs.append(
            f"{','.join([artist.get('name') for artist in artists])} - {track_name}"
        )
    return formatted_songs


def string_to_date(date_string):
    return datetime.strptime(date_string[0:16], "%Y-%m-%dT%H:%M")

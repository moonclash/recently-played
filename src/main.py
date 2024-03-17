import os
import requests
from fastapi import FastAPI, Request
from typing import Optional
from starlette.responses import RedirectResponse
from util import generate_random_string, encode_string, format_songs, string_to_date
from storage import DbManager
from strava import refresh_token as refresh_strava_token
from strava import update_activities_with_songs

app = FastAPI()

ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
LAST_PLAYED_URL = "https://api.spotify.com/v1/me/player/recently-played"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login():
    state = generate_random_string()
    scope = "user-read-recently-played"
    redirect_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={scope}&state={state}&redirect_uri={REDIRECT_URI}"
    return RedirectResponse(redirect_url)


@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    token = encode_string(CLIENT_ID, CLIENT_SECRET)
    response = requests.post(
        url="https://accounts.spotify.com/api/token",
        params={
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "json": True,
        },
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {token}",
        },
    )
    response_data = response.json()
    DbManager.update_token({
        "spotify_access_token": response_data.get("access_token"),
        "spotify_refresh_token": response_data.get("refresh_token")
    })
    return response_data


@app.post("/auto-update")
def auto_update():
    refresh_strava_token()
    refresh_token()
    update_activities_with_songs()


def refresh_token():
    response = requests.post(
        url=ACCESS_TOKEN_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encode_string(CLIENT_ID, CLIENT_SECRET)}",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": DbManager.get_token().get("spotify_refresh_token"),
            "client_id": CLIENT_ID,
        },
    )

    response_data = response.json()
    DbManager.update_token({
        "spotify_access_token": response_data.get("access_token"),
    })


@app.get("/recently-played")
def recently_played(after: Optional[str] = None, before: Optional[str] = None, limit: Optional[int] = None):
    _params = {}
    if after and limit:
        after_obj = string_to_date(after)
        _params["after"] = round(after_obj.timestamp())
        _params["limit"] = limit

    response = requests.get(
        url="https://api.spotify.com/v1/me/player/recently-played",
        headers={
            "Authorization": f"Bearer {DbManager.get_token().get('spotify_access_token')}"
        },
        params=_params,
    )
    music_data = response.json().get("items")
    formatted_songs = format_songs(
        music_data, before=before, after=after
    )

    return {"songs": formatted_songs}

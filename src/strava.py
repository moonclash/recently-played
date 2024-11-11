import os
import requests
from datetime import timedelta
from storage import DbManager
from util import string_to_date, generate_activity_name, refresh_strava_token, refresh_spotify_token

GET_ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
GET_TOKEN_URL = "https://www.strava.com/oauth/token"
UPDATE_ACTIVITY_URL = "https://www.strava.com/api/v3/activities"
GET_ACTIVITY_URL = "https://www.strava.com/api/v3/activities"

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_SECRET")
CODE = os.getenv("CODE")
HOST = "localhost"


def get_token():
    response = requests.post(
        url=GET_TOKEN_URL,
        params={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": CODE,
            "grant_type": "authorization_code",
        },
    )
    response_data = response.json()
    DbManager.update_token(
        {
            "strava_access_token": response_data.get("access_token"),
            "strava_refresh_token": response_data.get("refresh_token"),
        }
    )


def get_single_activity(activity_id):
    response = requests.get(
        url=f"{GET_ACTIVITY_URL}/{activity_id}",
        headers={
            "Authorization": f"Bearer {DbManager.get_token().get('strava_access_token')}"
        },
    )
    response_data = response.json()
    return {
                "activity_id": response_data.get("id"),
                "after": response_data.get("start_date"),
                "type": response_data.get("type"),
                "before": (
                    string_to_date(response_data.get("start_date"))
                    + timedelta(seconds=response_data.get("elapsed_time"))
                ).strftime("%Y-%m-%dT%H:%M"),
            }


def update_activity_description(activity_id, description, name=None):
    data = {"description": description}
    if name:
        data["name"] = name
    response = requests.put(
        url=f"{UPDATE_ACTIVITY_URL}/{activity_id}",
        headers={
            "Authorization": f"Bearer {DbManager.get_token().get('strava_access_token')}"
        },
        data=data,
    )
    return response


def update_activity_with_songs(activity_id):
    refresh_strava_token()
    refresh_spotify_token()
    activity = get_single_activity(activity_id)
    songs_response = requests.get(
        f"http://{HOST}:8000/recently-played",
        params={
            "after": activity.get("after"),
            "before": activity.get("before"),
            "limit": 50,
        },
    )
    songs_response_data = songs_response.json().get("songs")
    activity_name = generate_activity_name(activity.get("type"), songs_response_data)
    update_activity_description(
        activity.get("activity_id"),
        description="🎵 Songs played 🎵: \n" + "\n".join(songs_response_data),
        name=activity_name,
    )

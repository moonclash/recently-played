from main import refresh_token as refresh_spotify_token
from strava import refresh_token as refresh_strava_token
from strava import update_activities_with_songs

def update_strava_activities():
    refresh_strava_token()
    refresh_spotify_token()
    update_activities_with_songs()

if __name__ == "__main__":
    update_strava_activities()
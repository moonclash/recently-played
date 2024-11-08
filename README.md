This project will update your most recent Strava activities' descriptions with the music you've listened to during those activities on Spotify.

How it works:

First, we get the recent activties using Strava's API - the default is set to get all of the activities since "yesterday".

We find out what time the activity has started and then using the duration from the response, we find out the end time. (Strava provides information only on the start time).

Now having the dates, we find out what music we've listened to during that time period, by using the `/recently-played` Spotify endpoint.

We get the response, format and filter the data a little bit, and again using Strava's API we update the description.


To get this running locally (because I have no intentions to host this anywhere):

- Clone the repo
- create an `.env` file with the following credentials from Spotify and Strava:

CLIENT_ID=my_client_id

CLIENT_SECRET=my_client_secret

STRAVA_CLIENT_ID=my_trava_client_id

STRAVA_SECRET=my_strava_client_secret


and then run 

`docker-compose up`

While I'm working on adding a celery beat to this project (so we can have this updater run let's say three times a day), we can just run `python3 auto_updater.py` from inside the running docker container.

Update: this is now a kubernetes project. Why? Because I have no idea, what's why.

In order to run this project locally and have it auto run (I have it set to run 3 times a day), you need kubectl and some kind of k8s environment in order to run this. (You can still totally use the docker-compose approach, you won't get the auto update that way). 

I am using minikube to run this project locally. 

All you need to do to get everything running is create a k8s secret - `played-secrets.yaml` that will hold your b64 encoded secrets like so:

```
apiVersion: v1
kind: Secret
metadata:
  name: played-secrets
type: Opaque
data:
  spotify-client-id: my-encripted-secret-client-id
```

As soon as you have that, all you need to do is 

```
kubectl apply -f played-secrets.yaml
kubectl apply -f recently-played.yaml
kubectl apply -f rec-played-cronjob.yaml
```

And then leave your computer running and enjoy life (or host this on GCP|AWS|AZURE, you're your own boss)


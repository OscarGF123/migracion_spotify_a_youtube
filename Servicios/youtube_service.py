import pickle
import os
import requests

from googleapiclient._apis.youtube.v3 import YouTubeResource
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]

class Youtube:

    def autenticar_youtube(self):
        creds = None

        # Reutilizar token si ya existe
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_1058694267118-fiaf0nugnl27h4qth1k1pp662am87mvm.apps.googleusercontent.com.json",  # ← descargado de Google Cloud Console
                SCOPES
            )
            creds = flow.run_local_server(port=8888)  # abre el navegador para autorizar

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build("youtube", "v3", credentials=creds)
    
    def buscar_en_youtube(self, track_spotify: dict, youtube_api_key: str) -> dict:
        # 1. Extraer metadata de Spotify
        nombre = track_spotify['name']
        artista = track_spotify['artists'][0]['name']
        query = f"{nombre} {artista}"

        # 2. Buscar en YouTube Data API v3
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 1,
            "key": youtube_api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        if not data.get('items'):
            print(data)
            return {"encontrado": False}

        video = data['items'][0]
        video_id = video['id']['videoId']

        return {
            "encontrado": True,
            "titulo": video['snippet']['title'],
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "video_id": video_id
        }
    
    def insertar_cancion(self, youtube_api: YouTubeResource):
        if not youtube_api:
            return None
        request: YouTubeResource = youtube_api.playlistItems().insert(
            part='snippet',
            body={
                'snippet':{
                    'playlistId': "PL8EBQIXOvk5oiQISB22LyAjbD1thP2OZT",
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': "4NRXx6U8ABQ"
                    }
                }
            }
        )
        response = request.execute()
        return response
    

import pickle
import os
import requests

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from googleapiclient._apis.youtube.v3 import YouTubeResource
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]

class Youtube:

    def autenticar_youtube(self) -> "YouTubeResource":
        creds = None

        # Reutilizar token si ya existe
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            cliente_json = None
            if os.path.exists("client_secret_1058694267118-fiaf0nugnl27h4qth1k1pp662am87mvm.apps.googleusercontent.com.json"):
                cliente_json = "client_secret_1058694267118-fiaf0nugnl27h4qth1k1pp662am87mvm.apps.googleusercontent.com.json"
            else:
                cliente_json = "client_secret_1058694267118-i2gujo33en6e0t53gf625bnl4ofsb7s9.apps.googleusercontent.com.json"
            flow = InstalledAppFlow.from_client_secrets_file(
                cliente_json,  # ← descargado de Google Cloud Console
                SCOPES
            )
            creds = flow.run_local_server(port=8888)  # abre el navegador para autorizar

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build("youtube", "v3", credentials=creds)
    
    def buscar_en_youtube(self, track_spotify: dict, youtube_api_key: "YouTubeResource") -> dict:
        # 1. Extraer metadata de Spotify
        nombre = track_spotify['name']
        artista = track_spotify['artist']
        query = f"{nombre} {artista}"

        request = youtube_api_key.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=1
        )

        response = request.execute()

        return response

    def listar_playlist(self, youtube_api_key: "YouTubeResource", listar_nombres=None):
        page_token = True
        plalists = []
        while page_token:
            request = youtube_api_key.playlists().list(
                part='snippet',
                mine=True,
                pageToken= '' if page_token == True else page_token
            )

            response = request.execute()
            plalists.extend(response.get('items'))
            page_token = response.get("nextPageToken")

        if listar_nombres:
            nombres = []
            for item in plalists:
                nombres.append({
                        "nombre": item['snippet'].get('title', None),
                        "id" : item['id']
                })
            return nombres
        return response

    def crear_playlist(self, youtube_api_key: "YouTubeResource", nombre_playlist: str):
        request = youtube_api_key.playlists().insert(
            part='snippet',
            body={
                'snippet':{
                    'title': nombre_playlist
                }
            }
        )
        response = request.execute()

        return response
        pass

    def eliminar_playlist(self, youtube_api_key: "YouTubeResource", id_playlist: str):
        request = youtube_api_key.playlists().delete(
            id=id_playlist
        )
        return request.execute()

    def insertar_cancion(self, youtube_api: "YouTubeResource"): 

        
        if not youtube_api:
            return None
        request: "YouTubeResource" = youtube_api.playlistItems().insert(
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
    

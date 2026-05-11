import requests

def buscar_en_youtube(track_spotify: dict, youtube_api_key: str) -> dict:
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

def obtener_usuario_id(youtube_api_key: str, handle: str):
    
    url = f"https://www.googleapis.com/youtube/v3/channels"

    params = {
        'part': 'id',
        'forHandle': handle,
        'key': youtube_api_key,
    }

    return requests.get(url=url, params=params).json()
# Tienes el track de Spotify
track = {
    "name": "Blindin Lights",
    "artists": [{"name": "The Weekn"}]
}

def listar_listas_reproduccion(youtube_api_key: str, channel_id: str):
    url = "https://www.googleapis.com/youtube/v3/playlists"
    params = {
        'part': 'id',
        'channelId': channel_id,
        'key': youtube_api_key
    }

    return requests.get(url=url, params=params).json()




# print(resultado)

#print(obtener_usuario_id("AIzaSyA7NQful3XQQjADeI01WpnEXF_ay7OS-BQ", "@O_K_A"))
# print(listar_listas_reproduccion("AIzaSyA7NQful3XQQjADeI01WpnEXF_ay7OS-BQ", 'UCJEA5qWVwUppyFhGWYXf5fA'))

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def autenticar_youtube():
    creds = None

    # Reutilizar token si ya existe
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret_1058694267118-v6fb98hep04qov3u5c9ll3kbd34ab5c8.apps.googleusercontent.com.json",  # ← descargado de Google Cloud Console
            SCOPES
        )
        creds = flow.run_local_server(port=8888)  # abre el navegador para autorizar

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)
def crear_lista_reproduccion():
    youtube = autenticar_youtube()
    request = youtube.playlists().insert(
        part="snippet",
        body={
            'snippet': {
                'title': 'playlist_prueba'
            }
        }
    )
    response = request.execute()
    return response

def insertar_cancion():
    youtube = autenticar_youtube()
    request = youtube.playlistItems().insert(
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

# print(crear_lista_reproduccion())
# resultado = buscar_en_youtube(track, "AIzaSyA7NQful3XQQjADeI01WpnEXF_ay7OS-BQ")
# print(resultado)
print(insertar_cancion())
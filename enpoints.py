import time
import requests
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from googleapiclient._apis.youtube.v3 import YouTubeResource
from flask import jsonify, Blueprint, request, session, redirect, url_for, current_app

from Servicios.spotify_service import Spotify
from Servicios.youtube_service import Youtube

# Crear Blueprint y indicar en que archivo vive
endpoints_bp = Blueprint('spotify', __name__)
spotify = Spotify()
youtube = Youtube()

def validar_token_spotify(funcion: callable):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        if not session.get("spotify_token"):
            return autorizacion1_spotify()
        # Comprobar que el token no ha expirado
        url = "https://api.spotify.com/v1/me"
        headers = {'Authorization': f'Bearer {session.get('spotify_token')}'}
        response: dict = requests.get(url, headers=headers).json()
        if response.get('error', None):
            if response['error']['message'] == "The access token expired":
                return autorizacion1_spotify()
        return funcion(*args, **kwargs)
    return wrapper
    

@endpoints_bp.route('/')
def root():
    return "home"

@endpoints_bp.route("/auth1_spotify")
def autorizacion1_spotify():
    auth_url = spotify.codigo_autorizacion()
    
    return redirect(auth_url) 




@endpoints_bp.route('/obtener_playlist')
def get_users_playlist():
    token = session.get('spotify_token')
    print(f'token {token}')
    data = spotify.obtener_playlist_usuario(token)

    if not data:
        return jsonify({'message': 'no se obtuvo el token del usuario'})

    return jsonify({"data": data})

@endpoints_bp.route('/obtener_items_playlist')
def get_playlists_items():
    token = session.get("spotify_token")

    print(f"token: {token}")
    
    return jsonify({"data": spotify.obtener_items_playlist(token)})


@endpoints_bp.route('/callback')
def callback():
    code = request.args.get("code")
    code_verifier = spotify.code_verifier

    data: dict = spotify.obtener_token(code=code, code_verifier=code_verifier)

    session['spotify_token'] = data.get("access_token")

    print("Autenticacion de la api de spotify completada")

    return redirect(url_for('spotify.iniciar_migraciones'))

@endpoints_bp.route('/migracion_canciones')
@validar_token_spotify
def iniciar_migraciones():
    
    youtube_api: "YouTubeResource" = youtube.autenticar_youtube()

    current_app.logger.info("La Autenticacion del api de youtube fue exitosa")
    
    token = session.get("spotify_token")

    playlists = spotify.obtener_playlist_usuario(token)

    for k, v in playlists.items():
        print(f"k: {k}, v: {v}")

    # track = {
    #     'name': "\\\\\\",
    #     'artist': "c678924"
    # }
    # response = youtube.buscar_en_youtube(track, youtube_api)

    return jsonify({'songs': playlists})
    
@endpoints_bp.route('/end1')
def end1():
    session['spotify_token'] = None
    return jsonify({"hola": "hola"})

@endpoints_bp.route('/end2')
def end2():
    hola = session.get("spotify_token")
    return jsonify({"hola": hola})

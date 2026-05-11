import time

from googleapiclient._apis.youtube.v3 import YouTubeResource

from flask import jsonify, Blueprint, request, session, redirect, url_for
from Servicios.spotify_service import Spotify
from Servicios.youtube_service import Youtube

# Crear Blueprint y indicar en que archivo vive
endpoints_bp = Blueprint('spotify', __name__)
spotify = Spotify()
youtube = Youtube()

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
    code_verifier = Spotify().code_verifier

    data: dict = spotify.obtener_token(code=code, code_verifier=code_verifier)

    session['spotify_token'] = data.get("access_token")

    print("Autenticacion de la api de spotify completada")

    return redirect(url_for('spotify.iniciar_migraciones'))

@endpoints_bp.route('/migracion_canciones')
def iniciar_migraciones():
    
    youtube_api: YouTubeResource = youtube.autenticar_youtube()

    if not session.get("spotify_token"):
        return autorizacion1_spotify()

    return jsonify({'token': session.get("spotify_token")})
    
@endpoints_bp.route('/end1')
def end1():
    session['spotify_token'] = None
    return jsonify({"hola": "hola"})

@endpoints_bp.route('/end2')
def end2():
    hola = session.get("spotify_token")
    return jsonify({"hola": hola})

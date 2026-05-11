from flask import jsonify, Blueprint, request, session, redirect
from Servicios.SpotifyService import Spotify

# Crear Blueprint y indicar en que archivo vive
endpoints_bp = Blueprint('spotify', __name__)
spotify = Spotify()

@endpoints_bp.route('/')
def root():
    return "home"

@endpoints_bp.route("/auth1_spotify")
def autorizacion1_spotify():

    auth_url = spotify.codigo_autorizacion()
    return redirect(auth_url)     


@endpoints_bp.route('/callback')
def callback():
    code = request.args.get("code")
    code_verifier = Spotify().code_verifier

    data: dict = spotify.obtener_token(code=code, code_verifier=code_verifier)

    session['spotify_token'] = data.get("access_token")

    return jsonify({'code': code, 'code_verifier': code_verifier, 'token': data.get("access_token")})
@endpoints_bp.route('/obtener_playlist')
def get_users_playlist():
    token = session.get('spotify_token')
    data = spotify.obtener_playlist_usuario(token)

    if not data:
        return jsonify({'message': 'no se obtuvo el token del usuario'})

    return jsonify({"data": data})

@endpoints_bp.route('/obtener_items_playlist')
def get_playlists_items():
    token = session.get("spotify_token")
    
    return jsonify({"data": spotify.obtener_items_playlist(token)})

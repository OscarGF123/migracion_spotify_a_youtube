import hashlib
import base64
import secrets
import requests
from urllib.parse import urlencode
from flask import current_app, jsonify, session
# Solo para el api de spotify
def get_headers(token):
    return {
        'Authorization': f'Bearer {token}'
    }

class Spotify:

    code_verifier = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(64))
    api_url = "https://api.spotify.com"
    accounts_url = "https://accounts.spotify.com"
    client_id = "c76620898070401581ce714613e607e1"
    redirect_url = "http://127.0.0.1:5000/callback"
    
    def encriptar_sha256(self,code_verifier: str):
        # ✅ .digest() retorna bytes crudos, NO texto hexadecimal
        digest = hashlib.sha256(code_verifier.encode()).digest()
        # ✅ urlsafe_b64encode usa - y _ en lugar de + y /
        # ✅ .rstrip(b'=') elimina el padding requerido por el estándar PKCE
        return base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    
    def codigo_autorizacion(self):
        code_challenge = self.encriptar_sha256(self.code_verifier)
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_url,
            'scope': 'playlist-read-private%20user-library-read',
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge
        }

        auth_url = f"{self.accounts_url}/authorize?{urlencode(params)}"

        return auth_url

    def obtener_token(self, code: str, code_verifier: str):
        url = f"{self.accounts_url}/api/token"
        payload = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_url,
            "code_verifier": code_verifier,
        }

        return requests.post(url=url, data=payload).json()
    




    def obtener_playlist_usuario(self, token: str):
        if not token:
            return None
        
        url="https://api.spotify.com/v1/me/playlists"
        response = requests.get(url, headers=get_headers(token)).json()

        if response.get('items', None):
            current_app.logger.info("Se han recuperado las playlist del api correctamente")
        
        else:
            current_app.logger.error(f"No se ha podido recopilar las playlist {response}")
            return jsonify({'error': 'spotify_api', 'message': f'No se ha podido playlist las playlist {response}'})
        
        current_app.logger.info(f"Recopilando ids e imagenes de las playlists")

        playlists = {}

        for item in response.get('items'):
            playlists[item['name']] = {
                'id': item['id'],
                'images': item['images']
            }
        current_app.logger.info(f"¡Recopilacion de plalist lista! ")

        return playlists
    
    def obtener_tracks_guardados(self, token: str):
        url = "https://api.spotify.com/v1/me/tracks"
        tracks = []
        params = {
            'limit': '50'
        }
        current_app.logger.info("Recopilando canciones guardadas...")
        while url:
            response = requests.get(url, headers=get_headers(token), params=params).json()
            for item in response.get('items', []):
                tracks.insert(0, {
                    'trackName': item['track'].get('name'),
                    'artist': item['track']['artists'][0].get('name'),
                    'added_at': item.get("added_at")
                })
            url = response.get('next')
        return tracks

    
    def obtener_items_playlist(self, token: str, playlist_id: str):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items"
        params = {
            'limit': '50'
        }
        tracks = []

        while url:
            response = requests.get(url=url, headers=get_headers(token), params=params).json()

            for item in response.get('items', []):
                tracks.append({
                    'name': item['item'].get('name'),
                    'artist': item['item']['artists'][0].get('name'),
                    'added_at': item.get('added_at'),
                    'id': item['item'].get('id')
                })
            url = response.get('next')
        return tracks


        

import hashlib
import base64
import secrets
import requests
from urllib.parse import urlencode

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
    user_id = "6ix2y1slrp76l5d118hf05pqp"
    
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
            'scope': 'playlist-read-private',
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge
        }

        auth_url = f"{self.accounts_url}/authorize?{urlencode(params)}"

        return auth_url

    def obtener_token(self,code: str, code_verifier: str):
        url = f"{self.accounts_url}/api/token"
        payload = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_url,
            "code_verifier": code_verifier,
        }
        # headers = {
        #         'Content-Type': 'application/x-www-form-urlencoded',
        #     }
        return requests.post(url=url, data=payload).json()

    def obtener_playlist_usuario(self, token: str):
        if not token:
            return None

        return requests.get(url="https://api.spotify.com/v1/me/playlists", headers=get_headers(token)).json()
    
    def obtener_items_playlist(self, token):
        url = "https://api.spotify.com/v1/playlists/3a9t7dhAorFCf9eGaSHXn1/items"
        return requests.get(url=url, headers=get_headers(token)).json()
        

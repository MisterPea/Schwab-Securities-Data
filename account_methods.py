from requests_oauthlib import OAuth2Session
import os
import time
import webbrowser
import json
from requests.auth import HTTPBasicAuth

class AccountMethods:
    def __init__(self):
        self.app_key = os.environ.get("APP_KEY")
        self.secret_key = os.environ.get("SECRET_KEY")
        self.client_id = os.environ.get("CLIENT_ID")
        self.authorize_url = "https://api.schwabapi.com/v1/oauth/authorize"
        self.response_type = "code"
        self.scope = "api"
        self.redirect_uri = "https://127.0.0.1"
        self.token_url = "https://api.schwabapi.com/v1/oauth/token"
        self.flow = "authorizationCode"
        self.token = self.retrieve_local_token() or self.set_token()

    def set_token(self):
        """Method that furnishes a token to the class"""
        # Create session
        oauth = OAuth2Session(self.app_key, redirect_uri=self.redirect_uri, scope=self.scope)

        # Get user approval
        authorization_url, _ = oauth.authorization_url(self.authorize_url)
        webbrowser.open(authorization_url)

        # Get auth code from redirect
        authorization_response = input("Enter the full callback URL:")

        # Fetch token
        token = oauth.fetch_token(
            self.token_url,
            authorization_response=authorization_response,
            client_secret=self.secret_key,
        )

        # Note expiration
        token["expires_at"] = time.time() + token["expires_in"]
        self.save_token(token)
        return token

    def save_token(self, token):
        """Save token to file"""
        with open("token.json", "w") as f:
            json.dump(token, f)

    def retrieve_local_token(self):
        """Attempt to load token from local file"""
        if os.path.exists("token.json"):
            with open("token.json", "r") as f:
                token = json.load(f)
            return token
        return None

    def is_token_valid(self):
        """Check that token is valid by expiration time"""
        return time.time() < self.token["expires_at"]

    def refresh_token(self):
        """Refresh expired tokens using existing token"""
        oauth = OAuth2Session(self.app_key, token=self.token)
        auth = HTTPBasicAuth(self.app_key, self.secret_key)
        # options = {"client_id": self.app_key, "client_secret": self.secret_key}

        # Attempt to refresh token
        try:
            new_token = oauth.refresh_token(self.token_url, auth=auth, refresh_token=self.token["refresh_token"])
            # new_token = oauth.refresh_token(self.token_url, **options)
            new_token["expires_at"] = time.time() + new_token["expires_in"]
            self.token = new_token
            self.save_token(new_token)
            return new_token
        except Exception as err:
            print(f"Failed to renew token: {err}")
            return None

    def get_token(self):
        """Method to check token validity if token, if it's invalid we renew the token"""
        if not self.is_token_valid():
            # Token is not valid
            new_token = self.refresh_token()
            if new_token:
                return new_token
            else:
                # On failure to renew token
                self.token = self.set_token()
                return self.token
        else:
            # Token is still valid
            return self.token

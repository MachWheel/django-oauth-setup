from urllib.parse import urlencode

import requests
from django.conf import settings
from django.urls import reverse_lazy

from . import _config
from ._models import GoogleAccessTokens


class GoogleLoginService:
    API_URI = reverse_lazy("api_oauth_google_callback")
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = _config.get_service_credentials()

    @property
    def _redirect_uri(self) -> str:
        return f"{settings.BASE_BACKEND_URL}{self.API_URI}"

    def get_authorization_url(self) -> tuple[str, str]:
        state = _config.generate_state_session_token()
        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": self._redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{urlencode(params)}"
        return authorization_url, state

    def get_tokens(self, *, code: str) -> GoogleAccessTokens:
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": self._redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
        if not response.ok:
            raise ValueError("Failed to obtain access token from Google.")

        return GoogleAccessTokens(response.json())

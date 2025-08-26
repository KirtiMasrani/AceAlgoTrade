import time
from typing import Optional

import requests


class TokenManager:
    """Handle token acquisition and refresh logic for API providers."""

    def __init__(
        self,
        auth_url: str,
        refresh_url: str,
        client_id: str,
        client_secret: str,
    ) -> None:
        self.auth_url = auth_url
        self.refresh_url = refresh_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.expiry: float = 0.0

    def _request_token(self, url: str, data: dict) -> dict:
        resp = requests.post(url, data=data, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        self.access_token = payload.get("access_token")
        self.refresh_token = payload.get("refresh_token", self.refresh_token)
        expires_in = payload.get("expires_in", 0)
        self.expiry = time.time() + expires_in
        return payload

    def authenticate(self, scope: Optional[str] = None) -> dict:
        """Acquire a new access token."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if scope:
            data["scope"] = scope
        return self._request_token(self.auth_url, data)

    def refresh(self) -> dict:
        """Refresh an existing access token."""
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        return self._request_token(self.refresh_url, data)

    def get_token(self) -> str:
        """Return a valid access token, refreshing if necessary."""
        if self.access_token and time.time() < self.expiry - 60:
            return self.access_token
        if self.refresh_token:
            self.refresh()
        else:
            self.authenticate()
        if not self.access_token:
            raise RuntimeError("Failed to obtain access token")
        return self.access_token

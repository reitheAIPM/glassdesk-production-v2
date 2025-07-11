# LEGACY: This file is deprecated. Use app/enhanced_oauth_manager.py (EnhancedOAuthManager) for all new OAuth logic.
# This file is retained for reference only and should not be used for new development.

from flask import Flask, redirect, request, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Example for Google OAuth 2.0
GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
GOOGLE_REDIRECT_URI = "http://localhost:5000/oauth2callback"


@app.route("/login")
def login():
    scope = "https://www.googleapis.com/auth/gmail.readonly"
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope={scope}"
        "&access_type=offline&prompt=consent"
    )
    return redirect(auth_url)


@app.route("/oauth2callback")
def oauth2callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = requests.post(token_url, data=data)
    token_response = r.json()
    session["credentials"] = token_response
    return "OAuth 2.0 flow completed! You can close this window."

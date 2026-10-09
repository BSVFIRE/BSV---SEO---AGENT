"""Engangsscript: lager Google Ads refresh token.
Kjør lokalt: python scripts/get_refresh_token.py <client_id> <client_secret>
Logg inn med Google-brukeren som har «Read only»-tilgang i Google Ads."""
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

cfg = {"installed": {"client_id": sys.argv[1], "client_secret": sys.argv[2],
                     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                     "token_uri": "https://oauth2.googleapis.com/token",
                     "redirect_uris": ["http://localhost"]}}
flow = InstalledAppFlow.from_client_config(cfg, scopes=["https://www.googleapis.com/auth/adwords"])
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nGOOGLE_ADS_REFRESH_TOKEN =", creds.refresh_token)

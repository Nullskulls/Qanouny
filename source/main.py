import os
from slack_bolt import App
# from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
# USER_SCOPES = ["channels:history", "groups:history", "im:history", "mpim:history", "chat:write"] if not (set_scopes:= os.environ.get("USER_SCOPES")) else set_scopes.split(',')
# CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
# CLIENT_ID = os.environ.get("CLIENT_ID")

# for a later day

# oauth_settings = OAuthSettings(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     scopes=USER_SCOPES,
# )

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)


if __name__ == "__main__":
    bot = SocketModeHandler(app).start()


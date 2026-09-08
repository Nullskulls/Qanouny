import os
from slack_bolt import App
# from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from views import RenderTemplate
from auth import Encrypter

load_dotenv()

SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
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

render_template = RenderTemplate(app.client)

encrypter = Encrypter()

@app.command("/wipey")
def wipe_command(ack, body):
    ack()

@app.event("app_home_opened")
def home_tab(client, event, logger):
    render_template.render_view(event, render_template.render_home_tab())

@app.action("submit_token")
def handle_submit(ack, body):
    ack()

    user_id = body["user"]["id"]

    token = (
        body["view"]["state"]["values"]["token_input"]["plain_text_input-action"]["value"]
    )

    passkey = (
        body["view"]["state"]["values"]["encryption_key_input"]["encryption-action"]["value"]
    )

    enc_token = encrypter.encrypt_token(passkey, token)

if __name__ == "__main__":
    socket_mode_handler = SocketModeHandler(app=app, app_token=SLACK_APP_TOKEN)
    socket_mode_handler.start()


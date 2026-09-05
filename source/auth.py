import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
key = Fernet.generate_key()
f = Fernet(key)

token = input("Enter your Slack Bot Token: ")

encrypted_token = f.encrypt(bytes(token, 'utf-8'))

decrypted_token = f.decrypt(encrypted_token)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

def get_token(user_id):
    return decrypted_token.decode('utf-8')

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

if __name__ == "__main__":
    bot = SocketModeHandler(app).start()
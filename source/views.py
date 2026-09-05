import logging

logger = logging.getLogger(__name__)

class RenderTemplate:

    def __init__(self, client):
        self.client = client

    def render_view(self, event, view):
        print(f"Rendering view for user: {event['user']}")
        try:
            self.client.views_publish(
                user_id=event["user"],
                view=view
            )
        except Exception as e:
            logger.error(f"Error publishing view: {e}")

    def render_home_tab(self):
        view = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Welcome to the Wipey Bot where you can easily delete your messages with a single command!"
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "App Token",
                        # "emoji": True
                    },
                    # "optional": False
                }
            ]
        }
        
        return view
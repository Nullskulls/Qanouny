import time
from views import logger
from slack_sdk.errors import SlackApiError

class MessageHandler:

    def purge_message(self, user_app, message_ts, channel, thread_ts=None):
        try:
            user_app.chat.delete(
                channel=channel,
                ts=message_ts,
                thread_ts=thread_ts
            )
        except SlackApiError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 1))
                time.sleep(retry_after)
                self.purge_message(user_app, message_ts, channel, thread_ts)
            else:
                logger.error(f"Error purging message: {e}")


import slack
import os
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

# Load environment path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['TEST_SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['TEST_SLACK_TOKEN'])

# Get the ID of the bot
BOT_ID = client.api_call("auth.test")["user_id"]

@slack_event_adapter.on('message')
def call_and_response(payLoad):
    event = payLoad.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    # Post "Feel the Burn" if a message says "It's 3:42!"
    if(user_id != BOT_ID and (text == "It's 3:42!")):
        client.chat_postMessage(channel=channel_id,text="Feel the burn!")


if __name__ == "__main__":
    app.run(debug=True)
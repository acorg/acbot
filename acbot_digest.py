
# ------------------------------------------------
# acbot_digest.py
#
# This file contains code that uses the acbot app and it's privilages to make
# api calls to slack and access messages in the channel history. It could be run
# as a cron job and doesn't include any runs independently from the code that runs
# on the server and dynamically responds to events in slack like @acbot mentions.
# In fact you could run this code locally and it would work, provided you have the
# correct SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET defined in your shell environment.
#
# See https://api.slack.com/web#methods for a list of web api methods
# ------------------------------------------------

# Import necessary modules
from slack_bolt import App
import os
import json
from datetime import datetime, timedelta

# Initialize the acbot app object
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Fetch all public channels to which acbot belongs
channels = slack_app.client.users_conversations(
    types="public_channel"
)

# Setup a dictionary for storing the message history
message_history = {}

# Cycle through the channels
for channel in channels["channels"]:

    # Get the channel id and name
    channel_id = channel["id"]
    channel_name = channel["name"]

    # Get the timestamp for 7 days ago, this will be used in the query to fetch message history
    datetime_7_days_ago = datetime.now() - timedelta(days=7)
    timestamp_7_days_ago = int(datetime_7_days_ago.timestamp())

    # Fetch message from this channel from the past 7 days using the slack web api
    # "conversations.history" method (https://api.slack.com/methods/conversations.history)
    messages = slack_app.client.conversations_history(
        channel=channel["id"],
        oldest=timestamp_7_days_ago,
        limit=1000
    )["messages"]

    # Add a record of the messages to the message history object
    message_history[channel_id] = {
        "name": channel_name,
        "messages": messages
    }


# Output a json summary of the messages
with open('messages/messages.json', 'w') as outfile:
    json.dump(message_history, outfile)


# ------------------------------------------------
# acbot.py
# This file contains the main code for acbot, defining how acbot responds to slack
# events like a user posting a message in a channel or mentioning @acbot
#
# At the moment basically all code is in this file:
#
# - Code to set up the intial acbot App object, with appropriate tokens
# - Code to define how acbot responds to slack_events
# - Code to set up the flask app that ultimately serves acbot to gunicorn
#
# It would probably be nice to split this all up a bit and run acbot as a proper python module
#
# ------------------------------------------------

# Import flask, the slack_bolt library and necessary adapters
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Import other packages we will use
import os
import re

# --- ACBOT SETUP ------------

# Initializes acbot with the bot token and signing secret
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# This is a listener for whenever a message is posted in a channel in which acbot is a member
# You could filter for messages matching a pattern but here we catch everything
@slack_app.message(re.compile(".*"))
def message_action(client, message, say):

    # I've left a commented example of how you can make a call to the slack api through 'client' in order to ascertain
    # the name of a user from their user id
    #
    # Get user id and text from message object
    # userid = message['user']
    # text   = message['text']
    #
    # Make a call to the slack api to get user info for that user id
    # userinfo = client.users_info(
    #     user=user
    # )
    #
    # Say the name of the user
    # say(userinfo["user"]["real_name"])

    pass


# Here we define a listener for some mentioning @acbot in a channel to which acbot belongs
@slack_app.event("app_mention")
def say_ack(event, client, say):
    say("ack")


# --- FLASK SETUP ------------
app = Flask(__name__)
handler = SlackRequestHandler(slack_app)


# Boiler plate code
@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


# Here we define what is shown at the addresss acbot.shwilks.co.uk when acbot is online
@app.route("/")
def hello():
    return 'acbot online'

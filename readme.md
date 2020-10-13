# acbot

This is the code repo for acbot, the antigenic cartography bot that says "ack". But maybe some other useful things eventually too.

## Files
__acbot.py__  
The core of acbot, this code sets up the acbot server to respond to events like mentions to @acbot in channels and responding by saying "ack"

__acbot_digest.py__  
This is code that can be run as a cron job (also locally) to scrape all the messages sent in the channels to which acbot belongs over the past 7 days (or any other time period)

__acbot_formatmail.py__  
This could be where we write code to format the messages scraped from slack into a nice html email to mail round to everyone

__acbot_email.py__  
This could be where we write code to actually send the html email through the appropriate smtp server

## Guides
- [A tutorial for setting up a slack both with slack_bolt](https://api.slack.com/start/building/bolt-python)  
- [slack_bolt documentation on how to respond to different events](https://slack.dev/bolt-python/concepts)
- [A list of the slack web_api methods that you can use to do things like scrape messages from slack](https://api.slack.com/web#methods)
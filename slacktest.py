# test module for slack integration
import os
import time
from slackclient import SlackClient
import setup
import re

config_loc = 'config/config.ini'

config = setup.fetchauth(config_loc, 'SLACK')
# Set up slack client
slack_client = SlackClient(config['SLACK']['bot_token'])
# Bot ID to be set at startup
BotID = None
# RTM read delay
rtm_read_delay = 1
commandlist = ['!status', '!help', '!halp']
dmlist = ['enroll']
mention_regex = "&<@(" + str(BotID) + ")>(.*)"


def parse_bot_commands(slack_events):

    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            # Print out events for now
            print(event['type'], '||', event['channel'], '||', event['text'])

            user_id, message = parse_direct_mention(event["text"])
            if user_id == BotID:
                return message, event["channel"]
            elif any(command in event['text'] for command in commandlist):
                return event['text'], event['channel']

    return None, None


def parse_direct_mention(message_text):
    matches = re.search(mention_regex, message_text)
    # Group one will be the username, group two will be the message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):

    default_response = "What?"
    response = None

    if command.startswith('!status'):
        response = "There are some trains"
    elif command.startswith('!help'):
        response = "Help yourself"
    else:
        response = '(╯°□°）╯︵ ┻━┻'

    # Send back a response
    slack_client.api_call("chat.postMessage", channel=channel, 
        text=response
        )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot connected and running")
        # Read user id for workspace
        BotID = slack_client.api_call("auth.test")["user_id"]
        print(BotID)
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(rtm_read_delay)
    else:
        print("Connection failed")

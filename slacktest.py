# test module for slack integration
import os
import time
from slackclient import SlackClient
import setup

config_loc = 'config/config.ini'

config = setup.fetchauth(config_loc, 'SLACK')
# Set up slack client
slack_client = SlackClient(config['SLACK']['bot_token'])
# Bot ID to be set at startup
BotID = None
# RTM read delay
rtm_read_delay = 1
examplecommand = '!status'


def parse_bot_commands(slack_events):

    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == BotID:
                return message, event["channel"]
    
    return None, None

def handle_command(command, channel):

    default_response = "What?"
    response = None

    if command.startswith(examplecommand):
        response = "This is the only response"

    # Send back a response
    slack_client.api_call("chat.postMessage", channel=channel, 
        text=response or default_response
        )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot connected and running")
        # Read user id for workspace
        BotID = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                # handle command
                pass
            time.sleep(rtm_read_delay)
    else:
        print("Connection failed")

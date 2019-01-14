# test module for slack integration
import os
import time
from slackclient import SlackClient
import setup

# Get config from file and start bot
config_loc = 'config/config.ini'
config = setup.fetchauth(config_loc, 'SLACK')
slack_client = SlackClient(config['SLACK']['bot_token'])
# RTM read delay
rtm_read_delay = 1
commandlist = ['!status', '!help', '!halp']


def parse_messages(slack_events):
    # Loop through all incoming events
    for event in slack_events:
        # Only do anything if this is a message
        if event['type'] == 'message' and not "subtype" in event:
            # Print messages to console for debug purposes
            print(event['type'], '||', event['channel'], '||', event['text'])
            # If message is a DM, do DM processing
            if event['text'].startswith(Bot_Mention) == True:
                process_message(event['text'], event['channel'], True, event['user'])
            # else, if the message is a command, process normal commands
            elif event['text'].startswith(tuple(commandlist)):
                process_message(event['text'], event['channel'])
    return None

def bot_setup():
    # Get bot info
    BotID = slack_client.api_call("auth.test")["user_id"]
    BotName = slack_client.api_call("auth.test")["user"]
    print("Bot {} connected as {}".format(BotName, BotID))
    BotChannels = slack_client.api_call("users.conversations",
                                        types='private_channel')['channels']
    # Send out an online message to bot channels        
    message = 'PTV Bot Connected'
    Bot_Mention = '<@{}>'.format(BotID)

    print(Bot_Mention, 'is my keyword')

    for channel in BotChannels:
        bot_response(channel['id'], message)

    return BotID, BotName, BotChannels, Bot_Mention




def process_message(message, channel, dm_flag=False, user=None):
    if dm_flag == True:
        print(str(user), message)


def bot_response(channel, message):
    # Post a plaintext message
    slack_client.api_call("chat.postMessage", channel=channel, text=message)



if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        # Get bot info
        BotID, BotName, BotChannels, Bot_Mention = bot_setup()

        while True:
            x = parse_messages(slack_client.rtm_read())
            time.sleep(rtm_read_delay)


    else:
        print("Connection failed")

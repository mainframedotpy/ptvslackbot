# test module for slack integration
import os
import time
from slackclient import SlackClient
import configuration

# Get config from file and start bot
config_loc = 'config/config.ini'
config = configuration.fetchauth(config_loc, 'SLACK')
slack_client = SlackClient(config['SLACK']['bot_token'])
# RTM read delay
rtm_read_delay = 1
commandlist = ['!status', '!help', '!halp']


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

    reply = {}
    reply['text'] = message
    for channel in BotChannels:
        reply['channel'] = channel['id']
        bot_response(reply)

    return BotID, BotName, BotChannels, Bot_Mention


def parse_messages(slack_events):
    # Loop through all incoming events
    for event in slack_events:
        # Only do anything if this is a message
        if event['type'] == 'message' and not "subtype" in event:
            # Print messages to console for debug purposes
            print(event['type'], '||', event['user'], event['channel'], '||', event['text'])
            # If message is a DM, do DM processing
            if event['text'].startswith(Bot_Mention) == True:
                return event, True 
            # else, if the message is a command, process normal commands
            elif event['text'].startswith(tuple(commandlist)):
                return event, False
    return None, None


def process_message(event, dm_flag=False):
    # Initialise a reply
    reply = {}
    # Check for a DM
    if dm_flag == True:
        # DM Processing goes here
        # Dummy for now
        reply['text'] = 'Hello {}, I am a usless bot'.format(event['user'])
        reply['channel'] = event['channel']
        reply['ts'] = event['ts']
        
        return reply
    
    else:
        reply['channel']  = event['channel'] 
        
        if event['text'].startswith('!status'):
            reply['text'] = 'There are no trains today'
        elif event['text'].startswith('!halp'):
            reply['text'] = '(╯°□°）╯︵ ┻━┻'    
        else:
            reply['text'] = 'botbotbotbotbot'
        return reply
        
    

def bot_response(event):
    if 'ts' in event:
        slack_client.api_call("chat.postMessage", 
                            channel=event['channel'],
                            text=event['text'],
                            thread_ts=event['ts']
                            )
    else:
        slack_client.api_call("chat.postMessage", 
                            channel=event['channel'],   
                            text=event['text']
                            )



if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        # Set up the bot and get bot info
        BotID, BotName, BotChannels, Bot_Mention = bot_setup()
        
        # Start listen loop 
        while True:
            event, flag = parse_messages(slack_client.rtm_read())
            if event != None:
                out_message = process_message(event, flag)
                bot_response(out_message)

            time.sleep(rtm_read_delay)

    # If bot can't connect, print error
    else:
        print("Connection failed")

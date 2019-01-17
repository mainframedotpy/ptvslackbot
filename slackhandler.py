# test module for slack integration
import os
import time
from slackclient import SlackClient
import configuration

# RTM read delay
rtm_read_delay = 1
commandlist = ['!status', '!help', '!halp']


def bot_setup(bothandle):
    # Get bot info
    BotID = bothandle.api_call("auth.test")["user_id"]
    BotName = bothandle.api_call("auth.test")["user"]
    print("Bot {} connected as {}".format(BotName, BotID))
    BotChannels = bothandle.api_call("users.conversations",
                                        types='private_channel')['channels']
    # Send out an online message to bot channels        
    message = 'PTV Bot Connected'
    Bot_Mention = '<@{}>'.format(BotID)

    print(Bot_Mention, 'is my keyword')

    reply = {}
    reply['text'] = message
    for channel in BotChannels:
        reply['channel'] = channel['id']
        bot_response(bothandle, reply)

    return BotID, BotName, BotChannels, Bot_Mention


def parse_messages(slack_events, BotID, Bot_Mention):
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


def process_message(event, routes, dm_flag=False):
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
        if event['text'].strip() == "!status":
            reply['text'] = ''
            for i in routes:
                reply['text'] += "*{}*: {}\n".format(i, routes[i]['Status'])
        elif event['text'].startswith('!status'):
            line = event['text'][8:].strip()
            if line.lower() in [k.lower() for k in routes.keys()]:
                reply['text'] = "*{}*: {}".format(line.title(), routes[line.title()]['Status_Long'])
            else:
                reply['text'] = "Not a valid line"
        elif event['text'].startswith('!halp'):
            reply['text'] = '(╯°□°）╯︵ ┻━┻'    
        else:
            reply['text'] = 'botbotbotbotbot'
        return reply
        
    

def bot_response(bothandle, event):
    if 'ts' in event:
        bothandle.api_call("chat.postMessage", 
                            channel=event['channel'],
                            text=event['text'],
                            thread_ts=event['ts']
                            )
    else:
        bothandle.api_call("chat.postMessage", 
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

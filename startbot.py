from ptvclass import PTVAPIClass
import slackhandler
from slackclient import SlackClient
import configuration 
import time

# location of config file, this will eventually be replaced with env variables
config_loc = 'config/config.ini'

if __name__ == "__main__":
    # Fetch credentials for PTV and Slack
    config = configuration.fetchauth(config_loc)
    print("fetched config")
    # Establish a new session to PTV and SLACK
    ptv_connect = PTVAPIClass(config['PTV']['ptv_devid'], config['PTV']['ptv_key'])
    print("ptv class created")
    slack_client = SlackClient(config['SLACK']['bot_token'])
    print("connected to slack")

    #PTV setup 
    ptv_connect.getallstatus()
    print("All Routes Updated!")

    if slack_client.rtm_connect(with_team_state=False):
        BotID, BotName, BotChannels, Bot_Mention = slackhandler.bot_setup(slack_client)

        # Start listening to slack messages
        while True:
            event, flag = slackhandler.parse_messages(slack_client.rtm_read(), BotID, Bot_Mention)
            if event != None:
                out_message = slackhandler.process_message(event, ptv_connect.routes, flag)
                slackhandler.bot_response(slack_client, out_message)

            time.sleep(slackhandler.rtm_read_delay)
    
    else:
        print("Connection Failed")
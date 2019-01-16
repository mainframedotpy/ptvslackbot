from ptvclass import PTVAPIClass
import slackhandler
import slackclient
import configuration 

# location of config file, this will eventually be replaced with env variables
config_loc = 'config/config.ini'

# print(connection.routes)

if __name__ == "__main__":
    # Fetch credentials for PTV and Slack
    config = configuration.fetchauth(config_loc)
    # Establish a new session to PTV and SLACK
    connection = PTVAPIClass(config['PTV']['ptv_devid'], config['PTV']['ptv_key'])
    # slack_client = SlackClient(config['SLACK']['bot_token'])
    connection.getallstatus()
    print(connection.routes)
    
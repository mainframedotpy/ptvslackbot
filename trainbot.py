from ptvclass import PTVAPIClass
import setup 

# Don't store in plaintext
ptv_devid = ''
ptv_key = ''
config_loc = 'config/config.ini'

# Verify config exists and has valid contents
if setup.setuphandler(config_loc) == False:
    print("No valid config found")
else:
    print("Config Found")

# Fetch credentials for PTV
config = setup.fetchauth(config_loc, 'PTV')

# Establish a new session
connection = PTVAPIClass(config['PTV']['ptv_devid'], config['PTV']['ptv_key'])

# Dummy sections
# print(connection.routes)
pass
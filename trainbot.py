from ptvclass import PTVAPIClass
import setup

# Don't store in plaintext
ptv_devid = ''
ptv_key = ''
config_loc = 'config/config.ini'

# Initialise config file


# Establish a new session
connection = PTVAPIClass(ptv_devid, ptv_key)

# Dummy sections
print(connection.routes)
pass
import os

config_loc = 'config/config.ini'

if os.path.isfile(config_loc):
    print('working')
else:
    print("not working")

print(os.name)
print(os.environ)
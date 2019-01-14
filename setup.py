import os
import configparser


def setuphandler(config_loc):
    """
    Controller to perform initial verification of a config file
    Input:
        config_loc - location of an ini file to be used for config
                        eg, config/test.ini
    Output:
        True/False - A bool value representing succesful completion
    """
    if filecheck(config_loc) == False:
        # If no file, build a skeleton to be modified before next run
        # Return false to end setup
        buildskel(config_loc)
        return False
    else:
        # File exists so check for valid config
        configvalidation(config_loc)
        return True

def fetchauth(config_loc, inheader):
    """
    Given a config file and specified header,
    """
    # Read config file
    config = configparser.ConfigParser()
    config.read(config_loc)

    # set up a config dictionary for output
    return config


def filecheck(config_loc):
    """
    Check for a valid config file at 
    
    """
    if os.path.isfile(config_loc):
        print("Config file found at: {}".format(config_loc))
        return True
    else:
        print("No config file found at: {}".format(config_loc))
        return False

def configvalidation(config_loc):
    # Read config and check for the correct headers
    config = configparser.ConfigParser()
    print("Reading config file")
    config.read(config_loc)

    if 'DEFAULT' and 'SLACK' and 'PTV' in config.sections():
        print('Valid Headers Found')



def buildskel(config_loc):
    """
    Build a skeleton config file with sections:
        DEFAULT, PTV, SLACK
    Input:
        config_loc - location of config file being built
    Output:
        
    """
    # Setup a new config instance
    print("building skeleton config file")
    config = configparser.ConfigParser()
    
    # Establish sections and default values
    config['DEFAULT'] = {
        'interval': 30
    }
    config['PTV'] = {
        'ptv_devid': '',
        'ptv_key': ''
    }
    config['SLACK'] = {
    }

    # Write to the output file
    with open(config_loc, 'w') as configfile:
        config.write(configfile)
    


if __name__ == "__main__":
    pass
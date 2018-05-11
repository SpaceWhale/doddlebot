"""
:author: john.sosoka
:date: 5/10/2018

"""

import logging

"""
GENERAL APP CONSTANTS
"""

CONFIG_NAME = "doddle.config"
BOT_NAME = "doddle"
ROOT_LOGGING_IDENTITY = "doddle"
ENVIRONMENT_VARIABLE_BOT_ID = "BOT_ID"
ENVIRONMENT_VARIABLE_BOT_TOKEN = "SLACK_BOT_TOKEN"

"""
LOGGING CONSTANTS
"""

LOG_NAME = "doddle.log"
LOG_CONFIG = "%s(asctime)s - %s(name)s - %s(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

SLACK_API_CLIENT_LOG_LEGEL = logging.DEBUG

"""
PLUGIN CONSTANTS
"""

RELATIVE_PLUGIN_DIRECTORY_PATH = "plugins/"

"""
MISC CONSTANTS
"""
SPLASH = """
   ___          __   ____      _______        __  ___       __ 
  / _ \___  ___/ /__/ / /__   / ___/ /  ___ _/ /_/ _ )___  / /_
 / // / _ \/ _  / _  / / -_) / /__/ _ \/ _ `/ __/ _  / _ \/ __/
/____/\___/\_,_/\_,_/_/\__/  \___/_//_/\_,_/\__/____/\___/\__/ 
                                                               
                                                           2018
                                                           
Author:
    * john.sosoka@protonmail.ch
    
==================================================================
==================================================================
"""

PYTHON_FILE = "*.py"
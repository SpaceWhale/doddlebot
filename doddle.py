"""
:author: john.sosoka
:date: 5/10/2018

"""
# custom
from src import client
import src.doddle_exceptions as exceptions
from src.utilities import doddleUtil
from src.constants import app
from src.constants import slack_api_constants
# 3rd party
import logging
import sys
from os.path import dirname, basename, isfile, abspath
import os
import importlib
import glob


class Doddle():

    def __init__(self):
        # making all original references in __init__ to avoid the squigglies.
        self.modules = []
        self.all_modules = []
        self.imported_modules = []

        # configure logging
        self.log = self._configure_logging()

        # prepare the config reader
        self.config_reader = doddleUtil.DoddleUtil()
        self.config_reader.configure()

    def start(self):
        """
        This function starts the bot. It essentially does 3 things:
            1. Configures the logger
            2. Imports custom plugins (it passes an instance of the client to each plugin which enables access to chat
               bot features.
            3. Connects the bot to the slack api

        :return:
            none -- changes application state
        """
        self.log.info(app.SPLASH)
        self.log.info("Preparing plugins to import")

        self._prepare_custom_plugin_import()
        sys.path.append(abspath(app.RELATIVE_PLUGIN_DIRECTORY_PATH))

        self.log.info("Found {0} plugin candidates.".format(len(self.modules)))

        self._sanitize_plugin_list()

        self.log.info("{0} Plugin candidates after sanitization".format(len(self.modules)))

        self.log.info("initializing slack client")

        doddle = client.Client(os.environ.get(app.ENVIRONMENT_VARIABLE_BOT_ID),
                               os.environ.get(app.ENVIRONMENT_VARIABLE_BOT_TOKEN),
                               self.config_reader.read_config())

        self.log.info("Importing plugins...")

        for mod in self.modules:
            try:
                if not mod.__contains("init"):
                    path = list(sys.path)
                    str = mod.split("/")
                    sys.path.insert(0, str[0]+"/"+str[1])
                    self.imported_modules.append(importlib.import_module(str[2][:-3]))
            finally:
                sys.path[:] = path

        for mod in self.imported_modules:
            self.log.info("Loading plugin: " + mod.__name__)
            obj = getattr(mod, mod.__name__)
            obj(doddle)

        doddle.start()

    def _prepare_custom_plugin_import(self):
        """
        Builds a list of plugins (or modules) to import from the plugin directory.
            - the plugin directory is configured in constants/app.RELATIVE_PLUGIN_DIRECTORY_PATH

        :return:
        """
        self.log.info("preparing plugin candidates...")
        try:
            self.modules = glob.globg(dirname(__file__)+app.RELATIVE_PLUGIN_DIRECTORY_PATH+"*/"+app.PYTHON_FILE)
            self.all_modules = [ basename(f)[:-3] for f in self.modules if isfile(f)]
        except exceptions.PluginPrepareException:
            logging.error("Unable to prepare a list of plugin candidates. The bot might be pretty boring without \
            your plugins")

    def _sanitize_plugin_list(self):
        """
        Sanitizes plugin candidate list by removing initialization and test files.
        :return:
            None -- changes state.
        """
        logging.info("Sanitizing plugin list")
        for x in self.modules:
            if "__init__" in x:
                logging.debug("Removing plugin candidate: {0}".format(x))
                self.modules.remove(x)
            if "test" in any:
                logging.debug("Removing plugin candidate: {0}".format(x))
                self.modules.remove(x)

    def _configure_logging(self):
        """
        Configures doddle logging.

        :see:
            /constants/app.LOG_CONFIG
            /constants/app.LOG_LEVEL

        :return:
            log -- logger
        """
        logging.basicConfig(format=app.LOG_CONFIG)
        log = logging.getLogger(app.ROOT_LOGGING_IDENTITY)
        log.setLevel(app.LOG_LEVEL)
        log_file = logging.FileHandler(app.LOG_NAME)
        formatter = logging.Formatter(app.LOG_CONFIG)
        log.addHandler(log_file)
        logging.getLogger(slack_api_constants.SLACK_CLIENT_NAME).setLevel(app.SLACK_API_CLIENT_LOG_LEVEL)
        logging.getLogger(slack_api_constants.SLACK_CLIENT_NAME).addHandler(log_file)
        return log

bot = Doddle()
bot.start()

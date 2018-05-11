"""
:author: john.sosoka
:date: 5/10/2018

"""

import os
import logging
import ConfigParser

log = logging.getLogger("doddle.util.doddleUtil")


class DoddleUtil(object):
    """
    The doddleUtil currently only handles loading & reading the configuration file for the bot

    Init:
        :Args:
            None
    """

    def __init__(self):
        self.config_path = os.path.abspath('data/' + app.CONFIG_NAME)

        log.info("Using config " + self.config_path)

    def configure(self):
        """
        Configures the doddleUtil class
        :returns:
            None
        """
        self.bot_config = ConfigParser.ConfigParser()
        self.bot_config.read(self.config_path)

    def read_config(self, section):
        """
        Reads the configuration file
        :param section:
            str -- a string which corresponds to a relevant section in the doddle config file.
        :return:
            dict -- returns a dictionary with the key specified and values from the doddle config file.
        """

        section_dict = {}

        try:
            options = self.appConfig.options(section)
        except IOError:
            log.error("encountered an error reading config, %s" % IOError.message)

        for option in options:
            try:
                section_dict[option] = self.appConfig.get(section, option)
                if section_dict[option] == -1:
                    log.debug("skipping option: %s" % option)
            except:
                log.error("error reading option %s" % option)

        return section_dict

    def get_option(self, section, option, default=None):
        """
        :param section:
            str -- pointing to the relevant section of the config
        :param option:
            str -- pointing to the relevant subsection of the config
        :param default:

        :return:
            returns the resulting object from the config (string, dictionary, list, etc)

        :example:

        >>>
        """

        try:
            value = self.bot_config.get(section, option)

        except ConfigParser.NoOptionError:
            log.error("Encountered no option error %s" % ConfigParser.NoOptionError.message)
            log.info("No option provided, adding the default to the config, write and return default")
            if default:
                self.bot_config.set(section, option, default)
                self.bot_config.write(open(self.configfile, "w"))
            value = default

        return value

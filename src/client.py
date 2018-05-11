"""
:author: john.sosoka
:date: 5/10/2018

"""

# custom
from utilities import doddleUtil
from utilities import commandParser
from constants import slack_api_constants
from constants import app
import doddle_exceptions
# 3rd party
import logging
import time
import json
from slackclient import SlackClient

log = logging.getLogger("doddle.src.Client")


class Client:

    def __init__(self, bot_id, token, actionCharacter, websocket_delay=1):
        """

        :param bot_id:
            str -- the bot_id
        :param token:
            str -- the slack doken
        :param actionCharacter:
            str -- this is the character the bot listens to to process a command, if it is the first character
                   (i.e, !help) the bot will process this message with ! being the actionCharacter
        :param websocket_delay:
            int -- sets how frequently (in seconds) that the bot queries the rtm api
        :return:
            nothing
        """
        # mandatory slackclient data
        self.bot_id = bot_id
        self.token = token
        self.slack_client = SlackClient
        # handle commands based on action character
        self.actionChar = actionCharacter
        # Handle @mentions if wanted
        self.at_bot = "<@{0}>".format(self.bot_id)
        # configure behavior
        self.websocket_delay = websocket_delay
        self.registered_plugins = []
        self.commands = {}
        self.channelDirectory = {}
        self.commandParser = commandParser.util()
        # prepare the config reader
        self.config_reader = doddleUtil.DoddleUtil()
        self.config_reader.configure()
        # maintain state
        self.connected_status = False

    def start(self):
        self.slack_client = SlackClient(self.token)

        if self.slack_client.rtm_connect():
            log.info("Connected to slack.")
            self._set_channel_directory()
            self.connected_status = True
            while True:
                command, channel = self._parse_slack_output(self.slack_client.rtm_read())
                if command and channel:
                    self._handle_command(command, channel)
                time.sleep(self.websocket_delay)
            log.error(app.BOT_NAME + "has disconnected...Attempting to reconnect")
        else:
            self.connected_status = False
            log.error(app.BOT_NAME + "has disconnected...Attempting to reconnect")
            self.start()

    def get_channel_directory(self):
        """
        :return:
            dict - a directory of channels.
            Key = human readable name, Value = slack channel id.
        """
        return self.channelDirectory

    def reply_to_channel(self, channel, text, attatchments=None):
        """
        :param channel:
        :param attatchments:
        :return:
        """
        attatchment = None
        if attatchments:
            attatchment = json.dumps(attatchments)

        self.slack_client.api_call(slack_api_constants.CALL_CHAT_POST_MESSAGE,
                                   channel=channel,
                                   text=text,
                                   as_user=True,
                                   attatchments=attatchment)

    def reply_to_thread(self):
        """
        TODO

        :return:
        """

    def reply_to_direct_message(self):
        """
        TODO

        :return:
        """

    def register_command(self, name, about):
        """
        Registers a command provided by a plugin by adding the instructions to the "help" reply.

        :param name:
        :param about:
        :return:

        :example:

        self.bot.register_command("restart <machine>", "restarts the target machine")
        """

        self.commands[name] = self.actionChar + about

    def register_plugin(self, plugin):
        """
        Registers a new plugin by adding it into a list of plugins. Each plugin is required to have an on_command
        function to process the command parts/channel that get broadcast to it.

        :param plugin:
        :return:
        """
        self.registered_plugins.append(plugin)

    def get_option(self, section, option, default=None):
        """
        Returns the value of the result for the section/option keys provided

        :param section:
        :param option:
        :param default:
        :return:
        """
        try:
            return self.config_reader.read_config(section, option, default)
        except doddle_exceptions.CommandParseException:
            log.error("Unable to read configuration {0} {1}".format(section,
                                                                    option))

    def parse_command(self, options, parts):
        """
        Parses the command

        see:
        utilities/commandParser

        :param options:
            dict -- a dictionary with possible options/values
        :param parts:
            list -- a space delimited list of words from the original command
        :return:
            dict -- returns a dictionary of parsed commands.
        """
        return self.commandParser.parse_command(options, parts)

    def _set_channel_directory(self):
        """
        This method builds a directory of available slack channels.

        :return:
            Nothing

        :example:

        """
        log.info("Building channel direcotry.")
        channels = self.slack_client.api_call(slack_api_constants.CALL_CHANNELS_LIST)
        try:
            for channel in channels[slack_api_constants.CHANNELS]:
                self.channelDirectory[channel['name']] = channel["id"]
            log.info("Channel directory built. {0} channels.".format(len(self.channelDirectory)))
        except doddle_exceptions.DirectoryCreateException:
            log.error("Unable to create channel directory.")

    def _parse_slack_output(self, rtm_output):
        """
        This function parses all messages retrieved from the slack api. It returns a list of space delimited
        commands if the any of the following criteria are satisfied.

        - If the output starts with the action character
        - If the output contains an @mention directed at the bot
        - If a help command is issued

        :param rtm_output:
            list -- the output of a message from the slack api

        :return:
            list -- returns a list of space delimited words from the rtm_output
        """
        output_list = rtm_output

        if output_list and len(output_list) > 0:

            for output in output_list:
                try:
                    if output and "text" in output and self.actionChar in output['text'][0]:
                        if "help" in output["text"].split(self.actionChar)[1].strip():
                            self.help(output["user"])

                    if output and "text" in output and self.actionChar in output["text"][0]:
                        return output["text"].split(self.actionChar)[1].strip(), output["channel"]

                    elif output and "text" in output and self.at_bot in output["text"]:
                        return output["text"].split(self.at_bot)[1].strip(), output["channel"]
                except doddle_exceptions.CommandParseException:
                    log.error("Unable to parse rtm_output")
        return None, None

    def _handle_command(self, command, channel):
        """
        This function splits the string of text that the bot has decided to process into a space-delimited
        list of words and then broadcasts the command and channel to all registered plugins.

        See Also:
        utilities/commandParser

        :param command:
            string -- the string of text following the actionChar.
        :param channel:
            string -- the channel id that the command was sent from.
        :return:
        """
        log.debug("Handling command: {0} in channel: {1}".format(command,
                                                                 channel))

        parts = command.split()
        for plugin in self.registered_plugins:
            plugin.on_command(channel, parts)




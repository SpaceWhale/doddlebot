"""
:author: john.sosoka
:date: 5/10/2018

"""

class commandParser:


    def __init__(self):
        """
        The commandParser parses incoming slack messages and returns processed commands which
        are then sent to all registered plugins.

        Init:
            :Args:
                None
        """

    def parse_command(self, option, parts):
        """
        :param option:
            dict -- the plugin supplied dictionary containing valid options & values
        :param parts:
            list -- each space delimited word from the initial command split into a list
        :return:
            dict -- returns a dictionary with matched options & values

        :example:

        options = {'command': ['start',
                               'stop',
                               'restart'],
                   'target': ['machine1',
                              'machine2']

        parts = ['start', 'machine1', 'meaninglessInput']

        print(parse_command(options, parts))

        >> {'wildcard1': 'meaninglessInput', 'command': 'start', 'target': 'machine1'}
        """

        parsed_commands = {}
        tmp_dict = {}
        tmp_known_values = []
        tmp_known_keys = []

        # Integer i keeps track of parsed wildcard options
        i = 0

        for command, options in option.items():
            parsed_commands.update({command: ''.join(set(option).intersection(parts))})
        tmp_dict.update({'wildcard': list(set(parsed_commands).symmetric_difference(parts))})

        for key, value in parsed_commands.items():
            tmp_known_values.append(value)
            tmp_known_keys.append(key)

        tmp_wild = set(parsed_commands).symmetric_difference(parts)

        tmp_list = [x for x in tmp_wild if x not in tmp_known_values]
        final_tmp_list = [x for x in tmp_list if x not in tmp_known_keys]

        for item in final_tmp_list:
            parsed_commands.update({'wildcard%d' % i: item})

        return parsed_commands

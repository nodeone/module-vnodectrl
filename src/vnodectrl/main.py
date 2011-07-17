"""
Main file that can be executed directly.
"""
import os
import sys
import vnodectrl.plugins
from vnodectrl import utils
from optparse import OptionParser
from vnodectrl.plugins import *

def main(args):
    commands = {}
    # Locate the configuration.
    configuration = utils.get_main_config()
    if configuration == False:
        print "No configuration available. Make sure everything is installed properly"
        return 1

    # Locate deployment instructions.
    configuration["deployment"] = utils.get_deployment_config()

    # Get all commands.
    commands = utils.get_commands()

    parser = OptionParser()
    (options, args) = parser.parse_args()

    if len(args) > 0:
        primary_command = args[0];
        command_info = commands.get(primary_command, None);
        if command_info != None:
            plugin_class = getattr(command_info['module'], command_info['plugin'])
            plugin = plugin_class(configuration)
            plugin.execute(primary_command, args, options)
        else:
            print "Unrecognized command"

    else:
        print "Available Commands:\n"
        for command, options in commands.iteritems():
            print "{0}\t{1}".format(command, options['description']);

sys.exit(main(sys.argv))

import vnodectrl.base
from vnodectrl.base import VnodectrlPlugin

COMMANDS = {
	"list-drivers" : {
		"description": "List Drivers",
		"plugin": "ConfigPlugin",
		"name": "list-drivers",
		"requirements": vnodectrl.base.libcloud_requirements
	}
}
	
class ConfigPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;

	def execute(self, cmd, args, options):
		for driver in self.config['drivers'].keys():
			print driver

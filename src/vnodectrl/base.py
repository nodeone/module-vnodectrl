import sys; sys.path.append('..')
import utils
try:
	from libcloud.compute.types import Provider
	from libcloud.compute.providers import get_driver
except ImportError:
	'''
	'''

class VnodectrlOptions:
	def options(self):
		"""
		Declare all options here.
		"""

class VnodectrlPlugin:
	def commands(self):
		"""
		Declare all commands here.
		"""
	def help(self, cmd):
		"""
		Specify help for a specific command here.
		"""

	def execute(self, cmd):
		"""
		Act on a particular command here
		"""
	def connect(self, driver, user_id = "NaN", key = "NaN"):
		"""
		Connect with a particular driver using a userid
		and a key.
		"""
		try:
			driver_class = get_provider(driver)
			# Temporary to get support
			if driver == "virtualbox":
				conn = driver_class()
			else:
				conn = driver_class(str(user_id), str(key))
			return conn
		except NameError, e:
			print ">> Fatal Error: %s" % e
			return False
		except Exception, e:
			print ">> Fatal error: %s" % e
			return False
	
	def getSize(self, driver, conn, size = False):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		sizes = conn.list_sizes()
		
		# If size is false, let's not care about what size we use.
		if size is False:
			return sizes[0]
		
		size = str(size)
		for available_size in sizes:
			if available_size.id == size:
				return available_size
		return False
		
	def getImage(self, driver, conn, image):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		
		# Virtualbox drivers dont really know about the different images,
		# Instead they force you to add the drivers in list_images.
		# Dirrrty hack harr.
		if str(driver) == 'virtualbox':
			images = conn.list_images([image])
			return images[0]
		
		images = conn.list_images()
		for available_image in images:
			if available_image.id == image:
				return available_image
		return False
	
	def getNode(self, driver, conn, node):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		nodes = conn.list_nodes()
		for available_node in nodes:
			if available_node.name == node:
				return available_node
		return False		

class VnodectrlException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def libcloud_requirements():
	'''
	This function can be used to determine if libcloud exists.
	It also loads all required modules that might not be present
	in the system.
	It returns True if the requirements are met and false otherwise.
	'''
	try:
		from libcloud.compute.types import Provider
		from libcloud.compute.providers import get_driver
		return True
	except ImportError:
		return False
	
def get_provider(driver):
	'''
	Get a provider based on the string in the config.
	'''
	drivers = {
		"ec2-europe": Provider.EC2_EU_WEST,
		"virtualbox": "virtualbox"
		# Just fill out the rest of the gang later on.
	}
	# Try to import the virtualbox driver. Some clients might not have
	# virtualbox installed, so if they don't, just remove the driver.
	try:
		import virtualbox
	except ImportError:
		del drivers['virtualbox']

	if driver in drivers:
		real_driver = drivers[driver]
		# The Virtualbox driver is not really included in liblcoud,
		# so we add it ourselves here.
		if driver == "virtualbox":
			return virtualbox.VirtualBoxNodeDriver	
		
		return get_driver(real_driver)
	
	return False
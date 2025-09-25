#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import argparse
import logging
import traceback
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

logging.basicConfig(format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s', level = logging.DEBUG)

class ConstrainedDeviceApp():
	"""
	Definition of the ConstrainedDeviceApp class.
	
	"""
	
	def __init__(self):
		"""
		Initialization of class.
		
		@param path The name of the resource to apply to the URI.
		"""
		logging.info("Initializing CDA...")
		
		# Create DeviceDataManager instance (replaces direct SystemPerformanceManager usage)
		self.devDataMgr = DeviceDataManager()
		self.isStarted = False
		
		logging.info("CDA initialization complete.")

	def isAppStarted(self) -> bool:
		"""
		Check if the application has been started.
		
		@return bool True if started, False otherwise
		"""
		return self.isStarted

	def startApp(self):
		"""
		Start the CDA. Calls startManager() on the device data manager instance.
		
		"""
		logging.info("Starting CDA...")
		
		if self.devDataMgr:
			self.devDataMgr.startManager()
			self.isStarted = True
		
		logging.info("CDA started.")

	def stopApp(self, code: int):
		"""
		Stop the CDA. Calls stopManager() on the device data manager instance.
		
		@param code The exit code to use when stopping
		"""
		logging.info("CDA stopping...")
		
		if self.devDataMgr:
			self.devDataMgr.stopManager()
			self.isStarted = False
		
		logging.info("CDA stopped with exit code %s.", str(code))
		
def main():
	"""
	Main function definition for running client as application.
	
	Current implementation runs for 65 seconds then exits, or runs forever based on configuration.
	"""
	argParser = argparse.ArgumentParser( \
		description = 'CDA used for generating telemetry - Programming the IoT.')
	
	argParser.add_argument('-c', '--configFile', help = 'Optional custom configuration file for the CDA.')
	configFile = None
	
	try:
		args = argParser.parse_args()
		configFile = args.configFile
		logging.info('Parsed configuration file arg: %s', configFile)
	except:
		logging.info('No arguments to parse.')
	
	# Initialize ConfigUtil
	configUtil = ConfigUtil(configFile)
	cda = None
	
	try:
		# Initialize CDA
		cda = ConstrainedDeviceApp()
		
		# Start CDA
		cda.startApp()
		
		# Check if CDA should run forever
		runForever = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)
		
		if runForever:
			logging.info("CDA configured to run forever. Use Ctrl+C to exit.")
			# Sleep ~5 seconds every loop
			while (True):
				sleep(5)
		else:
			# Run CDA for ~65 seconds then exit
			logging.info("CDA configured to run for 65 seconds.")
			if (cda.isAppStarted()):
				sleep(65)
				cda.stopApp(0)
			
	except KeyboardInterrupt:
		logging.warning('Keyboard interruption for CDA. Exiting.')
		if (cda):
			cda.stopApp(-1)
	except Exception as e:
		# Handle any uncaught exception that may be thrown
		# during CDA initialization
		logging.error('Startup exception caused CDA to fail. Exiting.')
		traceback.print_exception(type(e), e, e.__traceback__)
		if (cda):
			cda.stopApp(-2)
	
	# Exit cleanly
	logging.info('Exiting CDA.')
	exit()

if __name__ == '__main__':
	"""
	Attribute definition for when invoking as app via command line
	
	"""
	main()
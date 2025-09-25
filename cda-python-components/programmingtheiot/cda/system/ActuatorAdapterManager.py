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

import logging
from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		"""
		Constructor for ActuatorAdapterManager.
		
		@param dataMsgListener Optional data message listener for processing actuator responses
		"""
		# Initialize data message listener
		self.dataMsgListener = dataMsgListener
		
		# Initialize configuration utility
		self.configUtil = ConfigUtil()
		
		# Get configuration properties
		self.useSimulator = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.ENABLE_SIMULATOR_KEY)
		
		self.useEmulator = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.locationID = self.configUtil.getProperty(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.DEVICE_LOCATION_ID_KEY, 
			defaultVal=ConfigConst.NOT_SET)
		
		# Initialize actuator task references
		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None
		
		# Initialize actuator tasks based on configuration
		if self.useEmulator:
			logging.info("ActuatorAdapterManager will use emulators.")
			# Emulator functionality will be added in Lab Module 4
			self._initActuatorEmulationTasks()
		else:
			logging.info("ActuatorAdapterManager will use simulators.")
			self._initEnvironmentalActuationTasks()
	
	def _initEnvironmentalActuationTasks(self):
		"""
		Initialize environmental actuator simulation tasks.
		"""
		# Create simulator tasks for environmental control
		self.humidifierActuator = HumidifierActuatorSimTask()
		self.hvacActuator = HvacActuatorSimTask()
		
		logging.info("Environmental actuator simulation tasks initialized.")
	
	def _initActuatorEmulationTasks(self):
		"""
		Initialize actuator emulation tasks (placeholder for Lab Module 4).
		"""
		# Placeholder - will be implemented in Lab Module 4
		logging.info("Actuator emulation tasks initialization - placeholder for Lab Module 4")
		# For now, fall back to simulation tasks
		self._initEnvironmentalActuationTasks()
	
	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		"""
		Send an actuator command to the appropriate actuator task.
		
		@param data The ActuatorData command to process
		@return ActuatorData The response from the actuator, or None if invalid/failed
		"""
		# Validate input data and check if it's not a response
		if data and not data.isResponseFlagEnabled():
			# First check if the actuation event is destined for this device
			if data.getLocationID() == self.locationID:
				logging.info("Actuator command received for location ID %s. Processing...", 
					str(data.getLocationID()))
				
				aType = data.getTypeID()
				responseData = None
				
				# Route command to appropriate actuator based on type ID
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
					responseData = self.hvacActuator.updateActuator(data)
				elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
					responseData = self.ledDisplayActuator.updateActuator(data)
				else:
					logging.warning("No valid actuator type. Ignoring actuation for type: %s", 
						data.getTypeID())
				
				# In a later lab module, the responseData instance will be
				# passed to a callback function implemented in DeviceDataManager
				# via IDataMessageListener
				return responseData
			else:
				logging.warning("Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s", 
					str(self.locationID), str(data.getLocationID()))
		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")
		
		return None
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		"""
		Set the data message listener for processing actuator responses.
		
		@param listener The IDataMessageListener implementation
		@return bool True if listener was set successfully, False otherwise
		"""
		if listener:
			self.dataMsgListener = listener
			return True
		
		return False
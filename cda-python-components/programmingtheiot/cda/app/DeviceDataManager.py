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

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self):
		"""
		Constructor for DeviceDataManager.
		
		Initializes all managers and configuration settings.
		"""
		# Initialize configuration
		self.configUtil = ConfigUtil()
		
		# Load configuration properties
		self.enableSystemPerf = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_SYSTEM_PERF_KEY)
		
		self.enableSensing = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_SENSING_KEY)
		
		self.handleTempChangeOnDevice = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
		
		self.triggerHvacTempFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY,
			defaultVal=18.0)
		
		self.triggerHvacTempCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY,
			defaultVal=20.0)
		
		# Initialize managers based on configuration
		if self.enableSystemPerf:
			self.sysPerfMgr = SystemPerformanceManager()
			self.sysPerfMgr.setDataMessageListener(self)
			logging.info("Local system performance tracking enabled")
		else:
			self.sysPerfMgr = None
			
		if self.enableSensing:
			self.sensorAdapterMgr = SensorAdapterManager()
			self.sensorAdapterMgr.setDataMessageListener(self)
			logging.info("Local sensor tracking enabled")
		else:
			self.sensorAdapterMgr = None
		
		# Initialize actuator adapter manager
		self.actuatorAdapterMgr = ActuatorAdapterManager()
		self.actuatorAdapterMgr.setDataMessageListener(self)
		logging.info("Local actuation capabilities enabled")
		
		# Initialize communication connectors (placeholders for future use)
		self.mqttClient = None
		self.coapClient = None
		
		# Initialize data caches
		self.latestSensorDataCache = {}
		self.latestActuatorDataCache = {}
		self.latestSystemPerfDataCache = {}
		
		# Initialize listeners
		self.sysPerfDataListener = None
		self.telemetryDataListener = None
		
		logging.info("DeviceDataManager initialization complete.")
		
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		
		@param name The actuator name to retrieve
		@return ActuatorData The cached actuator response data, or None if not found
		"""
		if name and name in self.latestActuatorDataCache:
			return self.latestActuatorDataCache[name]
		
		return None
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		
		@param name The sensor name to retrieve
		@return SensorData The cached sensor data, or None if not found
		"""
		if name and name in self.latestSensorDataCache:
			return self.latestSensorDataCache[name]
		
		return None
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		
		@param name The system performance data name to retrieve  
		@return SystemPerformanceData The cached system performance data, or None if not found
		"""
		if name and name in self.latestSystemPerfDataCache:
			return self.latestSystemPerfDataCache[name]
		
		return None
	
	def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
		"""
		This callback method will be invoked by the connection that's handling
		an incoming ActuatorData command message.
		
		@param data The incoming ActuatorData command message
		@return ActuatorData The response from processing the command
		"""
		logging.info("Actuator data: " + str(data))
		
		if data:
			logging.info("Processing actuator command message.")
			return self.actuatorAdapterMgr.sendActuatorCommand(data)
		else:
			logging.warning("Incoming actuator command is invalid (null). Ignoring.")
			return None
	
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		"""
		This callback method will be invoked by the actuator manager that just
		processed an ActuatorData command, which creates a new ActuatorData
		instance and sets it as a response before calling this method.
		
		@param data The incoming ActuatorData response message
		@return bool True if processed successfully, False otherwise
		"""
		if data:
			logging.debug("Incoming actuator response received (from actuator manager): " + str(data))
			
			# Cache the response data
			if data.getName():
				self.latestActuatorDataCache[data.getName()] = data
			
			# TODO: In later lab modules, will handle upstream transmission
			return True
		else:
			logging.warning("Incoming actuator response is invalid (null). Ignoring.")
			return False
	
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		This callback method is generic and designed to handle any incoming string-based
		message, which will likely be JSON-formatted and need to be converted to the appropriate
		data type. You may not need to use this callback at all.
		
		@param resourceEnum The resource enumeration for the message
		@param msg The incoming JSON message
		@return bool True if processed successfully, False otherwise
		"""
		logging.debug("Incoming message received. Resource: %s, Message: %s", 
			str(resourceEnum), msg)
		
		if msg:
			self._handleIncomingDataAnalysis(msg)
			return True
		
		return False
	
	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		This callback method will be invoked by the sensor manager that just processed
		a new sensor reading, which creates a new SensorData instance that will be
		passed to this method.
		
		@param data The incoming SensorData message
		@return bool True if processed successfully, False otherwise
		"""
		if data:
			logging.debug("Incoming sensor data received (from sensor manager): " + str(data))
			
			# Cache the sensor data
			if data.getName():
				self.latestSensorDataCache[data.getName()] = data
			
			# Analyze sensor data for potential actuator triggers
			self._handleSensorDataAnalysis(data)
			
			# TODO: In later lab modules, will handle upstream transmission
			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			return False
	
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		"""
		This callback method will be invoked by the system performance manager that just
		processed a new sensor reading, which creates a new SystemPerformanceData instance
		that will be passed to this method.
		
		@param data The incoming SystemPerformanceData message
		@return bool True if processed successfully, False otherwise
		"""
		if data:
			logging.debug("Incoming system performance message received (from sys perf manager): " + str(data))
			
			# Cache the system performance data
			if data.getName():
				self.latestSystemPerfDataCache[data.getName()] = data
			
			# TODO: In later lab modules, will handle upstream transmission
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
			return False
	
	def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
		"""
		Set the system performance data listener.
		
		@param listener The system performance data listener
		"""
		if listener:
			self.sysPerfDataListener = listener
			
	def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
		"""
		Set the telemetry data listener.
		
		@param name The listener name
		@param listener The telemetry data listener
		"""
		if listener:
			self.telemetryDataListener = listener
			
	def startManager(self):
		"""
		Start the DeviceDataManager and all associated managers.
		"""
		logging.info("Starting DeviceDataManager...")
		
		# Start system performance manager
		if self.sysPerfMgr:
			self.sysPerfMgr.startManager()
		
		# Start sensor adapter manager
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.startManager()
		
		# TODO: In later lab modules, will start communication connectors
		
		logging.info("Started DeviceDataManager.")
		
	def stopManager(self):
		"""
		Stop the DeviceDataManager and all associated managers.
		"""
		logging.info("Stopping DeviceDataManager...")
		
		# Stop system performance manager
		if self.sysPerfMgr:
			self.sysPerfMgr.stopManager()
		
		# Stop sensor adapter manager  
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.stopManager()
		
		# TODO: In later lab modules, will stop communication connectors
		
		logging.info("Stopped DeviceDataManager.")
		
	def _handleIncomingDataAnalysis(self, msg: str):
		"""
		Call this from handleIncomingMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
		2) Convert msg: Use DataUtil to convert if appropriate.
		3) Act on msg: Determine what - if any - action is required, and execute.
		
		@param msg The incoming message to analyze
		"""
		logging.debug("Analyzing incoming data analysis message: %s", msg)
		
		# TODO: In Lab Module 5, will implement JSON to object conversion
		# For now, just log the message
		logging.info("Incoming data analysis message received. Processing not yet implemented.")
		
	def _handleSensorDataAnalysis(self, data: SensorData):
		"""
		Call this from handleSensorMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Check config: Is there a rule or flag that requires immediate processing of data?
		2) Act on data: If #1 is true, determine what - if any - action is required, and execute.
		
		@param data The sensor data to analyze
		"""
		if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
			logging.info("Handle temp change: %s - type ID: %s",
				str(self.handleTempChangeOnDevice), str(data.getTypeID()))
			
			# Create actuator data for HVAC control
			ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
			ad.setLocationID(data.getLocationID())
			
			# Determine action based on temperature thresholds
			if data.getValue() > self.triggerHvacTempCeiling:
				# Temperature too high - turn on cooling
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempCeiling)
				logging.info("Temperature above ceiling threshold. Triggering HVAC cooling.")
			elif data.getValue() < self.triggerHvacTempFloor:
				# Temperature too low - turn on heating
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempFloor)
				logging.info("Temperature below floor threshold. Triggering HVAC heating.")
			else:
				# Temperature in acceptable range - turn off HVAC
				ad.setCommand(ConfigConst.COMMAND_OFF)
				ad.setValue(0.0)
				logging.info("Temperature within acceptable range. Turning off HVAC.")
			
			# Send actuator command
			self.handleActuatorCommandMessage(ad)
		
	def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handleSensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If #1 is true, send message upstream using one (or both) client connections.
		
		@param resourceName The resource name for the message
		@param msg The message to transmit upstream
		"""
		logging.info("Upstream transmission invoked. Checking comm's integration.")
		
		# TODO: In Lab Module 6 (MQTT) and Lab Module 8 (CoAP), will implement actual transmission
		# For now, just log the intent to transmit
		
		if self.mqttClient:
			logging.debug("Would publish to MQTT broker. Resource: %s, Message length: %d", 
				str(resourceName), len(msg) if msg else 0)
		elif self.coapClient:
			logging.debug("Would send via CoAP. Resource: %s, Message length: %d", 
				str(resourceName), len(msg) if msg else 0)
		else:
			logging.debug("No upstream communication configured. Message not transmitted.")
			logging.debug("Resource: %s, Message: %s", str(resourceName), msg)
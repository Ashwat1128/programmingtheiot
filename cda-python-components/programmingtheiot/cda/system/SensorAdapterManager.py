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

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		"""
		Constructor for SensorAdapterManager.
		
		@param dataMsgListener Optional data message listener for processing sensor data
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
		
		# Get polling rate for scheduler
		self.pollRate = self.configUtil.getInteger(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.POLL_CYCLES_KEY, 
			defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)
		
		# Initialize scheduler
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(
			func=self.handleTelemetry,
			trigger='interval',
			seconds=self.pollRate,
			max_instances=2,
			coalesce=True,
			misfire_grace_time=15)
		
		# Initialize sensor adapters
		if self.useEmulator:
			logging.info("SensorAdapterManager will use emulators.")
			# Emulator functionality will be added in Lab Module 4
			self._initSensorEmulationTasks()
		else:
			logging.info("SensorAdapterManager will use simulators.")
			self._initSensorSimulationTasks()
	
	def _initSensorSimulationTasks(self):
		"""
		Initialize sensor simulation tasks with data generators.
		"""
		# Get floor and ceiling values from configuration
		humidityFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.HUMIDITY_SIM_FLOOR_KEY, 
			defaultVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
		
		humidityCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.HUMIDITY_SIM_CEILING_KEY, 
			defaultVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
		
		pressureFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.PRESSURE_SIM_FLOOR_KEY, 
			defaultVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		
		pressureCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.PRESSURE_SIM_CEILING_KEY, 
			defaultVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
		
		tempFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.TEMP_SIM_FLOOR_KEY, 
			defaultVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
		
		tempCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE, 
			key=ConfigConst.TEMP_SIM_CEILING_KEY, 
			defaultVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		
		# Generate data sets
		self.dataGenerator = SensorDataGenerator()
		
		humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(
			minValue=humidityFloor, 
			maxValue=humidityCeiling, 
			useSeconds=False)
		
		pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(
			minValue=pressureFloor, 
			maxValue=pressureCeiling, 
			useSeconds=False)
		
		tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(
			minValue=tempFloor, 
			maxValue=tempCeiling, 
			useSeconds=False)
		
		# Create sensor simulation tasks with generated data sets
		self.humidityAdapter = HumiditySensorSimTask(dataSet=humidityData)
		self.pressureAdapter = PressureSensorSimTask(dataSet=pressureData)
		self.tempAdapter = TemperatureSensorSimTask(dataSet=tempData)
	
	def _initSensorEmulationTasks(self):
		"""
		Initialize sensor emulation tasks (placeholder for Lab Module 4).
		"""
		# Placeholder - will be implemented in Lab Module 4
		logging.info("Sensor emulation tasks initialization - placeholder for Lab Module 4")
		# For now, fall back to simulation tasks
		self._initSensorSimulationTasks()
	
	def handleTelemetry(self):
		"""
		Handle telemetry collection from all sensor adapters.
		
		This method is called by the scheduler at regular intervals.
		"""
		# Generate telemetry from each sensor adapter
		humidityData = self.humidityAdapter.generateTelemetry()
		pressureData = self.pressureAdapter.generateTelemetry()
		tempData = self.tempAdapter.generateTelemetry()
		
		# Set location ID for each sensor data instance
		humidityData.setLocationID(self.locationID)
		pressureData.setLocationID(self.locationID)
		tempData.setLocationID(self.locationID)
		
		# Log generated data for debugging
		logging.debug('Generated humidity data: %s', str(humidityData.getValue()))
		logging.debug('Generated pressure data: %s', str(pressureData.getValue()))
		logging.debug('Generated temp data: %s', str(tempData.getValue()))
		
		# Send data to message listener if available
		if self.dataMsgListener:
			self.dataMsgListener.handleSensorMessage(humidityData)
			self.dataMsgListener.handleSensorMessage(pressureData)
			self.dataMsgListener.handleSensorMessage(tempData)
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		"""
		Set the data message listener for processing sensor data.
		
		@param listener The IDataMessageListener implementation
		@return bool True if listener was set successfully, False otherwise
		"""
		if listener:
			self.dataMsgListener = listener
			return True
		
		return False
	
	def startManager(self) -> bool:
		"""
		Start the sensor adapter manager and its scheduler.
		
		@return bool True if started successfully, False if already running
		"""
		logging.info("Starting SensorAdapterManager.")
		
		if not self.scheduler.running:
			self.scheduler.start()
			logging.info("Started SensorAdapterManager.")
			return True
		else:
			logging.info("SensorAdapterManager scheduler already started. Ignoring.")
			return False
		
	def stopManager(self) -> bool:
		"""
		Stop the sensor adapter manager and its scheduler.
		
		@return bool True if stopped successfully, False if already stopped
		"""
		try:
			self.scheduler.shutdown()
			logging.info("Stopped SensorAdapterManager.")
			return True
		except:
			logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
			return False
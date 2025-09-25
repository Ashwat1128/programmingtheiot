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
import random

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

class BaseSensorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_MIN_VAL = 0.0
	DEFAULT_MAX_VAL = 1000.0
	
	def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, dataSet: SensorDataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
		"""
		Constructor for BaseSensorSimTask.
		
		@param name The sensor name
		@param typeID The sensor type ID
		@param dataSet Optional pre-defined data set for simulation
		@param minVal Minimum value for random generation
		@param maxVal Maximum value for random generation
		"""
		# Store constructor parameters as instance variables
		self.dataSet = dataSet
		self.name = name
		self.typeID = typeID
		self.dataSetIndex = 0
		self.useRandomizer = False
		self.latestSensorData = None
		
		# Determine if we should use randomizer or dataset
		if not self.dataSet:
			self.useRandomizer = True
			
		# Set min/max values for random generation
		self.minVal = minVal
		self.maxVal = maxVal
		
		# Initialize logging
		logging.basicConfig(level=logging.INFO)
		logging.info("Created BaseSensorSimTask instance: name=%s, typeID=%d, useRandomizer=%s", 
			self.name, self.typeID, self.useRandomizer)
	
	def generateTelemetry(self) -> SensorData:
		"""
		Implement basic logging and SensorData creation. Sensor-specific functionality
		should be implemented by sub-class.
		
		A local reference to SensorData can be contained in this base class.
		
		@return SensorData The generated sensor data
		"""
		# Create new SensorData instance
		sensorData = SensorData(typeID=self.getTypeID(), name=self.getName())
		sensorVal = ConfigConst.DEFAULT_VAL
		
		if self.useRandomizer:
			# Generate random value between min and max
			sensorVal = random.uniform(self.minVal, self.maxVal)
			logging.debug("Generated random sensor value: %f for %s", sensorVal, self.name)
		else:
			# Get next value from dataset
			sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
			
			# Advance index and wrap around if necessary
			self.dataSetIndex = self.dataSetIndex + 1
			if self.dataSetIndex >= self.dataSet.getDataEntryCount():
				self.dataSetIndex = 0
				
			logging.debug("Retrieved dataset sensor value: %f for %s at index %d", 
				sensorVal, self.name, self.dataSetIndex - 1)
		
		# Set the value in SensorData
		sensorData.setValue(sensorVal)
		
		# Store as latest sensor data
		self.latestSensorData = sensorData
		
		logging.info("Generated telemetry for %s: value=%f", self.name, sensorVal)
		
		return self.latestSensorData
	
	def getTelemetryValue(self) -> float:
		"""
		If a local reference to SensorData is not None, simply return its current value.
		If SensorData hasn't yet been created, call self.generateTelemetry(), then return
		its current value.
		
		@return float The current sensor value
		"""
		if not self.latestSensorData:
			# Generate new telemetry if none exists
			self.generateTelemetry()
			
		return self.latestSensorData.getValue()
	
	def getLatestTelemetry(self) -> SensorData:
		"""
		This can return the current SensorData instance or a copy.
		
		@return SensorData The latest sensor data instance
		"""
		if not self.latestSensorData:
			# Generate new telemetry if none exists
			self.generateTelemetry()
			
		return self.latestSensorData
	
	def getName(self) -> str:
		"""
		Returns the sensor name.
		
		@return str The sensor name
		"""
		return self.name
	
	def getTypeID(self) -> int:
		"""
		Returns the sensor type ID.
		
		@return int The sensor type ID
		"""
		return self.typeID
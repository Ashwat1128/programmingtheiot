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
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(SensorData, self).__init__(name = name, typeID = typeID, d = d)
		# Initialize the sensor value with default
		self.value = ConfigConst.DEFAULT_VAL
		# Initialize sensor type for backward compatibility
		self.sensorType = typeID
	
	def getSensorType(self) -> int:
		"""
		Returns the sensor type to the caller.
		
		@return int
		"""
		return self.sensorType
	
	def getValue(self) -> float:
		"""
		Returns the current sensor value.
		
		@return float The current sensor value
		"""
		return self.value
	
	def setValue(self, newVal: float):
		"""
		Sets the sensor value and updates the timestamp.
		
		@param newVal The new sensor value to set
		"""
		if newVal is not None:
			self.value = newVal
			# Update timestamp when value changes
			self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
		Internal method to update this instance with data from another SensorData instance.
		
		@param data The SensorData instance to copy data from
		"""
		if data and isinstance(data, SensorData):
			self.setValue(data.getValue())
			# Update sensor type if provided
			if hasattr(data, 'sensorType'):
				self.sensorType = data.sensorType
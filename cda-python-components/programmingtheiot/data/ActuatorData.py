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

class ActuatorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		# Initialize actuator-specific properties
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = ""
		self.isResponse = False
	
	def getCommand(self) -> int:
		"""
		Returns the actuator command.
		
		@return int The command value
		"""
		return self.command
	
	def getStateData(self) -> str:
		"""
		Returns the state data string.
		
		@return str The state data
		"""
		return self.stateData
	
	def getValue(self) -> float:
		"""
		Returns the actuator value.
		
		@return float The actuator value
		"""
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		"""
		Returns whether this actuator data represents a response.
		
		@return bool True if this is a response, False otherwise
		"""
		return self.isResponse
	
	def setCommand(self, command: int):
		"""
		Sets the actuator command and updates timestamp.
		
		@param command The command value to set
		"""
		if command is not None:
			self.command = command
			# Optionally update timestamp for command changes
			self.updateTimeStamp()
	
	def setAsResponse(self):
		"""
		Marks this ActuatorData as a response.
		"""
		self.isResponse = True
		self.updateTimeStamp()
		
	def setStateData(self, stateData: str):
		"""
		Sets the state data string.
		
		@param stateData The state data string to set
		"""
		if stateData is not None:
			self.stateData = stateData
			self.updateTimeStamp()
	
	def setValue(self, val: float):
		"""
		Sets the actuator value and updates timestamp.
		
		@param val The value to set
		"""
		if val is not None:
			self.value = val
			self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
		Internal method to update this instance with data from another ActuatorData instance.
		
		@param data The ActuatorData instance to copy data from
		"""
		if data and isinstance(data, ActuatorData):
			self.setValue(data.getValue())
			self.setCommand(data.getCommand())
			self.setStateData(data.getStateData())
			if data.isResponseFlagEnabled():
				self.setAsResponse()
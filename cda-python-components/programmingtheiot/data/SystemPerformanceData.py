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

class SystemPerformanceData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0
	
	def __init__(self, d = None):
		super(SystemPerformanceData, self).__init__(name = ConfigConst.SYSTEM_PERF_MSG, typeID = ConfigConst.SYSTEM_PERF_TYPE, d = d)
		# Initialize system performance metrics
		self.cpuUtil = ConfigConst.DEFAULT_VAL
		self.diskUtil = ConfigConst.DEFAULT_VAL
		self.memUtil = ConfigConst.DEFAULT_VAL
	
	def getCpuUtilization(self):
		"""
		Returns the CPU utilization percentage.
		
		@return float CPU utilization as a percentage
		"""
		return self.cpuUtil
	
	def getDiskUtilization(self):
		"""
		Returns the disk utilization percentage.
		
		@return float Disk utilization as a percentage
		"""
		return self.diskUtil
	
	def getMemoryUtilization(self):
		"""
		Returns the memory utilization percentage.
		
		@return float Memory utilization as a percentage
		"""
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		"""
		Sets the CPU utilization and updates timestamp.
		
		@param cpuUtil CPU utilization percentage (0.0 - 100.0)
		"""
		if cpuUtil is not None:
			# Optional: Add validation to ensure value is within valid range
			if 0.0 <= cpuUtil <= 100.0:
				self.cpuUtil = cpuUtil
				self.updateTimeStamp()
			else:
				# Handle invalid range - you can log warning or set to boundary values
				self.cpuUtil = max(0.0, min(100.0, cpuUtil))
				self.updateTimeStamp()
	
	def setDiskUtilization(self, diskUtil):
		"""
		Sets the disk utilization and updates timestamp.
		
		@param diskUtil Disk utilization percentage (0.0 - 100.0)
		"""
		if diskUtil is not None:
			# Optional: Add validation to ensure value is within valid range
			if 0.0 <= diskUtil <= 100.0:
				self.diskUtil = diskUtil
				self.updateTimeStamp()
			else:
				# Handle invalid range
				self.diskUtil = max(0.0, min(100.0, diskUtil))
				self.updateTimeStamp()
	
	def setMemoryUtilization(self, memUtil):
		"""
		Sets the memory utilization and updates timestamp.
		
		@param memUtil Memory utilization percentage (0.0 - 100.0)
		"""
		if memUtil is not None:
			# Optional: Add validation to ensure value is within valid range
			if 0.0 <= memUtil <= 100.0:
				self.memUtil = memUtil
				self.updateTimeStamp()
			else:
				# Handle invalid range
				self.memUtil = max(0.0, min(100.0, memUtil))
				self.updateTimeStamp()
	
	def _handleUpdateData(self, data):
		"""
		Internal method to update this instance with data from another SystemPerformanceData instance.
		
		@param data The SystemPerformanceData instance to copy data from
		"""
		if data and isinstance(data, SystemPerformanceData):
			self.setCpuUtilization(data.getCpuUtilization())
			self.setDiskUtilization(data.getDiskUtilization())
			self.setMemoryUtilization(data.getMemoryUtilization())
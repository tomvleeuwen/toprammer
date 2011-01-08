"""
#    TOP2049 Open Source programming suite
#
#    Generic SRAM chip
#
#    Copyright (c) 2011 Michael Buesch <mb@bu3sch.de>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from chip import *


class Chip_genericSRAM(Chip):
	def __init__(self, chipPackage, chipPinVCCX, chipPinGND,
		     VCCXVoltage,
		     nrAddressBits, nrDataBits):
		Chip.__init__(self,
			      chipPackage = chipPackage,
			      chipPinVCCX = chipPinVCCX,
			      chipPinGND = chipPinGND)
		self.VCCXVoltage = VCCXVoltage
		self.nrAddressBits = nrAddressBits
		self.nrAddressBytes = int(math.ceil((float(self.nrAddressBits) - 0.1) / 8))
		self.nrDataBits = nrDataBits
		assert(nrDataBits == 8)

	def shutdownChip(self):
		self.printDebug("Shutdown chip")
		self.top.cmdSetVCCXVoltage(self.VCCXVoltage)
		self.applyVCCX(False)
		self.applyVPP(False)
		self.applyGND(False)

	def erase(self):
		self.writeRAM(chr(0) * self.__sizeBytes())

	def __readBuffer(self, size):
		if not size:
			return ""
		data = self.top.cmdReadBufferReg()
		return data[0:size]

	def readRAM(self):
		image = []

		self.progressMeterInit("Reading SRAM", self.__sizeBytes())
		self.__turnOnChip()
		self.__setControlPins(CE=0, OE=0, WE=1)
		nrBytes = 0
		for addr in range(0, self.__sizeBytes()):
			self.progressMeter(addr)
			self.__setAddress(addr)
			self.__readData()
			nrBytes += 1
			if nrBytes == 64:
				image.append(self.__readBuffer(nrBytes))
				nrBytes = 0
		image.append(self.__readBuffer(nrBytes))
		self.__setControlPins(CE=1, OE=1, WE=1)
		self.progressMeterFinish()

		return "".join(image)

	def writeRAM(self, image):
		if len(image) > self.__sizeBytes():
			self.throwError("Invalid memory image size %d (expected max %d)" %\
				(len(image), self.__sizeBytes()))

		self.progressMeterInit("Writing SRAM", self.__sizeBytes())
		self.__turnOnChip()
		self.__setControlPins(CE=0, OE=1, WE=1)
		for addr in range(0, len(image)):
			self.progressMeter(addr)
			self.__setAddress(addr)
			self.__writeData(image[addr])
			self.__setControlPins(CE=0, OE=1, WE=0)
			self.top.cmdDelay(0.00000007) # Delay at least 70 nsec
			self.__setControlPins(CE=0, OE=1, WE=1)
		self.__setControlPins(CE=1, OE=1, WE=1)
		self.progressMeterFinish()

	def __sizeBytes(self):
		return (1 << self.nrAddressBits)

	def __turnOnChip(self):
		self.__setControlPins(CE=1, OE=1, WE=1)
		self.top.cmdSetVCCXVoltage(self.VCCXVoltage)
		self.applyGND(True)
		self.applyVCCX(True)
		self.lastAddress = None

	def __setControlPins(self, CE=1, OE=1, WE=1):
		value = 0
		if CE:
			value |= 1
		if OE:
			value |= 2
		if WE:
			value |= 4
		self.top.cmdFPGAWrite(0x11, value)

	def __writeData(self, data):
		data = ord(data)
		self.top.cmdFPGAWrite(0x10, data)

	def __readData(self):
		self.top.cmdFPGARead(0x10)

	def __setAddress(self, addr):
		for i in range(0, self.nrAddressBytes):
			shift = 8 * i
			mask = 0xFF << shift
			if self.lastAddress is None or\
			   (self.lastAddress & mask) != (addr & mask):
				self.top.cmdFPGAWrite(0x12 + i,
						      (addr & mask) >> shift)
		self.lastAddress = addr
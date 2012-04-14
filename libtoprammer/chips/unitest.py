"""
#    TOP2049 Open Source programming suite
#
#    Universal device tester
#
#    Copyright (c) 2010 Michael Buesch <m@bues.ch>
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

from libtoprammer.chip import *


class Chip_Unitest(Chip):
	def __init__(self, chipPackage=None, chipPinVCC=None, chipPinsVPP=None, chipPinGND=None,
			   VCCVoltage=None, VPPVoltage=None):
		Chip.__init__(self, chipPackage=chipPackage, chipPinVCC=chipPinVCC,
			      chipPinsVPP=chipPinsVPP, chipPinGND=chipPinGND)
		self.autogenVCCVoltage = VCCVoltage
		self.autogenVPPVoltage = VPPVoltage

	def shutdownChip(self):
		self.printDebug("Shutdown chip")
		self.reset()

	def reset(self):
		self.top.vcc.setLayoutPins( [] )
		self.vccMask = 0
		self.top.vpp.setLayoutPins( [] )
		self.vppMask = 0
		self.top.gnd.setLayoutPins( [] )
		self.gndMask = 0
		self.top.cmdSetVCCVoltage(self.top.vcc.minVoltage())
		self.top.cmdSetVPPVoltage(self.top.vpp.minVoltage())
		self.oscMask = 0
		self.setOutputEnableMask(0)
		self.setOutputs(0)
		self.setOscMask(0)
		self.top.flushCommands()

	def setVCC(self, voltage, layout):
		self.vccMask = self.top.vcc.ID2mask(layout)
		self.__updateOutEn()
		self.top.cmdSetVCCVoltage(voltage)
		self.top.vcc.setLayoutID(layout)
		self.top.flushCommands()

	def setVPP(self, voltage, layouts):
		self.vppMask = 0
		for layout in layouts:
			self.vppMask |= self.top.vpp.ID2mask(layout)
		self.__updateOutEn()
		self.top.cmdSetVPPVoltage(voltage)
		self.top.vpp.setLayoutMask(0) # Reset
		for layout in layouts:
			self.top.vpp.setLayoutID(layout)
		self.top.flushCommands()

	def setGND(self, layout):
		self.gndMask = self.top.gnd.ID2mask(layout)
		self.__updateOutEn()
		self.top.gnd.setLayoutID(layout)
		self.top.flushCommands()

	# Overloaded layout generator interface.
	def applyVCC(self, turnOn):
		layoutID = 0
		if turnOn:
			(layoutID, layoutMask) = self.generator.getVCCLayout()
		self.setVCC(self.autogenVCCVoltage, layoutID)

	# Overloaded layout generator interface.
	def applyVPP(self, turnOn, packagePinsToTurnOn=[]):
		assert(not packagePinsToTurnOn) # Not supported, yet.
		layouts = []
		if turnOn:
			layouts = map(lambda (layoutID, layoutMask): layoutID,
				      self.generator.getVPPLayouts())
		self.setVPP(self.autogenVPPVoltage, layouts)

	# Overloaded layout generator interface.
	def applyGND(self, turnOn):
		layoutID = 0
		if turnOn:
			(layoutID, layoutMask) = self.generator.getGNDLayout()
		self.setGND(layoutID)

	def __updateOutEn(self):
		mask = self.desiredOutEnMask
		mask &= ~self.gndMask
		mask &= ~self.vccMask
		mask &= ~self.vppMask
		mask |= self.oscMask
		self.top.cmdFPGAWrite(0x50, mask & 0xFF)
		self.top.cmdFPGAWrite(0x51, (mask >> 8) & 0xFF)
		self.top.cmdFPGAWrite(0x52, (mask >> 16) & 0xFF)
		self.top.cmdFPGAWrite(0x53, (mask >> 24) & 0xFF)
		self.top.cmdFPGAWrite(0x54, (mask >> 32) & 0xFF)
		self.top.cmdFPGAWrite(0x55, (mask >> 40) & 0xFF)
		self.top.flushCommands()

	def setOutputEnableMask(self, mask):
		self.desiredOutEnMask = mask
		self.__updateOutEn()

	def __updateOut(self):
		mask = self.desiredOutMask
		mask &= ~self.oscMask
		self.top.cmdFPGAWrite(0x70, mask & 0xFF)
		self.top.cmdFPGAWrite(0x71, (mask >> 8) & 0xFF)
		self.top.cmdFPGAWrite(0x72, (mask >> 16) & 0xFF)
		self.top.cmdFPGAWrite(0x73, (mask >> 24) & 0xFF)
		self.top.cmdFPGAWrite(0x74, (mask >> 32) & 0xFF)
		self.top.cmdFPGAWrite(0x75, (mask >> 40) & 0xFF)
		self.top.flushCommands()

	def setOutputs(self, mask):
		self.desiredOutMask = mask
		self.__updateOut()

	def getInputs(self):
		self.top.cmdFPGARead(0x30)
		self.top.cmdFPGARead(0x31)
		self.top.cmdFPGARead(0x32)
		self.top.cmdFPGARead(0x33)
		self.top.cmdFPGARead(0x34)
		self.top.cmdFPGARead(0x35)
		inputs = self.top.cmdReadBufferReg48()
		return inputs

	def getOscFreq(self):
		return self.top.getOscillatorHz()

	def setOscDivider(self, div):
		self.top.cmdFPGAWrite(0x12, div & 0xFF)
		self.top.cmdFPGAWrite(0x13, (div >> 8) & 0xFF)
		self.top.cmdFPGAWrite(0x14, (div >> 16) & 0xFF)
		self.top.cmdFPGAWrite(0x15, (div >> 24) & 0xFF)
		self.top.flushCommands()

	def setOscMask(self, mask):
		self.oscMask = mask
		self.top.cmdFPGAWrite(0x30, mask & 0xFF)
		self.top.cmdFPGAWrite(0x31, (mask >> 8) & 0xFF)
		self.top.cmdFPGAWrite(0x32, (mask >> 16) & 0xFF)
		self.top.cmdFPGAWrite(0x33, (mask >> 24) & 0xFF)
		self.top.cmdFPGAWrite(0x34, (mask >> 32) & 0xFF)
		self.top.cmdFPGAWrite(0x35, (mask >> 40) & 0xFF)
		self.__updateOutEn()
		self.__updateOut()
		self.top.flushCommands()

ChipDescription(
	Chip_Unitest,
	bitfile = "unitest",
	runtimeID = (0x0008, 0x01),
	chipType = ChipDescription.TYPE_INTERNAL,
	description = "Universal device tester",
)
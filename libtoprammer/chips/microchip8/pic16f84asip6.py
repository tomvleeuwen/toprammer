"""
#    TOP2049 Open Source programming suite
#
#   Microchip PIC16F84 SIP6
#
#    Copyright (c) 2013 Pavel Stemberk <stemberk@gmail.com>
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

from microchip8_splittedPMarea import *

class Chip_Pic16F84asip6(microchip8_splittedPMarea):
	CMD_BEGIN_ERASE_PROGRAMMING_CYCLE = 0x8
	CMD_BEGIN_PROGRAMMING_ONLY_CYCLE = 0x18
	
	voltageVDD = 5
	voltageVPP = 13
	
	delayTinternalProgPM = 0.004

	userIDLocationSize = 4
	hasEEPROM = True

	def __init__(self):
	 	microchip8_splittedPMarea.__init__(self,
		chipPackage = "DIP10",
		chipPinVCC = 9,
		chipPinsVPP = 10,
		chipPinGND = 8,
		signature="\x60\x05",
		flashPageSize=0x200,
		flashPages=1,
		eepromPageSize=64,
		eepromPages=1,
		fuseBytes=2
		)
		
	def sendWriteFlashInstr(self):
		'''
		'''
		self.sendCommand(0, 0, 0, self.CMD_BEGIN_PROGRAMMING_ONLY_CYCLE)
		self.top.cmdDelay(self.delayTinternalProgDM)
		
	def sendWriteFlashInstrDM(self):
		self.sendWriteFlashInstr()
	
	def bulkErasePGM(self):	
		self.sendCommand(0, 0, 0, self.CMD_BULK_ERASE_PGM)
		self.sendCommand(0, 0, 0, self.CMD_BEGIN_PROGRAMMING_ONLY_CYCLE)
		self.top.cmdDelay(self.delayTera)  # Tera
		
	def bulkEraseDM(self):
		self.sendCommand(0, 0, 0, self.CMD_BULK_ERASE_DM)
		self.sendCommand(0, 0, 0, self.CMD_BEGIN_PROGRAMMING_ONLY_CYCLE)
		self.top.cmdDelay(self.delayTera)  # Tera		
fuseDesc = (
	BitDescription(0, "FOSC[0], 00=LP osc, 01=XT osc"),
	BitDescription(1, "FOSC[1], 10=HS osc, 11=RC osc"),
	BitDescription(2, "WDTEN, 1=WDT enabled"),
	BitDescription(3, "nPWRT"),
	BitDescription(4, "nCP"),
	BitDescription(5, "nCP"),
	BitDescription(6, "nCP"),
	BitDescription(7, "nCP"),
	BitDescription(8, "nCP"),
	BitDescription(9, "nCP"),
	BitDescription(10, "nCP"),
	BitDescription(11, "nCP"),
	BitDescription(12, "nCP"),
	BitDescription(13, "nCP"),
)

ChipDescription(
	Chip_Pic16F84asip6,
	bitfile = "microchip01sip6",
	chipID="pic16f84asip6",
	runtimeID = (0xDE05, 0x01),
	chipVendors="Microchip",
	description = "PIC16F84A, PIC16LF84A - ICD",
	packages = (("DIP10", ""), ),
	fuseDesc=fuseDesc, 	
	maintainer="Pavel Stemberk <stemberk@gmail.com>",
)

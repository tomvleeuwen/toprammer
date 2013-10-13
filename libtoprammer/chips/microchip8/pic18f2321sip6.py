"""
#    TOP2049 Open Source programming suite
#
#   Microchip PIC18F2320 DIP18
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

from microchip8_18f2221family import *

class Chip_PIC18F2321sip6(microchip8_18f2221family):

	hasEEPROM = True

     	writeBufferSize			 = 8
     	eraseBufferSize			 = 64
     	
     	def __init__(self):
     		microchip8_18f2221family.__init__(self,
			chipPackage = "DIP10",
			chipPinVCC = 9,
			chipPinsVPP = 10,
			chipPinGND = 8,
			signature="\x22\x21",
			flashPageSize=0x2000,
			flashPages=1,
			eepromPageSize=0x100,
			eepromPages=1,
			fuseBytes=14
			)
			

fuseDesc = (
	BitDescription(0o00, "NA"),
	BitDescription(0o01, "NA"),
	BitDescription(0o02, "NA"),
	BitDescription(0o03, "NA"),
	BitDescription(0o04, "NA"),
	BitDescription(0o05, "NA"),
	BitDescription(0o06, "NA"),
	BitDescription(0o07, "NA"),
	BitDescription(0o10, "FOSC[0], 0000=LP, 1000=internal RC oscillator, RA6=CLKO"),
	BitDescription(0o11, "FOSC[1]"),
	BitDescription(0o12, "FOSC[2]"),
	BitDescription(0o13, "FOSC[3]"),
	BitDescription(0o14, "NA"),
	BitDescription(0o15, "NA"),
	BitDescription(0o16, "FCMEN, 0=Fail-Safe Clock Monitor is disabled"),
	BitDescription(0o17, "IESO, 0=Internal/External Switchover mode is disabled"),
    
	BitDescription(0o20, "nPWRTEN"),
	BitDescription(0o21, "BOREN[0]"),
	BitDescription(0o22, "BOREN[1]"),
	BitDescription(0o23, "BORV[0]"),
	BitDescription(0o24, "BORV[1]"),
	BitDescription(0o25, "NA"),
	BitDescription(0o26, "NA"),
	BitDescription(0o27, "NA"),
	BitDescription(0o30, "WDTEN, 0=WDT disabled, 1=WDT enabled"),
	BitDescription(0o31, "WDTPS[0]"),
	BitDescription(0o32, "WDTPS[1]"),
	BitDescription(0o33, "WDTPS[2]"),
	BitDescription(0o34, "WDTPS[3]"),
	BitDescription(0o35, "NA"),
	BitDescription(0o36, "NA"),
	BitDescription(0o37, "NA"),
	
	BitDescription(0o40, "NA"),
	BitDescription(0o41, "NA"),
	BitDescription(0o42, "NA"),
	BitDescription(0o43, "NA"),
	BitDescription(0o44, "NA"),
	BitDescription(0o45, "NA"),
	BitDescription(0o46, "NA"),
	BitDescription(0o47, "NA"),
	BitDescription(0o50, "NA"),
	BitDescription(0o51, "PBADEN"),
	BitDescription(0o52, "LPT1OSC"),
	BitDescription(0o53, "NA"),
	BitDescription(0o54, "NA"),
	BitDescription(0o55, "NA"),
	BitDescription(0o56, "NA"),
	BitDescription(0o57, "MCLRE"), 	
    
	BitDescription(0o60, "STVREN"),
	BitDescription(0o61, "NA"),
	BitDescription(0o62, "LVP"),
	BitDescription(0o63, "NA"),
	BitDescription(0o64, "BBSIZ[0]"),
	BitDescription(0o65, "BBSIZ[1]"),
	BitDescription(0o66, "XINST"),
	BitDescription(0o67, "nDEBUG"),
	BitDescription(0o70, "NA"),
	BitDescription(0o71, "NA"),
	BitDescription(0o72, "NA"),
	BitDescription(0o73, "NA"),
	BitDescription(0o74, "NA"),
	BitDescription(0o75, "NA"),
	BitDescription(0o76, "NA"),
	BitDescription(0o77, "NA"),
	
	BitDescription(0o100, "CP[0]"),
	BitDescription(0o101, "CP[1]"),
	BitDescription(0o102, "CP[2]/NA"),
	BitDescription(0o103, "CP[3]/NA"),
	BitDescription(0o104, "CP[4]/NA"),
	BitDescription(0o105, "CP[5]/NA"),
	BitDescription(0o106, "NA"),
	BitDescription(0o107, "NA"),
	BitDescription(0o110, "NA"),
	BitDescription(0o111, "NA"),
	BitDescription(0o112, "NA"),
	BitDescription(0o113, "NA"),
	BitDescription(0o114, "NA"),
	BitDescription(0o115, "NA"),
	BitDescription(0o116, "CPB"),
	BitDescription(0o117, "CPD"), 	
	
	BitDescription(0o120, "WRT[0]"),
	BitDescription(0o121, "WRT[1]"),
	BitDescription(0o122, "WRT[2]/NA"),
	BitDescription(0o123, "WRT[3]/NA"),
	BitDescription(0o124, "WRT[4]/NA"),
	BitDescription(0o125, "WRT[5]/NA"),
	BitDescription(0o126, "NA"),
	BitDescription(0o127, "NA"),
	BitDescription(0o130, "NA"),
	BitDescription(0o131, "NA"),
	BitDescription(0o132, "NA"),
	BitDescription(0o133, "NA"),
	BitDescription(0o134, "NA"),
	BitDescription(0o135, "WRTC"),
	BitDescription(0o136, "WRTB"),
	BitDescription(0o137, "WRTD"),
	
	BitDescription(0o140, "EBTR[0]"),
	BitDescription(0o141, "EBTR[1]"),
	BitDescription(0o142, "EBTR[2]/NA"),
	BitDescription(0o143, "EBTR[3]/NA"),
	BitDescription(0o144, "EBTR[4]/NA"),
	BitDescription(0o145, "EBTR[5]/NA"),
	BitDescription(0o146, "NA"),
	BitDescription(0o147, "NA"),
	BitDescription(0o150, "NA"),
	BitDescription(0o151, "NA"),
	BitDescription(0o152, "NA"),
	BitDescription(0o153, "NA"),
	BitDescription(0o154, "NA"),
	BitDescription(0o155, "NA"),
	BitDescription(0o156, "EBTRB"),
	BitDescription(0o157, "NA"),
)

ChipDescription(
	Chip_PIC18F2321sip6,
	bitfile = "microchip01sip6",
	chipID="PIC18F2321sip6",
	runtimeID = (0xDE05, 0x01),
	chipVendors="Microchip",
	description = "PIC18F2321 - ICD",
	packages = (("DIP10", ""), ),
	fuseDesc=fuseDesc, 	
	maintainer="Pavel Stemberk <stemberk@gmail.com>",
)

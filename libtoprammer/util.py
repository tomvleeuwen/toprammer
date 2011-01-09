"""
#    TOP2049 Open Source programming suite
#
#    Utility functions
#
#    Copyright (c) 2009-2010 Michael Buesch <mb@bu3sch.de>
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

import sys
import re
import math


class TOPException(Exception): pass

def nrBitsSet(integer):
	count = 0
	while integer:
		count += (integer & 1)
		integer >>= 1
	return count

def roundup(x, y):
	x = int(x)
	y = int(y)
	return ((x + (y - 1)) // y) * y

hexdump_re = re.compile(r"0x[0-9a-fA-F]+:\s+([0-9a-fA-F\s]+)\s*.*")

def parseHexdump(dump):
	try:
		bin = []
		for line in dump.splitlines():
			line = line.strip()
			if not line:
				continue
			m = hexdump_re.match(line)
			if not m:
				raise TOPException("Invalid hexdump format (regex failure)")
			bytes = m.group(1).replace(" ", "")
			if len(bytes) % 2 != 0:
				raise TOPException("Invalid hexdump format (odd bytestring len)")
			for i in range(0, len(bytes), 2):
				byte = int(bytes[i:i+2], 16)
				bin.append(chr(byte))
		return "".join(bin)
	except (ValueError), e:
		raise TOPException("Invalid hexdump format (Integer error)")

def generateHexdump(mem):
	def toAscii(char):
		if char >= 32 and char <= 126:
			return chr(char)
		return "."

	ret = ""
	ascii = ""
	for i in range(0, len(mem)):
		if i % 16 == 0 and i != 0:
			ret += "  " + ascii + "\n"
			ascii = ""
		if i % 16 == 0:
			ret += "0x%04X:  " % i
		c = ord(mem[i])
		ret += "%02X" % c
		if (i % 2 != 0):
			ret += " "
		ascii += toAscii(c)
	ret += "  " + ascii + "\n\n"
	return ret

def dumpMem(mem):
	sys.stdout.write(generateHexdump(mem))

class IO_ihex:
	TYPE_DATA = 0
	TYPE_EOF  = 1
	TYPE_ESAR = 2
	TYPE_SSAR = 3
	TYPE_ELAR = 4
	TYPE_SLAR = 5

	def autodetect(self, data):
		try:
			self.toBinary(data)
		except (TOPException), e:
			return False
		return True

	def toBinary(self, ihexData):
		bin = []
		checksumWarned = False
		doublewriteWarned = False
		try:
			lines = ihexData.splitlines()
			hiAddr = 0
			for line in lines:
				line = line.strip()
				if len(line) == 0:
					continue
				if len(line) < 11 or (len(line) - 1) % 2 != 0:
					raise TOPException("Invalid IHEX format (length error)")
				if line[0] != ':':
					raise TOPException("Invalid IHEX format (magic error)")
				count = int(line[1:3], 16)
				if len(line) != count * 2 + 11:
					raise TOPException("Invalid IHEX format (count error)")
				addr = (int(line[3:5], 16) << 8) | int(line[5:7], 16)
				addr |= hiAddr << 16
				type = int(line[7:9], 16)
				checksum = 0
				for i in range(1, len(line), 2):
					byte = int(line[i:i+2], 16)
					checksum = (checksum + byte) & 0xFF
				checksum = checksum & 0xFF
				if checksum != 0 and not checksumWarned:
					checksumWarned = True
					print "WARNING: Invalid IHEX format (checksum error)"

				if type == self.TYPE_EOF:
					break
				if type == self.TYPE_ELAR:
					if count != 2:
						raise TOPException("Invalid IHEX format (inval ELAR)")
					hiAddr = (int(line[9:11], 16) << 8) | int(line[11:13], 16)
					continue
				if type == self.TYPE_DATA:
					if len(bin) < addr + count: # Reallocate
						bin += ['\xFF'] * (addr + count - len(bin))
					for i in range(9, 9 + count * 2, 2):
						byte = chr(int(line[i:i+2], 16))
						if bin[(i - 9) / 2 + addr] != '\xFF' and \
						   not doublewriteWarned:
							doublewriteWarned = True
							print "Invalid IHEX format (Wrote twice to same location)"
						bin[(i - 9) / 2 + addr] = byte
					continue
				raise TOPException("Invalid IHEX format (unsup type %d)" % type)
		except ValueError:
			raise TOPException("Invalid IHEX format (digit format)")
		return "".join(bin)

	def fromBinary(self, binData):
		ihex = []
		addr = 0
		for i in range(0, len(binData), 16):
			if addr > 0xFFFF:
				checksum = 0
				ihex.append(":%02X%04X%02X" % (2, 0, self.TYPE_ELAR))
				checksum += 2 + 0 + 0 + self.TYPE_ELAR
				a = (addr >> 16) & 0xFFFF
				ihex.append("%04X" % a)
				checksum += ((a >> 8) & 0xFF) + (a & 0xFF)
				checksum = ((checksum ^ 0xFF) + 1) & 0xFF
				ihex.append("%02X\n" % checksum)
				addr -= 0xFFFF
			checksum = 0
			size = min(len(binData) - i, 16)
			ihex.append(":%02X%04X%02X" % (size, addr, self.TYPE_DATA))
			checksum += size + ((addr >> 8) & 0xFF) + (addr & 0xFF) + self.TYPE_DATA
			for j in range(0, size):
				data = ord(binData[i + j])
				checksum = (checksum + data) & 0xFF
				ihex.append("%02X" % data)
			checksum = ((checksum ^ 0xFF) + 1) & 0xFF
			ihex.append("%02X\n" % checksum)
			addr += size
		ihex.append(":00000001FF\n")
		return "".join(ihex)

class IO_hex:
	def autodetect(self, data):
		try:
			self.toBinary(data)
		except (TOPException), e:
			return False
		return True

	def toBinary(self, data):
		return parseHexdump(data)

	def fromBinary(self, data):
		return generateHexdump(data)

class IO_binary:
	def autodetect(self, data):
		return True

	def toBinary(self, data):
		return data

	def fromBinary(self, data):
		return data

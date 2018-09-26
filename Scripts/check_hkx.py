#! python3

import sys
import re
import os.path
import sizes
import util
import shutil

import subprocess

Unknown = 0
PC_32 = 1
PC_64 = 2
NX_64 = 3

def CheckHKX_Internal(filename):
	util.LogDebug("CheckHKX : " + filename)
	
	with open(filename, "rb") as file:
		file.seek(16, 0)
		bitsFlag = file.read(1)
		file.seek(18, 0)
		nxFlag = file.read(1)
		util.LogDebug("BF {} NF {}".format(bitsFlag, nxFlag))
		if bitsFlag == b'\x04':
			if nxFlag == b'\x00':
				return PC_32
		elif bitsFlag == b'\x08':
			if nxFlag == b'\x00':
				return PC_64
			elif nxFlag == b'\x01':
				return NX_64
	return Unknown

def CheckHKX(target, filename):
	return CheckHKX_Internal(filename)
	
if __name__ == '__main__':
	filename = sys.argv[1]
	CheckHKX_Internal(filename)
#! python3

import sys
import os.path
import shutil
import subprocess
import util
import job_manager
import convert_dds
import convert_hkx
import convert_txt
import convert_sound


import bitflag

def ConvertPath(mod_name, target):

	script_path = util.GetScriptPath()
	
	util.LogInfo("Convert Path")
	util.LogDebug("This is the target: " + target)
	util.LogDebug("This is the mod name " + mod_name)
	
	has_havoc = util.HasHavokBPP()
	
	ConvertListDDS = []
	ConvertListHKX = []
	ConvertListTXT = []
	ConvertListSound = []
	for root, subdirs, files in os.walk(target):
		if root != target:
			util.LogDebug("Walking folder " + root)
			for filename in files:
				#util.LogDebug("filename: {}".format(filename))
				if filename.lower().endswith(".dds"):
					file_path = os.path.join(root, filename)
					ConvertListDDS.append(file_path)
				elif filename.lower().endswith(".hkx"):
					file_path = os.path.join(root, filename)
					ConvertListHKX.append(file_path)
				elif filename.lower().startswith("translate_") and filename.lower().endswith(".txt"):
					file_path = os.path.join(root, filename)
					ConvertListTXT.append(file_path)
				elif filename.lower().endswith(".xwm") or filename.lower().endswith(".fuz") or filename.lower().endswith(".wav"):
					file_path = os.path.join(root, filename)
					ConvertListSound.append(file_path)
					
	util.LogInfo("Found {} dds files to convert".format(len(ConvertListDDS)))
	if has_havoc: util.LogInfo("Found {} hkx files to convert".format(len(ConvertListHKX)))
	util.LogInfo("Found {} txt files to convert".format(len(ConvertListTXT)))
	util.LogInfo("Found {} sound files to convert".format(len(ConvertListSound)))
	'''
	def LogProgress(convertList, convertFn, name):
		if len(convertList) > 0:
			failedCount = 0
			for i in range(len(convertList)):
				file_path = convertList[i]
				success = convertFn(target, file_path)
				if not success:
					failedCount += 1
				sys.stdout.write("Converted {}/{} {} ({}) failed. \r".format(i+1, len(convertList), name, failedCount))
				sys.stdout.flush()
			sys.stdout.write("\n")
	'''
	
	def LogProgress(convertList, convertFn, name):
		if len(convertList) > 0:
			failedCount = 0
			jm = job_manager.JobManager()
			convertedCount = 0
			processedCount = 0
			totalCount = len(convertList)
			def cb(success):
				nonlocal processedCount, convertedCount, failedCount
				processedCount += 1
				if success:
					convertedCount += 1
				else:
					failedCount += 1
				sys.stdout.write("{} Processed {}/{} ({}/{}) success/failure. \r".format(name, processedCount, totalCount, convertedCount, failedCount))
				sys.stdout.flush()
				
			for i in range(len(convertList)):
				file_path = convertList[i]
				job = job_manager.Job(cb, convertFn, target, file_path)
				jm.AddJob(job)
			jm.ProcessBatch()
			
			sys.stdout.write("\n")
	
	LogProgress(ConvertListDDS, convert_dds.ConvertDDS, "DDS")
	if has_havoc:
		LogProgress(ConvertListHKX, convert_hkx.ConvertHKX, "HKX")
	LogProgress(ConvertListTXT, convert_txt.ConvertTXT, "TXT")
	LogProgress(ConvertListSound, convert_sound.ConvertSound, "Sounds")

def ConvertPath_External(mod_name, target):
	util.InitialiseLog(target + ".log")
	util.StartTimer()
	util.LogInfo("TOOLKIT call convert_path")
	ConvertPath(mod_name, target)
	util.EndTimer()
	
if __name__ == '__main__':
	mod_name = sys.argv[1]
	target = sys.argv[2]
	util.InitialiseLog(target + ".log")
	util.StartTimer()
	ConvertPath(mod_name, target)
	util.EndTimer()
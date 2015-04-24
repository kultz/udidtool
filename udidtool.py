#!/usr/bin/env python
'''\nProvisioning Parser Script
Usage: python script.py -i <Profile>
Arguments:
 -i, --file       provisioning profile
Flags:
 -h      help
''' 
import plistlib
import sys, getopt
import os
def usage():
    print sys.exit(__doc__)
def main(argv):
	if len(sys.argv) == 1:
		usage()
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["file=","profile="])
	except getopt.GetoptError:
		print 'Usage: '+sys.argv[0]+' -i <Profile>'
		sys.exit(1)
	for opt, arg in opts:
		if opt == '-h':
			print sys.argv[0]+' -i <Profile>'
			sys.exit(1)
		elif opt in ("-i", "--file"):
			inputfile = arg

	PHEAD = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
	PEND = '</plist>'

	with open(inputfile,'rb') as thefile:
		data = thefile.read()

	start_point = data.find(PHEAD)
	end_point = data.find(PEND)
	if end_point < 0:
		print "Could not recognize the profile try another one!"
		sys.exit(1)


	plist_content = plistlib.readPlistFromString(data[start_point:end_point] + '</plist>')

	print "Name: " + plist_content['Name']
	print "Created on: " + str(plist_content['CreationDate'])
	print "Expires on: " + str(plist_content['ExpirationDate'])
	print "=================================="
	print "Provisioning Devices( "+str(len(plist_content['ProvisionedDevices']))+" ) :"
	for x in plist_content['ProvisionedDevices']:
		print x


	print "=================================="
	print "Conntected Devices:"
	tmp = os.popen("system_profiler SPUSBDataType | sed -n -e '/iPad/,/Serial/p' -e '/iPhone/,/Serial/p' | grep 'Serial Number:' | awk -F ': ' '{print $2}'").read()
	if len(tmp) > 0:
		for udid in tmp.split('\n'):
			if udid in plist_content['ProvisionedDevices']:
				print udid + " *Associated with provisioning profile"
			else:
				print udid
	else:
		print "N/A"

if __name__ == "__main__":
	main(sys.argv[1:])

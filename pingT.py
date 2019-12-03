import subprocess
import re
import time
import datetime

#
# This is a simple program to capture ICMP latency over time.
# By default it will ping the designated server 1 time every 15 seconds
# It will run until terminated with CTRL-C
#

# Capture date to create filename
date = datetime.datetime.now().strftime("%Y-%m-%d-%f")

# Change IP to desired value. 
IP = "8.8.8.8"
fIP = open(IP+date+".csv", "w")

while True:
	# ping from windows os
	ping = subprocess.Popen(["ping", IP, "-n", "1"], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	# capture the results
	output = ping.communicate()
	# define search pattern 
	pattern = r"Average = (\d+\S+)"
	# capture time for time stamp
	ct = time.ctime()
	try: # added this bit to capture Index Error when packet is lost
		reout = re.findall(pattern, output[0].decode())[0]
	except IndexError:
		fIP.write(IP+","+"No Response"+","+ct+"\n")
	# write data to file
	fIP.write(IP+","+reout+","+ct+"\n")
	print(IP+","+reout+","+ct)
	# wait 15 seconds
	time.sleep(15)

fIP.close()
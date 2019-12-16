import subprocess
import re
import time
import datetime
import signal
import sys

#
# This is a simple program to capture ICMP latency over time.
# By default it will ping the designated server 1 time every 15 seconds
# It will run until terminated with CTRL-C
#

# function to catch ctl-c
def signal_handler(signal, frame):
	print("Ctl-C was pressed, the program has ended.")
	sys.exit(0)

# Capture date to create filename
date = datetime.datetime.now().strftime("%Y-%m-%d-%f")

# Change IP to desired value. 
IP = input("Enter an IP address or URL: ")
PI = input("Enter the ping frequency: ")
while int(PI) not in range(1,300):
	PI = input("Please enter a value between 1 and 300: ")

fIP = open(IP+date+".csv", "w")

while True:
        # ping from linux os
        ping = subprocess.Popen(["ping", IP, "-c", "1"], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        # capture the results
        output = ping.communicate()
        # define search pattern
        pattern = r"time=(.)"
        # capture time for time stamp
        ct = time.ctime()
        try: # added this bit to capture Index Error when packet is lost
                reout = re.findall(pattern, output[0].decode())[0]
        except IndexError:
                fIP.write(IP+","+"No Response"+","+ct+"\n")
        # write data to file
        fIP.write(IP+","+reout+","+ct+"\n")
        print(IP+","+reout+","+ct)
        # check for ctl-c
        signal.signal(signal.SIGINT, signal_handler)
        # wait the appropriate number of seconds
        time.sleep(int(PI))

fIP.close()

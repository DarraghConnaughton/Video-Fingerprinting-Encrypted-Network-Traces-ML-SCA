# import time
from ping3 import ping
import time
import subprocess
import re


ip = "192.168.4.1"
# count = 0

# # print(f"Processing IP: {ip}")
# while True:
#     print(f'{time.time()}, {ping(ip)}')
#     count+=1
#     time.sleep(200/1000)

# def ping(ip):
#     # Implement your ping logic here
#     # You can use the 'subprocess' module to execute ping commands
#     # and return the results.
#     # For example:
#     # ping_process = subprocess.Popen(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     # stdout, err = ping_process.communicate()

#     try:
#         ping_output = subprocess.check_output(['ping', '-c', '1', ip], stderr=subprocess.STDOUT, universal_newlines=True)
#         rtt_match = re.search(r"time=(\d+\.\d+)", ping_output)
#         if rtt_match:
#             print(f'{time.time()}, {float(rtt_match.group(1))}')
#     except subprocess.CalledProcessError:
#         pass

while True:
    # start_time = time.time()

    # Send the ping and print the result
    # ping(ip)
    print(f'{time.time()}, {ping(ip)}')
    # time.sleep(200/1000)
    time.sleep(100/1000)
    # time.sleep(max(0, 0.2 - (time.time() - start_time)))

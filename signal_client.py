#!/usr/bin/python3
# Need to install pydbus - pip3 install --user pydbus

# Look into threading to have main loop receiving messages and threads called on specific actions

from requests import get
import os

from pydbus import SystemBus
import zmq

bus = SystemBus()
signal_send = SystemBus().get('org.asamk.Signal')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")

# TODO Setup logging instead of printing to screen
# TODO Make this object orientated
# Only return messages from my number
number_filter = "+16303366257"
if isinstance(number_filter, bytes):
    number_filter = number_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, number_filter)

def send_message(number, message):
    print("sending message")
    signal_send.sendMessage(message, [], [number])
    return 0

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=",""))

def run_ping_test():
    numPings = 2
    pingTimeout = 2
    maxWaitTime = 6
    response = os.popen("ping -c %s -W %s -w %s 8.8.8.8" % (numPings, (pingTimeout * 1000), maxWaitTime)).read()
    result = response.split("\n")
    return result[-2]
    # return { 'date': datetime.now(), 'success': success }

def run_speed_test():
    # run a speed test
    result = os.popen("speedtest-cli --simple").read()
    if 'Cannot' in result:
        return "Error with speed test"
        # return { 'date': datetime.now(), 'uploadResult': 0, 'downloadResult': 0, 'ping': 0 }

    # Result:
    # Ping: 529.084 ms
    # Download: 0.52 Mbit/s
    # Upload: 1.79 Mbit/s
    
    return result
    # resultSet = result.split('\n')
    # pingResult = resultSet[0]
    # downloadResult = resultSet[1]
    # uploadResult = resultSet[2]

    # pingResult = float(pingResult.replace('Ping: ', '').replace(' ms', ''))
    # downloadResult = float(downloadResult.replace('Download: ', '').replace(' Mbit/s', ''))
    # uploadResult = float(uploadResult.replace('Upload: ', '').replace(' Mbit/s', ''))

    # return { 'date': datetime.now(), 'uploadResult': uploadResult, 'downloadResult': downloadResult, 'ping': pingResult }

def generate_message(number, input_message):
    """Parse the input message and determine a return
    """
    if input_message == "\help":
        # help
        return_message = "Possible options are:\n\n\help: Return this screen\n\\temp: Return temperature\n\ip: Return external ip address\n\ping: Return 8.8.8.8 ping\n\speedtest: Speedtest"
    elif input_message == "\\temp":
        # RPi temperature
        temp = measure_temp()
        return_message = "Temperature: {}".format(temp)
    elif input_message == "\ip": 
        # Current ip address
        ip = get('https://api.ipify.org').text
        return_message = "IP Address: {}".format(ip)
    elif input_message == "\ping":
        return_message = run_ping_test()
    elif input_message == "\speedtest":
        return_message = run_speed_test()
    else:
        return_message = "Unknown command. Try \help"
     
    return return_message


if __name__ == "__main__":
    while True:
        string = socket.recv_string()
        number, message = string.split()
        if message[0] == "\\":
            return_message = generate_message(number, message)
            send_message(number, return_message)

#!/usr/bin/python3
# Need to install pydbus - pip3 install --user pydbus

# Look into threading to have main loop receiving messages and threads called on specific actions

from pydbus import SystemBus
import zmq

bus = SystemBus()
signal_send = SystemBus().get('org.asamk.Signal')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")

number_filter = "+16303366257"
if isinstance(number_filter, bytes):
    number_filter = number_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, number_filter)

def send_message(number, message):
    print("sending message")
    signal_send.sendMessage(message, [], [number])
    return 0


if __name__ == "__main__":
    while True:
        string = socket.recv_string()
        number, message = string.split()
        send_message(number, message)

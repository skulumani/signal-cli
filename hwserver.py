# Listen to signal messages from the dbus and send out on a socket
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    # wait for request from client
    message = socket.recv()
    print("Received request: {}".format(message))
    
    time.sleep(1)
    # send back
    socket.send(b"World")

# Listens to the socket from teh client and send messages it receives
import zmq

context = zmq.Context()

# socket to talk to server
print("Conneting to hello world server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# 10 requests waiting for reply
for request in range(10):
    print("Sending request {}".format(request))
    socket.send(b"Hello")

    # get reply
    message = socket.recv()
    print("Received reply {} [ {} ]".format(request, message))

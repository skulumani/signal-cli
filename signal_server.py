#!/usr/bin/python3
# Need to install pydbus - pip3 install --user pydbus

# Look into threading to have main loop receiving messages and threads called on specific actions

from pydbus import SystemBus
from gi.repository import GLib
import zmq

bus = SystemBus()
signal_listen = bus.get('org.asamk.Signal')
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

def message_callback(timestamp, source, groupID, message, attachments):
    # groupID is empty if not a group
    # attachments will be a path to the attachment

    # convert unix time to something useful
    # ts = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    print("\n{} From:{}\n{}".format(timestamp, source, message))
    # parse the message to check for strings
    socket.send_string("{} {}".format(source, message))
    # send message out on socket
    return 0

def listen():
    signal_listen.onMessageReceived = message_callback
    # start the sending thread

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()


if __name__ == "__main__":
    listen()


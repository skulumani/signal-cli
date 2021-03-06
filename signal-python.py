#!/usr/bin/python3
# Need to install pydbus - pip3 install --user pydbus

# Look into threading to have main loop receiving messages and threads called on specific actions

from pydbus import SystemBus
from gi.repository import GLib
import argparse
from datetime import datetime
import threading
import queue
import pdb

message_queue = queue.Queue()

bus = SystemBus()
signal_listen = bus.get('org.asamk.Signal')
signal_send = SystemBus().get('org.asamk.Signal')
send_messages_flag = True

def send_worker(message_queue):
    """Send messages from the queue over a different bus to sending client
    """

    while send_messages_flag:
        try:
            number, message = message_queue.get()
            signal_send.sendMessage(message, [] , [number])
        except queue.Empty:
            return

        # send_message(number, message)
        message_queue.task_done()

def send_message(number, message):
    signal_send.sendMessage(message, [], [number])
    return 0

def message_callback(timestamp, source, groupID, message, attachments):
    # groupID is empty if not a group
    # attachments will be a path to the attachment

    # convert unix time to something useful
    # ts = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    print("\n{} From:{}\n{}".format(timestamp, source, message))
    # do this with a hashmap instead of logic
    if message == 'help':
        # send a message back on the bus 
        message_queue.put((source, "Return help section"))
    elif message == 'random':
        message_queue.put((source, "A random string"))
    
    return 0

def listen():
    signal_listen.onMessageReceived = message_callback
    # start the sending thread
    send_thread = threading.Thread(target=send_worker, args=(message_queue,))
    send_thread.daemon = True
    send_thread.start()

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
    send_messages_flag = False

# signal.sendGroupMessage(data, [], [___GROUP___])
# replace ___GROUP___ with byte-representation of 
# e.g. 0x01, 0x23,  0x45, 0x67,  0x89, 0xab,   0xcd, 0xef,   0x01, 0x23,   0x45, 0x67,   0x89, 0xab,   0xcd, 0xef
# obtain these bytes by:
# grep "groupId" ___SIGNAL_CONFIG_FILE___
# where ___SIGNAL_CONFIG_FILE___ is the signal configuration stored in .config/signal/data/
# echo ___BASE64_REPRESENTATION___ | base64 --decode | hexdump -x
# where ___BASE64_REPRESENTATION___ is the string stored in that line
# and splitting the two-byte words into single bytes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send/Receive Signal messages")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--send', nargs=2, help="Send a message to number")
    group.add_argument('--receive', action='store_true', help='Receive messages and print')
    args = parser.parse_args()

    if args.send:
        number = args.send[1]
        message = args.send[0]
        send_message(number, message)
    elif args.receive:
        listen()


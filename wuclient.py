import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting data from weather server")
socket.connect("tcp://localhost:5556")

zip_filter = sys.argv[1] if len(sys.argv) > 1 else "20012"

if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')

socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# process indefinately
for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    print("Temp {}".format(temperature))


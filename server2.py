import pickle
import socket

# A simple dictionary to send over the network
data = {'Python': 'Fun', 'Pickle': 'Tasty'}

# Serialize the dictionary
serialized_data = pickle.dumps(data)

# Send the serialized data over a network (omitting the networking code for brevity)
# socket.send(serialized_data)

# On the receiving end...

# Receive the serialized data (omitting the networking code for brevity)
# received_data = socket.recv(1024)

# Deserialize the data
# deserialized_data = pickle.loads(received_data)
# print(deserialized_data)

# Output (on the receiving end):
# {'Python': 'Fun', 'Pickle': 'Tasty'}

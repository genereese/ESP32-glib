# GSPNOW Usage

You probably want to hook up your ESP32 boards to different computers as your dev system will likely get confused if you have multiple ESP32 boards connected to it at the same time.

## On the transmitting ESP32
Technically, this is all you need to do on the transmitter, but you will likely want to send to specific boards rather than broadcast to everything:
```
from glib import gspnow
c = gspnow.Connection()
c.broadcast("Some data")
```

To send to a specific board or boards:
```
# Import the connection library
from glib import gspnow

# Create the base connection object
c = gspnow.Connection()

# Add a PeerGroup for your receiver ESP board(s)
peer_group_receivers = c.peerGroupAdd("Receivers")

# Add your Peers to the receivers PeerGroup
peer_receiver_1 = peer_group_receivers.peerAdd("AA:AA:AA:AA:AA:AA", "Optional Name")
peer_receiver_2 = peer_group_receivers.peerAdd("BB:BB:BB:BB:BB:BB")

# Add another PeerGroup for fun
peer_group_fun = c.peerGroupAdd("Fun Group")

# Add a peer to the fun group
peer_fun_1 = peer_group_fun.peerAdd("CC:CC:CC:CC:CC:CC", "The fun device")

# Create some test data to send
test_data = {'name': "Gene",
             'description': 'Cool guy',
             'age': 43}

# Send the data to all configured peers
c.send(test_data)

# Send the data to all Peers in just one PeerGroup
peer_group_receivers.send(test_data)

# Send the data to just one Peer
peer_fun_1.send(test_data)
```

## On the receiving ESP board(s)
```
# Import the library
from glib import gspnow

# Set up the ESPNOW connection
c = gspnow.Connection()

# Set up the sender's PeerGroup
peer_group_sender = c.peerGroupAdd("Sender")

# Add the MAC of the sending device as a Peer
#  This has to be done or this device will ignore any data received.
#  This prevents it from receiving unintentional data from unauthorized ESP boards that are transmitting
peer_sender = peer_group_sender.peerAdd("9C:9C:1F:E9:D6:14")

# Finally, you need to override the Connection object's callback function to do
#  something useful with the data it receives

# Define a new callback function that accepts two parameters, the sender's MAC address and the data:
#  This function is run every time this board receives data from an authorized sender
def onDataReceived(sender, data):
  # Do something cool with the data
  print("Received data from: " + sender)
  print()
  print("Data:")
  print(data)
  print()

# Actually overwrite the Connection's default callback function with the new one:
c.onDataReceived = onDataReceived
```

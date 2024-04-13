# GSPNOW Usage

## On the transmitting ESP32

```
# Import the connection library
import gspnow

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
             'description: 'Cool guy',
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
import gspnow

# Set up the ESPNOW connection
c = gspnow.Connection()

# Set up the sender's PeerGroup
peer_group_sender = c.peerGroupAdd("Sender")

# Add the MAC of the sending device as a Peer
#  This has to be done or this device will ignore any data received.
#  This prevents it from receiving unintentional data from unauthorized ESP boards that are transmitting
peer_sender = peer_group_sender.peerAdd("EE:EE:EE:EE:EE:EE")

# Finally, you need to override the Connection object's callback function to do something useful with the data it receives

# Define a new callback function that accepts two parameters, the sender's MAC address and the data:
def onDataReceived(sender, data):
  # Do something cool with the data
  print("Received data from: " + sender + " : " + data)

# Actually overwrite the Connection's default callback function with the new one:
c.onDataReceived = onDataReceived
```

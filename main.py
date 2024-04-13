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

# Finally, you need to override the Connection object's callback function to do something useful with the data it receives

# Define a new callback function that accepts two parameters, the sender's MAC address and the data:
def onDataReceived(sender, data):
  # Do something cool with the data
  print("Received data from: " + sender)
  print()
  print("Data:")
  print(data)
  print()

# Actually overwrite the Connection's default callback function with the new one:
c.onDataReceived = onDataReceived
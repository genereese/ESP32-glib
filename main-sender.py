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

c.broadcast(test_data)

# Handle imports
import espnow
import network
import pickle


class Connection:

    """ Represents an ESPNOW connection """

    def __init__(self):

        # Activate WLAN interface
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)

        # Set up ESPNOW
        self._connection = espnow.ESPNow()
        self._connection.active(True)

        self.peer_groups = []

        # Set up the broadcast PeerGroup
        peer_group_broadcast = self.peerGroupAdd("BROADCAST")
        peer_group_broadcast.peerAdd("BROADCAST", "FF:FF:FF:FF:FF:FF")

    def getPeerGroupDefault(self):
        
        try:
            return self.peer_groups[0]
        except:
            return None

    def peerGroupAdd(self, name):

        peer_group = PeerGroup(name, self._connection)
        self.peer_groups.append(peer_group)
        return peer_group
    
    def peerGroupFind(self, name):

        name = name.upper()

        print("Searching for group:", name)
        for peer_group in self.peer_groups:
            if (peer_group.name == name):
                print(" Found group.")
                return peer_group
        
        print(" Couldn't find a group with that name.")
        return None

    def broadcast(self, data):

        #print("Broadcasting:")
        self.peer_groups[0].send(data)
    
    def send(self, data):

        #print("Sending to all PeerGroups:")
        if (len(self.peer_groups) > 1):
            for peer_group in self.peer_groups[1:]:
                peer_group.send(data)
        else:
            print(" ERROR: No PeerGroups found.")


class PeerGroup:
    """ Represents a group of Peers communicating via ESPNOW """

    def __init__(self, name, connection):

        # Set the PeerGroup's attributes
        self.name = name.upper()
        self._connection = connection

        # Set up the peer list
        self.peers = []

    def peerAdd(self, name, mac_address):
        
        print(" Adding peer:", mac_address)
        peer = Peer(name, mac_address, connection=self._connection)
        self.peers.append(peer)
        try:
            self._connection.add_peer(peer.getMACEncoded())
        except OSError:
            print("  Peer already exists!")
        return peer
    
    def peerRemove(self, mac_address):

        print(" Removing peer:", mac_address)
        index = 0
        for peer in self.peers:
            if (peer.getMAC() == mac_address):
                self.connection.del_peer(peer.getMACEncoded())
                self.peers.pop(index)
            index += 1
    
    def peerFindByName(self, name):

        name = name.upper()

        print(" Searching for Peer by name:", name)
        for peer in self.peers:
            if (peer.getName() == name):
                print(" Success.")
                return peer
        print("  No match could be located.")
        return None
    
    def peerFindByMAC(self, mac):

        mac = mac.upper()
        
        print(" Searching for Peer by MAC:", mac)
        for peer in self.peers:
            if (peer.getMAC() == mac):
                print("  Success.")
                return peer
        print("  No match could be located.")
        return None
    
    def send(self, data):

        if (len(self.peers) > 0):

            #print(" Sending to:", self)
            
            for peer in self.peers:
                peer.send(data)
        else:

            print(" ERROR: No peers in group.")
    
    def __repr__(self):
        return "PeerGroup (" + self.name + ")"


class Peer:

    def __init__(self, name, mac_address, connection):

        self._name = name.upper()
        self._mac_string = mac_address.upper()
        self._mac_btyearray = self._encode()
        self._connection = connection
    
    def _encode(self):

        return bytearray(int(part, 16) for part in self._mac_string.split(":"))

    def _decode(self):

        return ':'.join('{:02x}'.format(b) for b in self._mac_btyearray).upper()
    
    def getName(self):

        return self._name

    def getMAC(self):

        return self._mac_string
    
    def getMACEncoded(self):
        
        return self._mac_btyearray
    
    def send(self, data):

        serialized_data = pickle.dumps(data)
        #print("  Sending to:", self, "-", serialized_data)
        self._connection.send(self.getMACEncoded(), serialized_data)
    
    def __repr__(self):

        return "Peer (" + self.getName() + " - " + self.getMAC() + ")"
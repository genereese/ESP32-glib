
# Handle imports
import espnow
import network
import time

from glib import pickle
from glib.glog import Logger

"""
Log levels:
    1 = Errors only
    2 = Information and errors
    3 = Debug, info, and errors
"""
logger = Logger(2)

class Peer:
    """ Represents a Peer communicating via ESPNOW """

    def __init__(self, mac_address, name="", connection=None):

        self._name = name.upper()
        self._mac_string = mac_address.upper()
        self._mac_btyearray = self._encode()
        self._connection = connection
    
    def _encode(self):

        return bytearray(int(part, 16) for part in self._mac_string.split(":"))

    def _decode(self):

        return ':'.join('{:02x}'.format(b) for b in self._mac_btyearray).upper()

    def setName(self, name):

        self._name = name.upper()
    
    def getName(self):

        return self._name

    def getMAC(self):

        return self._mac_string
    
    def getMACEncoded(self):
        
        return self._mac_btyearray
    
    def send(self, data):

        serialized_data = pickle.dumps(data)
        logger.info("  Sending to: " + str(self))
        logger.info("   " + str(data))
        self._connection.send(self._mac_btyearray, serialized_data)
    
    def __repr__(self):
        return_string = "Peer (" + self.getMAC()
        if (len(self.getName()) > 0):
            return_string = return_string + " - " + self.getName()
        return_string = return_string + ")"
        return return_string


class PeerGroup:
    """ Represents a group of Peers communicating via ESPNOW """

    def __init__(self, parent, name):

        # Set the PeerGroup's attributes
        self.name = name.upper()
        self.parent = parent

        # Set up the peer list
        self.peers = {}

    def peerAdd(self, mac_address, name=""):
        
        logger.info(" Adding peer: " + mac_address)

        peer = Peer(mac_address, name, connection=self.parent._connection)
        try:
            peer = Peer(mac_address, name, connection=self.parent._connection)
        except:
            logger.info("  ERROR: Could not add peer")
        else:
            self.parent._connection.add_peer(peer._mac_btyearray)
            self.peers[peer.getMAC()] = peer
            self.parent.peers[peer.getMAC()] = peer
            return peer
    
    def peerRemove(self, mac_address):

        logger.info(" Removing Peer: " + mac_address)
        
        try:
            peer = self.peers[mac_address]
        except KeyError:
            logger.info("  Could not find referenced Peer.")
        else:
            self.parent._connection.del_peer(peer.getMACEncoded())
            del self.peers[mac_address]
            del self.parent.peers[mac_address]
    
    def peerFindByName(self, name):

        name = name.upper()

        logger.info(" Searching for Peer by name: " + name)
        for peer_mac in self.peers.keys():
            peer = self.peers[peer_mac]
            if (peer.getName() == name):
                logger.info(" Success.")
                return peer
        logger.info("  No match could be located.")
        return None
    
    def peerFindByMAC(self, mac_address):

        mac_address = mac_address.upper()
        
        logger.info(" Searching for Peer by MAC: " + mac_address)

        try:
            peer = self.peers[mac_address]
        except KeyError:
            logger.info("  Could not find referenced Peer.")
        else:
            logger.info("   Success.")
            return peer
    
    def send(self, data):

        if (len(self.peers) > 0):

            logger.info(" Sending to: " + str(self))
            
            for peer_mac in self.peers.keys():
                self.peers[peer_mac].send(data)
        else:

            logger.info(" ERROR: No peers in group.")
    
    def __repr__(self):
        return "PeerGroup (" + self.name + ")"


class Connection(Peer):

    """ Represents both a Peer and an ESPNOW connection """

    def __init__(self):

        # Set up self-referenced Peer information
        self._name = "SELF"

        # Activate WLAN interface
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)

        # Set up ESPNOW connection
        self._connection = espnow.ESPNow()
        self._connection.active(True)
    
        # Set up additional self-derived Peer information
        self._mac_btyearray = self._wlan.config('mac')
        self._mac_string = self._decode()

        # Initialize the list of Peers and PeerGroups
        self.peers = {}
        self.peer_groups = {}

        # Set up the broadcast PeerGroup
        peer_group_broadcast = self.peerGroupAdd("BROADCAST")
        peer_broadcast = peer_group_broadcast.peerAdd("FF:FF:FF:FF:FF:FF", "BROADCAST")
        del self.peers[peer_broadcast.getMAC()]        

        # Set up the default callback handler
        self._connection.irq(self._callbackOnReceive)

        logger.info("Configured connection for: " + self.getMAC())
    
    def _callbackOnReceive(self, event):

        sender, data = event.irecv(0)
        if not (sender):
            return
        
        sender_mac = ':'.join('{:02x}'.format(b) for b in sender).upper()

        logger.info("Received data from: " + sender_mac)

        try:
            self.peers[sender_mac]
        except KeyError:
            logger.info(" Sender is not in peer list; ignoring sent data.")
            return
        else:
            data = pickle.loads(data)
            self.onDataReceived(sender_mac, data)

    def onDataReceived(self, sender, data):
        logger.info(sender, ":", data)

    def getPeerGroupDefault(self):
        
        try:
            return self.peer_groups['BROADCAST']
        except:
            return None

    def peerGroupAdd(self, name):

        name = name.upper()
        peer_group = self.peerGroupFind(name)

        if not(peer_group):
            logger.info(" Creating group: " + name)
            peer_group = PeerGroup(self, name)
            self.peer_groups[name] = peer_group

        return peer_group
    
    def peerGroupFind(self, name):

        name = name.upper()
        logger.info("Searching for group: " + name)

        try:
            peer_group = self.peer_groups[name]
        except KeyError:
            logger.info(" No results found.")
            return
        else:
            logger.info(" Found group.")
            return peer_group

    def broadcast(self, data):

        logger.info("Broadcasting:")
        self.peer_groups['BROADCAST'].send(data)
    
    def send(self, data):

        logger.info("Sending to all PeerGroups:")
        if (len(self.peer_groups) > 1):
            for peer_group_name in self.peer_groups.keys():
                if (peer_group_name != "BROADCAST"):
                    self.peer_groups[peer_group_name].send(data)
        else:
            logger.info(" ERROR: No PeerGroups found.")
            logger.info('  Use .broadcast() instead, or add a PeerGroup with .peerGroupAdd("name")')
    
    def turnOff(self):
        self._wlan.active(False)
    
    def turnOn(self):
        self._wlan.active(True)

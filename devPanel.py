class ClusterNode:
    def __init__(self):
        self.hostname = "localhost"
        self.ipaddress = "127.0.0.1"
        self.root_password = ""
    def setIP(self, ipaddress):
        self.ipaddress = ipaddress
    def setRootPassword(self, root_password):
        self.root_password = root_password
    def setHostname(self, hostname):
        self.hostname = hostname    

class ClusterConfig:
    def __init__(self):
        self.webNodes = []
        self.dbNodes = []
        self.lbNodes = []
        self.masterNode = None

    def setMaster(self, node_ip):
        self.masterNode = node_ip

    def addNode(self, **kwargs):
        for key, value in kwargs.items():
            print '%s = %s' % (key, value)
        

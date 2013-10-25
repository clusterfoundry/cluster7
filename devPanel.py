class ClusterNode:
    def __init__(self):
        self.hostname = None
        self.password = None
        self.ipaddress = None
    def setPassword(self, password):
        self.password = password

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
        

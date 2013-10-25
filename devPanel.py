class ClusterConfig:
    def __init__(self):
        self.webNodes = []
        self.dbNodes = []
        self.lbNodes = []
        self.masterNode = None

    def setMaster(self, node_ip):
        self.masterNode = node_ip

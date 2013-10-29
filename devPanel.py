class ClusterNode:
    def __init__(self):
        self.hostname = "localhost"
        self.ipaddress = "127.0.0.1"
        self.root_password = None
    def setIP(self, ipaddress):
        self.ipaddress = ipaddress
    def setRootPassword(self, root_password):
        self.root_password = root_password
    def setHostname(self, hostname):
        self.hostname = hostname

class ClusterDB:
    def __init__(self):
        self.databaseType = "mysql"
        config = DBConfig()
    def setDBType(self, dbType="mysql"):
        if dbType == "mysql":
            self.databaseType = dbType
        else:
            raise "Unknown database type: [%s]" % dbType

class DBConfig:
    def __init__(self):
        self.adminUser = "root"
        self.adminPassword = None
        self.dataDir = "/var/lib/mysql"
        self.bindAddress = "127.0.0.1"
        self.bindPort = 4000
# TODO: Finish Class        
        
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
        

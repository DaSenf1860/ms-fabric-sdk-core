import os
from time import sleep

from msfabricpysdkcore.auth import FabricAuthClient, FabricServicePrincipal, FabricSparkUtilsAuthentication

class FabricClient():
    """FabricClient class to interact with Fabric API"""

    def __init__(self, tenant_id = None, client_id = None, client_secret = None, silent=False) -> None:
        """Initialize FabricClient object"""
        self.tenant_id = tenant_id if tenant_id else os.getenv("FABRIC_TENANT_ID")
        self.client_id = client_id if client_id else os.getenv("FABRIC_CLIENT_ID")
        self.client_secret = client_secret if client_secret else os.getenv("FABRIC_CLIENT_SECRET")

        self.scope = "https://api.fabric.microsoft.com/.default"

        if self.client_id is None or self.client_secret is None or self.tenant_id is None:
            try:
                self.auth = FabricSparkUtilsAuthentication(silent=silent)
            except:
                self.auth = FabricAuthClient(silent=silent)
        else:
            self.auth = FabricServicePrincipal(tenant_id = self.tenant_id,
                                               client_id = self.client_id, 
                                               client_secret = self.client_secret,
                                               silent=silent)
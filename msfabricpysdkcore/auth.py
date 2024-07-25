from warnings import warn

import requests
from abc import abstractmethod
from azure.identity import AzureCliCredential
from msfabricpysdkcore.util import logger
import logging
try:
    from notebookutils import mssparkutils
except ImportError:
    pass
class FabricAuth():
    """FabricAuth class to interact with Entra ID"""

    _logger: logging.Logger

    def __init__(self, scope):
        """Initialize FabricAuth object"""
        self._logger = logger.getChild(__name__)
        self.scope = scope

    @abstractmethod
    def get_token(self):
        """Get token from Azure AD"""
        pass

    def get_headers(self):
        """Get headers for API requests"""
        access_token = self.get_token()
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        return headers


class FabricAuthClient(FabricAuth):
    """FabricAuthClient class to interact with Entra ID"""

    def __init__(self, scope, silent = None):
        super().__init__(scope)
        self._logger.info("Using Azure CLI for authentication")
        self.auth = AzureCliCredential()

        if silent is not None:
            warn("The 'silent' parameter is deprecated and will be removed in a future version.", DeprecationWarning, stacklevel=2)

    def get_token(self):
        """Get token from Azure AD"""
        token = self.auth.get_token(self.scope)
        return token.token

class FabricServicePrincipal(FabricAuth):
    """FabricServicePrincipal class to interact with Entra ID"""

    def __init__(self, tenant_id, client_id, client_secret, scope, silent = None):
        super().__init__(scope)

        self._logger.info("Using Service Principal for authentication")

        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

        if silent is not None:
            warn("The 'silent' parameter is deprecated and will be removed in a future version.", DeprecationWarning, stacklevel=2)

    
    def get_token(self):
        """Get token from Azure AD"""
        # Get token from Azure AD
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': f'{self.client_id}',
            'client_secret': f'{self.client_secret}',
            'scope': self.scope
        }
        response = requests.post(url, data=payload)
        access_token = response.json().get('access_token')
        return access_token
    
class FabricSparkUtilsAuthentication(FabricAuth):
    """FabricSparkUtilsAuthentication class to interact with Entra ID"""

    def __init__(self, scope, silent=None):
        # super().__init__(scope)

        mssparkutils.credentials.getToken("pbi")
        self._logger.info("Using Synapse Spark Utils for authentication")

        if silent is not None:
            warn("The 'silent' parameter is deprecated and will be removed in a future version.", DeprecationWarning, stacklevel=2)

    def get_token(self):
        """Get token from Azure AD"""
        token = mssparkutils.credentials.getToken("pbi")
        return token
    


import requests
from abc import abstractmethod
from azure.identity import AzureCliCredential

class FabricAuth():
    """FabricAuth class to interact with Entra ID"""

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

    def __init__(self):
        print("Using Azure CLI for authentication")
        self.auth = AzureCliCredential()

    def get_token(self):
        """Get token from Azure AD"""
        token = self.auth.get_token("https://api.fabric.microsoft.com/.default")
        return token.token

class FabricServicePrincipal(FabricAuth):
    """FabricServicePrincipal class to interact with Entra ID"""

    def __init__(self, tenant_id, client_id, client_secret):
        print("Using Service Principal for authentication")

        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

        self.scope = "https://api.fabric.microsoft.com/.default"

    
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
    
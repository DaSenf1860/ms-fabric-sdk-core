import requests
from abc import abstractmethod
from azure.identity import AzureCliCredential
import msal

try:
    from notebookutils import mssparkutils
except ImportError:
    pass


class FabricAuth:
    """FabricAuth class to interact with Entra ID"""

    @abstractmethod
    def get_token(self):
        """Get token from Azure AD"""
        pass

    def get_headers(self):
        """Get headers for API requests"""
        access_token = self.get_token()
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        return headers


class FabricAuthClient(FabricAuth):
    """FabricAuthClient class to interact with Entra ID"""

    def __init__(self, silent=False):
        if not silent:
            print("Using Azure CLI for authentication")
        self.auth = AzureCliCredential()

    def get_token(self):
        """Get token from Azure AD"""
        token = self.auth.get_token("https://api.fabric.microsoft.com/.default")
        return token.token


class FabricServicePrincipal(FabricAuth):
    """FabricServicePrincipal class to interact with Entra ID"""

    def __init__(self, tenant_id, client_id, client_secret, silent=False):
        if not silent:
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
            "grant_type": "client_credentials",
            "client_id": f"{self.client_id}",
            "client_secret": f"{self.client_secret}",
            "scope": self.scope,
        }
        response = requests.post(url, data=payload)
        access_token = response.json().get("access_token")
        return access_token


class FabricSparkUtilsAuthentication(FabricAuth):
    """FabricSparkUtilsAuthentication class to interact with Entra ID"""

    def __init__(self, silent=False):
        mssparkutils.credentials.getToken("pbi")
        if not silent:
            print("Using Synapse Spark Utils for authentication")

    def get_token(self):
        """Get token from Azure AD"""
        token = mssparkutils.credentials.getToken("pbi")
        return token


class MSALConfidentialClientApplicationAuthentication(FabricAuth):

    def __init__(
        self, tenant_id, client_id, client_secret, username, password, silent=False
    ):
        if not silent:
            print(
                "Using Microsoft Authentication Library (MSAL) ConfidentialClientApplication for authentication"
            )

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.scopes = ["https://api.fabric.microsoft.com/.default"]

        self.app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority,
        )

    def get_token(self):
        result = self.app.acquire_token_for_client(scopes=self.scopes)
        result = self.app.acquire_token_by_username_password(
            username=self.username,
            password=self.password,
            scopes=self.scopes,
        )
        return result["access_token"]

from abc import abstractmethod
import os
from time import sleep
import requests
import json

from msfabricpysdkcore.auth import FabricAuthClient, FabricServicePrincipal, FabricSparkUtilsAuthentication

class FabricClient():
    """FabricClient class to interact with Fabric API"""

    def __init__(self, scope, tenant_id = None, client_id = None, client_secret = None, silent=False) -> None:
        """Initialize FabricClient object"""
        self.tenant_id = tenant_id if tenant_id else os.getenv("FABRIC_TENANT_ID")
        self.client_id = client_id if client_id else os.getenv("FABRIC_CLIENT_ID")
        self.client_secret = client_secret if client_secret else os.getenv("FABRIC_CLIENT_SECRET")
        self.scope = scope
        #self.scope = "https://api.fabric.microsoft.com/.default"

        if self.client_id is None or self.client_secret is None or self.tenant_id is None:
            try:
                self.auth = FabricSparkUtilsAuthentication(self.scope, silent=silent)
            except:
                self.auth = FabricAuthClient(self.scope, silent=silent)
        else:
            self.auth = FabricServicePrincipal(scope= self.scope,
                                               tenant_id = self.tenant_id,
                                               client_id = self.client_id, 
                                               client_secret = self.client_secret,
                                               silent=silent)
            
    def get_token(self):
        """Get token from Entra"""
        return self.auth.get_token()

    def calling_routine(self, url, operation, body = None, headers=None, file_path = None, response_codes = [200], error_message = "Error",
                        continue_on_error_code = False, return_format = "value_json", paging = False,
                        wait_for_completion = True, continuation_token = None):
        """Routine to make API calls
        Args:
            url (str): The URL of the API
            operation (str): The operation to perform
            body (dict): The body of the request
            response_codes (list): The response codes to expect
            error_message (str): The error message
            continue_on_error_code (bool): Whether to continue on error code
            return_format (str): The format of the return
            paging (bool): Whether to paginate
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            dict: The response
        """
        original_url = url

        if continuation_token:
            last_part_url = url.split("/")[-1]   
            if "?" not in last_part_url:
                continuation_token  = f"?continuationToken={continuation_token}"
            else:
                continuation_token  = f"&continuationToken={continuation_token}"
            url = f"{url}{continuation_token}"

        response_codes.append(429)
        if headers is None:
            headers = self.auth.get_headers()
        for _ in range(10):
            if operation == "GET":
                response = requests.get(url=url, headers=headers)
            elif operation == "PATCH":
                if body is None:
                    response = requests.patch(url=url, headers=headers)
                else:
                    response = requests.patch(url=url, headers=headers, json=body)
            elif operation == "POST":
                if body is not None:
                    response = requests.post(url=url, headers=headers, json=body)
                elif file_path is not None:
                    headers.pop('Content-Type')
                    with open(file_path, 'rb') as f:
                        files = {"file": f}
                        response = requests.post(url=url, files=files, headers=headers)
                else:
                    response = requests.post(url=url, headers=headers)
            elif operation == "PUT":
                if body is None:
                    response = requests.put(url=url, headers=headers)
                else:
                    response = requests.put(url=url, headers=headers, json=body)
            elif operation == "DELETE":
                response = requests.delete(url=url, headers=headers)
            else:
                raise ValueError("Invalid operation")
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            elif response.status_code == 202:
                if wait_for_completion:
                    operation_result = self.long_running_operation(response.headers)
                    if "operation_result" in return_format:
                        return operation_result
                return response
            elif response.status_code not in response_codes:
                if continue_on_error_code:
                    return response
                raise Exception(f"{error_message}: {response.status_code} {response.text}")
            break

        if paging:
            resp_dict = json.loads(response.text)

            if return_format in ["data", "itemEntities", "Overrides", "accessEntities", "workspaces"]:
                items = resp_dict[return_format]
            else:
                items = resp_dict["value"]

                
            if "continuationToken" in resp_dict and resp_dict["continuationToken"]:
                continuation_token = resp_dict["continuationToken"]
                items_next = self.calling_routine(url=original_url, operation=operation, body=body, headers=headers,
                                                  response_codes=response_codes,
                                                  error_message=error_message, continuation_token=continuation_token,
                                                  return_format=return_format, paging=True, wait_for_completion=wait_for_completion)
                items.extend(items_next)
            if "etag" in return_format:
                return items, response.headers.get('ETag')
            return items

        if "value_json" in return_format:
            resp_dict = json.loads(response.text)
            if "etag" in return_format:
                return resp_dict["value"], response.headers.get('ETag')	
            return resp_dict["value"]
        
        if "json" in return_format:
            return json.loads(response.text)

        return response
    
    @abstractmethod
    def long_running_operation(self, headers):
        """Long running operation"""
        pass
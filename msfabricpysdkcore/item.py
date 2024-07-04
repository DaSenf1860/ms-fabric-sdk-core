import json 
import requests
from time import sleep

from msfabricpysdkcore.onelakeshortcut import OneLakeShortcut
from msfabricpysdkcore.job_instance import JobInstance
from msfabricpysdkcore.long_running_operation import check_long_running_operation

class Item:
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description="") -> None:
        
        self.id = id
        self.display_name = display_name
        self.description = description
        self.type = type
        self.definition = definition
        self.properties = properties
        self.workspace_id = workspace_id
        
        self.auth = auth

    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            'id': self.id,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.type,
            'definition': self.definition,
            'workspace_id': self.workspace_id,
            'properties': self.properties
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(item_dict, auth):
        """Create Item object from dictionary"""
        
        return Item(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
                    properties=item_dict.get('properties', None),
                    definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

    def delete(self, type = None):
        """Delete the workspace item"""

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/{type}/{self.id}"
        for _ in range(10):
            response = requests.delete(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error deleting item: {response.status_code}, {response.text}")
            break

        return response.status_code
    
    def get_definition(self, type = None, format = None):
        """Get the definition of the item"""
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/getDefinition"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/{type}/{self.id}/getDefinition"

        if format:
            url += f"?format={format}"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                operation_result = check_long_running_operation( response.headers, self.auth)
                self.definition = operation_result['definition']
                return operation_result
                
            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting item definition: {response.text}")
            break
        
        resp_dict = json.loads(response.text)
        self.definition = resp_dict['definition']
        return resp_dict
    
    def update(self, display_name = None, description = None, type = None):
        """Update the item"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/{type}/{self.id}"

        payload = dict()
        if display_name:
            payload['displayName'] = display_name
        if description:
            payload['description'] = description
        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=payload)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error updating item: {response.text}")
            break
        if display_name:
            self.display_name = payload['displayName']
        if description:
            self.description = payload['description']

        return self

    def update_definition(self, definition, type = None):
        """Update the item definition"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/updateDefinition"

        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/{type}/{self.id}/updateDefinition"
            
        payload = {
            'definition': definition
        }
        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=payload)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error updating item definition: {response.text}")
            break

        self.definition = payload['definition']
        return self
    
    def get_shortcut(self, path, name):
        """Get the shortcut in the item"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/shortcuts/{path}/{name}"
        
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error getting shortcut: {response.text}")
            break

        shortcut_dict = json.loads(response.text)
        shortcut_dict['workspaceId'] = self.workspace_id
        shortcut_dict['itemId'] = self.id
        return OneLakeShortcut.from_dict(shortcut_dict,
                                         auth = self.auth)
    
    def create_shortcut(self, path, name, target):
        """Create a shortcut in the item"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/shortcuts"

        body = {'name': name,
                'path': path,
                'target': target}

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (201, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error creating shortcut: {response.text}")
            break

        shortcut_dict = json.loads(response.text)
        shortcut_dict['workspaceId'] = self.workspace_id
        shortcut_dict['itemId'] = self.id
        return OneLakeShortcut.from_dict(shortcut_dict,
                                         auth = self.auth)
    
    def delete_shortcut(self, path, name):
        """Delete the shortcut in the item"""
        return self.get_shortcut(path, name).delete()
    

    def run_on_demand_item_job(self, job_type, execution_data = None):
        """Run an on demand job on the item"""

        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/jobs/instances?jobType={jobType}
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/jobs/instances?jobType={job_type}"
        payload = {
            'executionData': execution_data
        }

        for _ in range(10):
            if execution_data:
                response = requests.post(url=url, headers=self.auth.get_headers(), json=payload)
            else:
                response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue

            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error running on demand job: {response.text}")
            break
        job_instance_id = response.headers["Location"].split("/")[-1]
        job_instance = self.get_item_job_instance(job_instance_id=job_instance_id)
        return job_instance

    def get_item_job_instance(self, job_instance_id):
        """Get the job instance of the item"""

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/jobs/instances/{job_instance_id}"
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting job instance: {response.status_code}, {response.text}")
            break

        job_dict = json.loads(response.text)
        job_dict['workspaceId'] = self.workspace_id
        job_dict['itemId'] = self.id
        return JobInstance.from_dict(job_dict, auth=self.auth)
    
    def cancel_item_job_instance(self, job_instance_id):
        """Cancel a job instance ofjob the item"""
        return self.get_item_job_instance(job_instance_id=job_instance_id).cancel()
        
    def list_tables(self):
        raise NotImplementedError("List tables only works on Lakehouse Items")
    
    def load_table(self, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        raise NotImplementedError("Load table only works on Lakehouse Items")
    
    def create_external_data_share(self, paths, recipient):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/externalDataShares
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/externalDataShares"

        body = {
            'paths': paths,
            'recipient': recipient
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (201, 429):
                raise Exception(f"Error creating external data share: {response.status_code}, {response.text}")
            break
        return json.loads(response.text)
    
    def get_external_data_share(self, external_data_share_id):
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/externalDataShares/{externalDataShareId}
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/externalDataShares/{external_data_share_id}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting external data share: {response.status_code}, {response.text}")
            break
        return json.loads(response.text)
    
    def list_external_data_shares_in_item(self, continuationToken = None):
        # GET GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/externalDataShares?continuationToken={continuationToken}

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/externalDataShares"

        if continuationToken:
            url += f"?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            
            if response.status_code not in (200, 429):
                raise Exception(f"Error listing external data shares: {response.status_code}, {response.text}")
            break
        
        resp = json.loads(response.text)
        external_data_shares = resp['value']

        if 'continuationToken' in resp:
            external_data_shares_new = self.list_external_data_shares_in_item(continuationToken=resp['continuationToken'])
            external_data_shares.extend(external_data_shares_new)

        return external_data_shares
    
    def revoke_external_data_share(self, external_data_share_id):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/externalDataShares/{externalDataShareId}/revoke

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/externalDataShares/{external_data_share_id}/revoke"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error revoking external data share: {response.status_code}, {response.text}")
            break

        return response.status_code


    # One Lake data access security

    def list_data_access_roles(self, continuationToken = None):
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/dataAccessRoles

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/dataAccessRoles"

        if continuationToken:
            url += f"?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error revoking external data share: {response.status_code}, {response.text}")
            break

        resp_dict = json.loads(response.text)
        data_access_roles = resp_dict['value']
        etag = response.headers.get('ETag', None)

        if 'continuationToken' in resp_dict and resp_dict['continuationToken']:
            data_access_roles_new, etag = self.list_data_access_roles(continuationToken=resp_dict['continuationToken'])
            data_access_roles.extend(data_access_roles_new)

        return data_access_roles, etag
    
    def create_or_update_data_access_roles(self, data_access_roles, dryrun = False, etag_match = None):
        # PUT https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/dataAccessRoles

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.id}/dataAccessRoles"

        if dryrun:
            url += "?dryrun=true"

        if etag_match:
            if 'If-Match' in etag_match:
                headers = self.auth.get_headers()
                headers['If-Match'] = etag_match['If-Match']
            elif 'If-None-Match' in etag_match:
                headers = self.auth.get_headers()
                headers['If-None-Match'] = etag_match['If-None-Match']
            else:
                raise Exception("Etag match should include If-Match or If-None-Match")
        else:
            headers = self.auth.get_headers()

        body = {"value" : data_access_roles}
        
        for _ in range(10):
            response = requests.put(url=url, headers=headers, json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error creating or updating data access roles: {response.status_code}, {response.text}")
            break

        return response
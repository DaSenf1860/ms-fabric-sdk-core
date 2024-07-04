import json 
import requests
from time import sleep

from msfabricpysdkcore.item import Item
from msfabricpysdkcore.long_running_operation import check_long_running_operation

class Environment(Item):
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return Environment(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""),
            auth=auth)

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/sparkcompute
    def get_published_settings(self):
        """Get the published settings of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/sparkcompute"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting published settings: {response.status_code}, {response.text}")
            break

        resp_json = json.loads(response.text)        
        return resp_json
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/sparkcompute

    def get_staging_settings(self):
        """Get the staging settings of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/sparkcompute"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting staging settings: {response.status_code}, {response.text}")
            break

        resp_json = json.loads(response.text)        
        return resp_json


    def update_staging_settings(self,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        """Update the staging settings of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/sparkcompute"
        body = {}
        if driver_cores is not None:
            body['driverCores'] = driver_cores
        if driver_memory is not None:
            body['driverMemory'] = driver_memory
        if dynamic_executor_allocation is not None:
            body['dynamicExecutorAllocation'] = dynamic_executor_allocation
        if executor_cores is not None:
            body['executorCores'] = executor_cores
        if executor_memory is not None:
            body['executorMemory'] = executor_memory
        if instance_pool is not None:
            body['instancePool'] = instance_pool
        if runtime_version is not None:
            body['runtimeVersion'] = runtime_version
        if spark_properties is not None:
            body['sparkProperties'] = spark_properties

        
        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error updating staging settings: {response.status_code}, {response.text}")
            break

        return json.loads(response.text)

#  GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/libraries

    def get_published_libraries(self):
        """Get the published libraries of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/libraries"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting published libraries: {response.status_code}, {response.text}")
            break

        resp_json = json.loads(response.text)
        return resp_json
    
# GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries

    def get_staging_libraries(self):
        """Get the staging libraries of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/libraries"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting staging libraries: {response.status_code}, {response.text}")
            break

        resp_json = json.loads(response.text)
        return resp_json
    

    def upload_staging_library(self, file_path):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/libraries"
        headers = self.auth.get_headers()
        headers.pop('Content-Type', None)

        for _ in range(10):
            with open(file_path, 'rb') as f:
                files = {"file": f}
                response = requests.post(url=url, files=files, headers=headers)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error uploading staging library: {response.status_code}, {response.text}")
            break

        return response
    
# DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries?libraryToDelete={libraryToDelete}

    def delete_staging_library(self, library_to_delete):
        """Delete a library from the staging libraries of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/libraries?libraryToDelete={library_to_delete}"

        for _ in range(10):
            response = requests.delete(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error deleting staging libraries: {response.status_code}, {response.text}")
            break

        return response
    
# POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/publish

    def publish_environment(self):
        """Publish the staging settings and libraries of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/publish"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                publish_info = check_long_running_operation(response.headers, self.auth)
                return publish_info
            if response.status_code not in (200, 429):
                raise Exception(f"Error publishing staging: {response.status_code}, {response.text}")
            break

        resp_dict = json.loads(response.text)
        return resp_dict


# POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/cancelPublish

    def cancel_publish(self):
        """Cancel the publishing of the staging settings and libraries of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/cancelPublish"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error canceling publishing: {response.status_code}, {response.text}")
            break

        resp_dict = json.loads(response.text)
        return resp_dict
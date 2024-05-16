import json 
import requests
from time import sleep

from msfabricpysdkcore.item import Item
from msfabricpysdkcore.long_running_operation import check_long_running_operation

class Environment(Item):
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description="", 
                 sparkcompute = None, staging_sparkcompute = None, libraries = None, staging_libraries = None):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

        self.sparkcompute = sparkcompute
        self.staging_sparkcompute = staging_sparkcompute
        self.libraries = libraries
        self.staging_libraries = staging_libraries

    def from_dict(item_dict, auth):
        return Environment(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), 
            sparkcompute=item_dict.get('sparkcompute', None),
            staging_sparkcompute=item_dict.get('staging_sparkcompute', None),
            libraries=item_dict.get('libraries', None),
            staging_libraries=item_dict.get('staging_libraries', None),
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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error getting published settings: {response.text}")
            break

        resp_json = json.loads(response.text)        
        self.sparkcompute = resp_json
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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error getting staging settings: {response.text}")
            break

        resp_json = json.loads(response.text)        
        self.staging_sparkcompute = resp_json
        return resp_json

    def update_staging_settings(self, instance_pool, driver_cores, driver_memory, executor_cores, executor_memory,
                                dynamic_executor_allocation, spark_properties, runtime_version):
        """Update the staging settings of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/environments/{self.id}/staging/sparkcompute"
        body = {
            "instancePool": instance_pool,
            "driverCores": driver_cores,
            "driverMemory": driver_memory,
            "executorCores": executor_cores,
            "executorMemory": executor_memory,
            "dynamicExecutorAllocation": dynamic_executor_allocation,
            "sparkProperties": spark_properties,
            "runtimeVersion": runtime_version
        }
        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error updating staging settings: {response.text}")
            break

        self.staging_sparkcompute = body
        return body

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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error getting published libraries: {response.text}")
            break

        resp_json = json.loads(response.text)
        self.libraries = resp_json
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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error getting staging libraries: {response.text}")
            break

        resp_json = json.loads(response.text)
        self.staging_libraries = resp_json
        return resp_json
    

    def update_staging_libraries(self):
        raise NotImplementedError("This method is not implemented yet because the REST API is not complete")
    
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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error deleting staging libraries: {response.text}")
            break

        return response.text
    
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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error publishing staging: {response.text}")
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
                print(response.status_code)
                print(response.text)
                print(self)
                raise Exception(f"Error canceling publishing: {response.text}")
            break

        resp_dict = json.loads(response.text)
        return resp_dict
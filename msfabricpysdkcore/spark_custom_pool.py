import json
from time import sleep

import requests 


class SparkCustomPool:
    """Class to represent a custom pool in Microsoft Fabric"""

    def __init__(self, id, name, type, node_family, node_size, auto_scale, dynamic_executor_allocation, workspace_id, auth) -> None:
        
        self.id = id
        self.name = name
        self.type = type
        self.node_family = node_family
        self.node_size = node_size
        self.auto_scale = auto_scale
        self.dynamic_executor_allocation = dynamic_executor_allocation
        self.workspace_id = workspace_id
        
        self.auth = auth

    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "nodeFamily": self.node_family,
            "nodeSize": self.node_size,
            "autoScale": self.auto_scale,
            "dynamicExecutorAllocation": self.dynamic_executor_allocation,
            "workspaceId": self.workspace_id
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(item_dict, auth):
        """Create Item object from dictionary"""

        if 'autoScale' not in item_dict:
            item_dict['autoScale'] = item_dict['auto_scale']

        if 'dynamicExecutorAllocation' not in item_dict:
            item_dict['dynamicExecutorAllocation'] = item_dict['dynamic_executor_allocation']
        
        if 'nodeFamily' not in item_dict:
            item_dict['nodeFamily'] = item_dict['node_family']
        
        if 'nodeSize' not in item_dict:
            item_dict['nodeSize'] = item_dict['node_size']
        
        return SparkCustomPool(id=item_dict['id'], name=item_dict['name'], type=item_dict['type'], node_family=item_dict['nodeFamily'],
                                node_size=item_dict['nodeSize'], auto_scale=item_dict['autoScale'], dynamic_executor_allocation=item_dict['dynamicExecutorAllocation'],
                                workspace_id=item_dict['workspaceId'], auth=auth)


    def delete(self):
        """Delete the custom pool item"""
        # DELETE http://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools/{poolId}

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/spark/pools/{self.id}"
        for _ in range(10):
            response = requests.delete(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error deleting spark pool: {response.status_code}, {response.text}")
            break

        return response.status_code
    

    def update(self, name, node_family, node_size, auto_scale, dynamic_executor_allocation):
        """Update the custom pool item"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/spark/pools/{self.id}"
        body = {}

        if name is not None:
            body['name'] = name
        if node_family is not None:
            body['nodeFamily'] = node_family
        if node_size is not None:
            body['nodeSize'] = node_size
        if auto_scale is not None:
            body['autoScale'] = auto_scale
        if dynamic_executor_allocation is not None:
            body['dynamicExecutorAllocation'] = dynamic_executor_allocation

        if not body:
            return self
        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error updating item: {response.status_code}, {response.text}")
            break

        if name is not None:
            self.name = name
        if node_family is not None:
            self.node_family = node_family
        if node_size is not None:
            self.node_size = node_size
        if auto_scale is not None:
            self.auto_scale = auto_scale
        if dynamic_executor_allocation is not None:
            self.dynamic_executor_allocation = dynamic_executor_allocation

        return self
    
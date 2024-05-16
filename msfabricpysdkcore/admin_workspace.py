import json
from time import sleep

import requests

from msfabricpysdkcore.admin_item import AdminItem 


class AdminWorkspace:
    """Class to represent a workspace in Microsoft Fabric"""

    def __init__(self, id, type, name, state, capacity_id, auth) -> None:
        """Constructor for the Workspace class

        Args:
            id (str): The ID of the workspace
            type (str): The type of the workspace
            name (str): The name of the workspace
            state (str): The state of the workspace
            capacity_id (str): The ID of the capacity
            auth (Auth): The Auth object
        Returns:
            Workspace: The Workspace object
        """
        self.id = id
        self.type = type
        self.name = name
        self.state = state
        self.capacity_id = capacity_id
        self.auth = auth


    def __str__(self) -> str:
        """Return a string representation of the workspace object
        
        Returns:
            str: The string representation of the workspace object
        """
        dict_ = {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'state': self.state,
            'capacity_id': self.capacity_id
        }
        return json.dumps(dict_, indent=2)

    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(item_dict, auth):
        """Create Workspace object from dictionary

        Args:
            item_dict (dict): The dictionary representing the workspace
            auth (Auth): The Auth object
        Returns:
            Workspace: The Workspace object
        """
        return AdminWorkspace(
            id=item_dict['id'],
            type=item_dict['type'],
            name=item_dict['name'],
            state=item_dict['state'],
            capacity_id=item_dict['capacityId'],
            auth=auth
        )
    
    def get_workspace_access_details(self):
        """Get the access details of the workspace

        Returns:
            dict: The access details of the workspace
        """
        return self.list_workspace_access_details()
    
    def list_workspace_access_details(self):
        """Get the access details of the workspace

        Returns:
            dict: The access details of the workspace
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{self.id}/users"
           
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting workspace: {response.text}")
            break

        return json.loads(response.text)
        
    def get_item(self, item_id, type = None):
        """Get an item from the workspace
        
        Args:
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            AdminItem: The item object
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{self.id}/items/{item_id}"
        if type:
            url += f"?type={type}"
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting item: {response.text}")
            break
        item_dict = json.loads(response.text) 
        return AdminItem.from_dict(item_dict, self.auth)
    
    def list_item_access_details(self, item_id, type=None):
        """Get the access details of the item
        
        Args:
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            dict: The access details of the item
        """
        return self.get_item(item_id, type).list_item_access_details()

    def get_item_access_details(self, item_id, type=None):
        """Get the access details of the item
        
        Args:
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            dict: The access details of the item
        """
        return self.list_item_access_details(item_id, type)
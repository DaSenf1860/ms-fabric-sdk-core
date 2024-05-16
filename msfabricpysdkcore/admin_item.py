import json
from time import sleep

import requests 


class AdminItem:
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, type, name, workspace_id, state, description, last_updated_date, capacity_id, creator_principal, auth) -> None:
        """Constructor for the Item class
        
        Args:
            id (str): The ID of the item
            type (str): The type of the item
            name (str): The name of the item
            workspace_id (str): The ID of the workspace
            state (str): The state of the item
            description (str): The description of the item
            last_updated_date (str): The last updated date of the item
            capacity_id (str): The ID of the capacity
            creator_principal (dict): The creator principal of the item
            auth (Auth): The Auth object
        Returns:
            Item: The Item object
        """
        self.id = id
        self.type = type
        self.name = name
        self.workspace_id = workspace_id
        self.state = state
        self.description = description
        self.last_updated_date = last_updated_date
        self.capacity_id = capacity_id
        self.creator_principal = creator_principal
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
            'workspace_id': self.workspace_id,
            'state': self.state,
            'description': self.description,
            'last_updated_date': self.last_updated_date,
            'capacity_id': self.capacity_id,
            'creator_principal': self.creator_principal
        }
        return json.dumps(dict_, indent=2)

    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(item_dict, auth):
        """Create Item object from dictionary
        
        Args:
            item_dict (dict): The dictionary containing the item information
            auth (Auth): The Auth object
        Returns:
            Item: The Item object"""
        return AdminItem(
            id = item_dict['id'],
            type = item_dict['type'],
            name = item_dict['name'],
            workspace_id = item_dict['workspaceId'],
            state = item_dict['state'],
            description = item_dict.get('description', None),
            last_updated_date = item_dict['lastUpdatedDate'],
            capacity_id = item_dict['capacityId'],
            creator_principal = item_dict['creatorPrincipal'],
            auth = auth
        )
    
    def get_item_access_details(self, type=None):
        """Get the access details of the item
        
        Returns:
            dict: The access details of the item"""
        return self.list_item_access_details(type)
        
    def list_item_access_details(self, type=None):
        """Get the access details of the item
        
        Returns:
            dict: The access details of the item"""
        
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{self.workspace_id}/items/{self.id}/users"

        if type:
            url += f"?type={self.type}"
        
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
        
        return json.loads(response.text)
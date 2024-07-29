import json
from time import sleep

from msfabricpysdkcore.admin_item import AdminItem 
from msfabricpysdkcore.adminapi import FabricClientAdmin


class AdminWorkspace:
    """Class to represent a workspace in Microsoft Fabric"""

    def __init__(self, id, type, name, state, capacity_id, admin_client:FabricClientAdmin) -> None:
        """Constructor for the Workspace class

        Args:
            id (str): The ID of the workspace
            type (str): The type of the workspace
            name (str): The name of the workspace
            state (str): The state of the workspace
            capacity_id (str): The ID of the capacity
            admin_client (FabricClientAdmin): The FabricClientAdmin object
        Returns:
            Workspace: The Workspace object
        """
        self.id = id
        self.type = type
        self.name = name
        self.state = state
        self.capacity_id = capacity_id
        self.admin_client = admin_client


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
    
    def from_dict(item_dict, admin_client):
        """Create Workspace object from dictionary

        Args:
            item_dict (dict): The dictionary representing the workspace
            admin_client (FabricClientAdmin): The FabricClientAdmin object
        Returns:
            Workspace: The Workspace object
        """
        return AdminWorkspace(
            id=item_dict['id'],
            type=item_dict['type'],
            name=item_dict['name'],
            state=item_dict['state'],
            capacity_id=item_dict['capacityId'],
            admin_client=admin_client
        )
        
    def list_workspace_access_details(self):
        """Get the access details of the workspace

        Returns:
            dict: The access details of the workspace
        """
        return self.admin_client.list_workspace_access_details(self.id)
    
    # Items

    def get_item(self, item_id, type = None):
        """Get an item from the workspace
        
        Args:
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            AdminItem: The item object
        """
        return self.admin_client.get_item(self.id, item_id, type)
    
    def list_item_access_details(self, item_id, type=None):
        """Get the access details of the item
        
        Args:
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            dict: The access details of the item
        """
        return self.admin_client.list_item_access_details(self.id, item_id, type)
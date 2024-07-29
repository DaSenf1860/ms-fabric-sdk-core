import json
from msfabricpysdkcore.adminapi import FabricClientAdmin


class AdminItem:
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, type, name, workspace_id, state, description, last_updated_date, capacity_id, creator_principal, admin_client: FabricClientAdmin) -> None:
        """Constructor for the Item class
        
        Args:
            id (str): The ID of the item
            type (str): The type of the item
            name (str): The name of the item
            workspace_id (str): The ID of the workspace to which the item belongs
            state (str): The state of the item
            description (str): The description of the item
            last_updated_date (str): The date when the item was last updated
            capacity_id (str): The
            creator_principal (str): The principal who created the item
            admin_client (FabricClientAdmin): The FabricClientAdmin object
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
    
    def from_dict(item_dict, admin_client):
        """Create Item object from dictionary
        
        Args:
            item_dict (dict): The dictionary containing the item details
            admin_client (FabricClientAdmin): The FabricClientAdmin object
        Returns:
            AdminItem: The AdminItem object
        """
        return AdminItem(
            id = item_dict['id'],
            type = item_dict['type'],
            name = item_dict.get('name', None),
            workspace_id = item_dict['workspaceId'],
            state = item_dict['state'],
            description = item_dict.get('description', None),
            last_updated_date = item_dict['lastUpdatedDate'],
            capacity_id = item_dict['capacityId'],
            creator_principal = item_dict.get('creatorPrincipal', None),
            admin_client = admin_client
        )
            
    def list_item_access_details(self, type=None):
        """Get the access details of the item
        
        Returns:
            dict: The access details of the item"""
        
        return self.admin_client.list_item_access_details(self.workspace_id, self.id, type)
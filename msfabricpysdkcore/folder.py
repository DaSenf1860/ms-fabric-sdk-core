import json 

from msfabricpysdkcore.coreapi import FabricClientCore

class Folder:
    """Class to represent a folder in Microsoft Fabric"""

    def __init__(self, id, display_name, workspace_id, core_client: FabricClientCore, parent_folder_id) -> None:
        
        self.id = id
        self.display_name = display_name
        self.parent_folder_id = parent_folder_id
        self.workspace_id = workspace_id
        
        self.core_client = core_client

    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            'id': self.id,
            'display_name': self.display_name,
            'parent_folder_id': self.parent_folder_id,
            'workspace_id': self.workspace_id,
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(folder_dict, core_client):
        """Create Folder object from dictionary"""
        
        return Folder(id=folder_dict['id'], display_name=folder_dict['displayName'], workspace_id=folder_dict['workspaceId'],
                       parent_folder_id=folder_dict.get('parentFolderId', ""), core_client=core_client)

    def delete(self):
        """Delete the folder"""
        return self.core_client.delete_folder(workspace_id=self.workspace_id, folder_id=self.id)
    
    def get(self):
        """Get the folder"""
        returned_folder = self.core_client.get_folder(workspace_id=self.workspace_id, folder_id=self.id)
        self.display_name = returned_folder.display_name
        self.parent_folder_id = returned_folder.parent_folder_id
        self.workspace_id = returned_folder.workspace_id
        return returned_folder
    
    def move(self, target_folder_id = None):
        """Move a folder
        Args:
            target_folder_id (str): The ID of the target folder
        Returns:
            dict: The moved folder
        """
        moved_folder =  self.core_client.move_folder(folder_id=self.id, target_folder_id=target_folder_id)
        self.id = moved_folder.id
        self.display_name = moved_folder.display_name
        self.parent_folder_id = moved_folder.parent_folder_id
        self.workspace_id = moved_folder.workspace_id

        return moved_folder
    
    def update(self, display_name = None):
        """Update the folder"""
        updated_folder = self.core_client.update_folder(workspace_id=self.workspace_id, folder_id=self.id, display_name=display_name)
        self.display_name = updated_folder.display_name
        self.parent_folder_id = updated_folder.parent_folder_id
        self.workspace_id = updated_folder.workspace_id
        return updated_folder
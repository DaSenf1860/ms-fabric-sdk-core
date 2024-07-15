import json 
from msfabricpysdkcore.coreapi import FabricClientCore

class OneLakeShortcut:
    """Class to represent a onelake shortcut in Microsoft Fabric"""

    def __init__(self, name, path, workspace_id, item_id, target,
                  core_client: FabricClientCore) -> None:
        
        self.name = name
        self.path = path
        self.target = target
        self.item_id = item_id
        self.workspace_id = workspace_id

        self.core_client = core_client

    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            'name': self.name,
            'path': self.path,
            'target': self.target,
            'item_id': self.item_id,
            'workspace_id': self.workspace_id,
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(short_dict, core_client):
        """Create OneLakeShortCut object from dictionary"""
        return OneLakeShortcut(name=short_dict['name'],
                               path=short_dict['path'], 
                               target=short_dict['target'], 
                               item_id=short_dict['itemId'], 
                               workspace_id=short_dict['workspaceId'], 
                               core_client=core_client)
    
    def delete(self):
        """Delete the shortcut"""
        return self.core_client.delete_shortcut(workspace_id=self.workspace_id, item_id=self.item_id, path=self.path,
                                                name=self.name)
import json 
import requests
from time import sleep

class OneLakeShortcut:
    """Class to represent a onelake shortcut in Microsoft Fabric"""

    def __init__(self, name, path, workspace_id, item_id, target,
                  auth) -> None:
        
        self.name = name
        self.path = path
        self.target = target
        self.item_id = item_id
        self.workspace_id = workspace_id

        self.user_auth = auth

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
    
    def from_dict(short_dict, auth):
        """Create OneLakeShortCut object from dictionary"""
        return OneLakeShortcut(name=short_dict['name'],
                               path=short_dict['path'], 
                               target=short_dict['target'], 
                               item_id=short_dict['itemId'], 
                               workspace_id=short_dict['workspaceId'], 
                               auth=auth)
    
    def delete(self):
        """Delete the shortcut"""

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.item_id}/shortcuts/{self.path}/{self.name}"
        for _ in range(10):
            response = requests.delete(url=url, headers=self.user_auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error deleting shortcut: {response.text}")
            break

        return response.status_code
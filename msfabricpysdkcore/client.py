import requests
import json
import os
from time import sleep

from msfabricpysdkcore.capacity import Capacity
from msfabricpysdkcore.workspace import Workspace
from msfabricpysdkcore.auth import FabricAuthClient, FabricServicePrincipal

class FabricClientCore():
    """FabricClientCore class to interact with Fabric API"""

    def __init__(self, tenant_id = None, client_id = None, client_secret = None) -> None:
        """Initialize FabricClientCore object"""
        self.tenant_id = tenant_id if tenant_id else os.getenv("FABRIC_TENANT_ID")
        self.client_id = client_id if client_id else os.getenv("FABRIC_CLIENT_ID")
        self.client_secret = client_secret if client_secret else os.getenv("FABRIC_CLIENT_SECRET")

        if self.client_id is None or self.client_secret is None or self.tenant_id is None:
            self.auth = FabricAuthClient()
        else:
            self.auth = FabricServicePrincipal(tenant_id = self.tenant_id,
                                               client_id = self.client_id, 
                                               client_secret = self.client_secret)

        self.scope = "https://api.fabric.microsoft.com/.default"


    def list_workspaces(self, continuationToken = None):
        """List all workspaces in the tenant"""

        url = "https://api.fabric.microsoft.com/v1/workspaces"
        if continuationToken:
            url = f"{url}?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error listing workspaces: {response.status_code},  {response.text}")
            break
        resp_dict = json.loads(response.text)
        ws_list = resp_dict["value"]
        ws_list = [Workspace.from_dict(ws, auth=self.auth) for ws in ws_list]
      
        if "continuationToken" in resp_dict:
            ws_list_next = self.list_workspaces(continuationToken=resp_dict["continuationToken"])
            ws_list.extend(ws_list_next)

        return ws_list
    
    def get_workspace_by_name(self, name):
        """Get workspace by name"""
        ws_list = self.list_workspaces()
        for ws in ws_list:
            if ws.display_name == name:
                return ws
            
    def get_workspace_by_id(self, id):
        """Get workspace by id"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{id}"


        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting workspace: {response.status_code} {response.text}")
            break
        ws_dict = json.loads(response.text)
        ws = Workspace.from_dict(ws_dict, auth=self.auth)

        return ws

    
    def get_workspace(self, id = None, name = None):
        """Get workspace by id or name"""
        if id:
            return self.get_workspace_by_id(id)
        if name:
            return self.get_workspace_by_name(name)
        raise ValueError("Either id or name must be provided")
        
    def get_workspace_role_assignments(self, workspace_id):
        """Get role assignments for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_role_assignments()
    
    def create_workspace(self, display_name, capacity_id = None, description = None, exists_ok = True):
        """Create a workspace"""
        body = dict()
        body["displayName"] = display_name
        if capacity_id:
            body["capacityId"] = capacity_id
        if description:
            body["description"] = description
        
        url = "https://api.fabric.microsoft.com/v1/workspaces"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            ws_dict = json.loads(response.text)
            if response.status_code not in (201, 429):
                if "errorCode" in ws_dict and ws_dict["errorCode"] == "WorkspaceNameAlreadyExists" and exists_ok:
                    return self.get_workspace_by_name(display_name)
                else:
                    print(response.status_code)
                    print(response.text)
                    raise Exception(f"Error creating workspace: {response.text}")
            break

        ws = Workspace.from_dict(ws_dict, auth=self.auth)
        return ws
    
    def delete_workspace(self, workspace_id = None, display_name = None):
        """Delete a workspace"""
        if workspace_id is None and display_name is None:
            raise ValueError("Either workspace_id or display_name must be provided")
        ws = self.get_workspace(id = workspace_id, name = display_name)
        reponse = ws.delete()
        return reponse
    
    def add_workspace_role_assignment(self, workspace_id, role, principal):
        """Add a role assignment to a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.add_role_assignment(role, principal)
    
    def delete_workspace_role_assignment(self, workspace_id, principal_id):
        """Delete a role assignment from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_role_assignment(principal_id)
    
    def update_workspace(self, workspace_id, display_name = None, description = None):
        """Update a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update(display_name, description)
    
    def update_workspace_role_assignment(self, workspace_id, role, principal_id):
        """Update a role assignment for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_role_assignment(role, principal_id)

    def assign_to_capacity(self, workspace_id, capacity_id):
        """Assign a workspace to a capacity"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.assign_to_capacity(capacity_id)
    
    def unassign_from_capacity(self, workspace_id):
        """Unassign a workspace from a capacity"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.unassign_from_capacity()
 
    def list_capacities(self, continuationToken = None):
        """List all capacities in the tenant"""
        url = "https://api.fabric.microsoft.com/v1/capacities"

        if continuationToken:
            url = f"{url}?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error listing capacities: {response.text}")
            break

        resp_dict = json.loads(response.text)
        items = resp_dict["value"]

        if "continuationToken" in resp_dict:
            cap_list_next = self.list_capacities(continuationToken=resp_dict["continuationToken"])
            items.extend(cap_list_next)

        items = json.loads(response.text)["value"]
        items = [Capacity.from_dict(i) for i in items]
        return items

    
    def create_item(self, workspace_id, display_name, type, definition = None, description = None):
        """Create an item in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        
        return ws.create_item(display_name = display_name,
                              type = type,
                              definition = definition,
                              description = description)

    def get_item(self, workspace_id = None, 
                  item_id = None, workspace_name = None, item_name = None, item_type = None):
        """Get an item from a workspace"""
        ws = self.get_workspace(id = workspace_id, name = workspace_name)
        return ws.get_item(item_id = item_id, item_name = item_name, item_type = item_type)

    def delete_item(self, workspace_id, item_id):
        """Delete an item from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_item(item_id)

    def list_items(self, workspace_id):
        """List items in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_items()
    
    def get_item_definition(self, workspace_id, item_id):
        """Get the definition of an item"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_item_definition(item_id)
    
    def update_item(self, workspace_id, item_id, display_name = None, description = None):
        """Update an item in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_item(item_id).update(display_name, description)
    
    def update_item_definition(self, workspace_id, item_id, definition):
        """Update the definition of an item"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).update_definition(definition=definition)
    
    def create_shortcut(self, workspace_id, item_id, path, name, target):
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).create_shortcut(path=path, name=name, target=target)
    
    def get_shortcut(self, workspace_id, item_id, path, name):
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).get_shortcut(path=path, name=name)
    
    def delete_shortcut(self, workspace_id, item_id, path, name):
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).delete_shortcut(path=path, name=name)
      
    def get_item_job_instance(self, workspace_id, item_id, job_instance_id):
        """Get a job instance for an item"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).get_item_job_instance(job_instance_id=job_instance_id)
    
    def run_on_demand_item_job(self, workspace_id, item_id, job_type, execution_data = None):
        """Run an on demand job for an item"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).run_on_demand_item_job(job_type=job_type, execution_data=execution_data)
    
    def cancel_item_job_instance(self, workspace_id, item_id, job_instance_id):
        """Cancel a job instance for an item"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.get_item(item_id=item_id).get_item_job_instance(job_instance_id=job_instance_id).cancel()
    
    def commit_to_git(self, workspace_id,mode, comment=None, items=None, workspace_head=None):
        """Commit changes to git"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.commit_to_git(mode=mode, comment=comment, items=items, workspace_head=workspace_head)
    
    def git_connect(self, workspace_id, git_provider_details):
        """Connect to git"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.git_connect(git_provider_details=git_provider_details)
    
    def git_disconnect(self, workspace_id):
        """Disconnect from git"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.git_disconnect()
    
    def git_get_connection(self, workspace_id):
        """Get git connection details"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.git_get_connection()
    
    def git_get_status(self, workspace_id):
        """Get git status"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.git_get_status()
    
    def git_initialize_connection(self, workspace_id, initialization_strategy):
        """Initialize git"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.git_initialize_connection(initialization_strategy=initialization_strategy)
    
    def update_from_git(self, workspace_id, remote_commit_hash, conflict_resolution = None, options = None, workspace_head = None):
        """Update workspace from git"""
        ws = self.get_workspace_by_id(id=workspace_id)
        return ws.update_from_git(remote_commit_hash=remote_commit_hash,
                                  conflict_resolution=conflict_resolution, 
                                  options=options, 
                                  workspace_head=workspace_head)
    
    def get_capacity(self, capacity_id = None, capacity_name = None):
        """Get a capacity
        
        Args:
            capacity_id (str): The ID of the capacity
            capacity_name (str): The name of the capacity
            
        Returns:
            Capacity: The capacity object
            
        Raises:
            ValueError: If no capacity is found
        """
        if capacity_id is None and capacity_name is None:
            raise ValueError("Either capacity_id or capacity_name must be provided")
        caps = self.list_capacities()
        for cap in caps:
            if capacity_id and cap.id == capacity_id:
                return cap
            if capacity_name and cap.display_name == capacity_name:
                return cap
        raise ValueError("No capacity found") 
    
    def list_tables(self, workspace_id, item_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_tables(item_id=item_id)
    
    def load_table(self, workspace_id, item_id, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.load_table(item_id, table_name, path_type, relative_path,
                    file_extension, format_options,
                    mode, recursive, wait_for_completion)
import json 
import requests
from time import sleep
from msfabricpysdkcore.item import Item
from msfabricpysdkcore.lakehouse import Lakehouse
from msfabricpysdkcore.long_running_operation import check_long_running_operation
from msfabricpysdkcore.otheritems import SparkJobDefinition
from msfabricpysdkcore.otheritems import Warehouse

class Workspace:
    """Class to represent a workspace in Microsoft Fabric"""

    def __init__(self, id, display_name, description, type, auth, capacity_id = None) -> None:
        self.id = id
        self.display_name = display_name
        self.description = description
        self.type = type
        self.capacity_id = capacity_id

        self.auth = auth
        
    
    def from_dict(dict,  auth):
        """Create a Workspace object from a dictionary"""
        return Workspace(id=dict['id'], display_name=dict['displayName'], description=dict['description'], type=dict['type'], capacity_id=dict.get('capacityId', None),
                         auth=auth)
    
    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            'id': self.id,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.type,
            'capacity_id': self.capacity_id
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_role_assignments(self):
        """Get role assignments for the workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/roleAssignments"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting role assignments: {response.text}")
            break

        return json.loads(response.text)
    
    def delete(self):
        """Delete the workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}"

        for _ in range(10):
            response = requests.delete(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error deleting workspace: {response.text}")
            break

        return response.status_code
    
    # function to add workpace role assignment
    def add_role_assignment(self, role, principal):
        """Add a role assignment to the workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/roleAssignments"

        payload = {
            'principal': principal,
            'role': role
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), data=json.dumps(payload))
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error adding role assignments: {response.text}")
            break

        return response.status_code
    

    def delete_role_assignment(self, principal_id):
        """Delete a role assignment from the workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/roleAssignments/{principal_id}"

        for _ in range(10):
            response = requests.delete(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error deleting role assignments: {response.text}")
            break

        
        return response.status_code
    
    def update(self, display_name = None, description = None):
        """Update the workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}"

        body = dict()
        if display_name:
            body["displayName"] = display_name
        if description:
            body["description"] = description


        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error updating workspace: {response.text}")
            break

        assert response.status_code == 200
        if display_name:
            self.display_name = display_name
        if description:
            self.description = description

        return self

    def update_role_assignment(self, role, principal_id):
        """Update a role assignment in the workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/roleAssignments/{principal_id}"
        body = {
            'role': role
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
                raise Exception(f"Error updating role assignments: {response.text}")
            break

        return response.status_code
    
    def assign_to_capacity(self, capacity_id):
        """Assign the workspace to a capacity"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/assignToCapacity"

        body = {
            'capacityId': capacity_id
        }


        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error assigning capacity: {response.text}")
            break

        assert response.status_code == 202
        self.capacity_id = capacity_id
        return response.status_code
    
    def unassign_from_capacity(self):
        """Unassign the workspace from a capacity"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/unassignFromCapacity"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue

            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error unassigning capacity: {response.text}")
            break

        assert response.status_code == 202
        self.capacity_id = None
        return response.status_code
    
    def create_item(self, display_name, type, definition = None, description = None):
        """Create an item in a workspace"""

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/items"

        body = {
            'displayName': display_name,
            'type': type,
            'definition': definition,
            'description': description
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (201, 202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error creating item: {response.text}")
            break

        item_dict = json.loads(response.text)
        if item_dict is None:
            print("Item not returned by API, trying to get it by name")
            return self.get_item_by_name(display_name, type)    

        if item_dict["type"] == "Lakehouse":
            return self.get_lakehouse(item_dict["id"])
        if item_dict["type"] == "Warehouse":
            return self.get_warehouse(item_dict["id"])
        if item_dict["type"] == "SparkJobDefinition":
            return self.get_spark_job_definition(item_dict["id"])
        
        item_obj = Item.from_dict(item_dict, auth=self.auth)
        if item_obj.type in ["Notebook", "Report", "SemanticModel"]:
            item_obj.get_definition()
        return item_obj

    def get_item_by_name(self, item_name, item_type):
        """Get an item from a workspace by name"""
        ws_items = self.list_items(with_properties=False)
        for item in ws_items:
            if item.display_name == item_name and item.type == item_type:
                return self.get_item(item.id, item_type)    


    def get_item_internal(self, url):

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
        return item_dict

    def get_lakehouse(self, lakehouse_id = None, lakehouse_name = None):
        """Get a lakehouse from a workspace"""

        if lakehouse_id is None and lakehouse_name is not None:
            return self.get_item_by_name(lakehouse_name, "Lakehouse")
        elif lakehouse_id is None:
            raise Exception("lakehouse_id or the lakehouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/lakehouses/{lakehouse_id}"

        item_dict = self.get_item_internal(url)
        return Lakehouse.from_dict(item_dict, auth=self.auth)
    
    def get_warehouse(self, warehouse_id = None, warehouse_name = None):
        """Get a warehouse from a workspace"""
        if warehouse_id is None and warehouse_name is not None:
            return self.get_item_by_name(warehouse_name, "Warehouse")
        elif warehouse_id is None:
            raise Exception("warehouse_id or the warehouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/warehouses/{warehouse_id}"

        item_dict = self.get_item_internal(url)
        return Warehouse.from_dict(item_dict, auth=self.auth)

    def get_spark_job_definition(self, spark_job_definition_id = None, spark_job_definition_name = None):
        """Get a spark job definition from a workspace"""
        if spark_job_definition_id is None and spark_job_definition_name is not None:
            return self.get_item_by_name(spark_job_definition_name, "SparkJobDefinition")
        elif spark_job_definition_id is None:
            raise Exception("spark_job_definition_id or the spark_job_definition_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/sparkjobdefinitions/{spark_job_definition_id}"

        item_dict = self.get_item_internal(url)
        sjd_obj =  SparkJobDefinition.from_dict(item_dict, auth=self.auth)
        sjd_obj.get_definition()
        return sjd_obj

    def get_item(self, item_id = None, item_name = None, item_type = None):
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}
        """Get an item from a workspace"""
        if item_type:
            if item_type.lower() == "lakehouse":
                return self.get_lakehouse(item_id, item_name)
            if item_type.lower() == "warehouse":
                return self.get_warehouse(item_id, item_name)
            if item_type.lower() == "sparkjobdefinition":
                return self.get_spark_job_definition(item_id, item_name)
                
        if item_id is None and item_name is not None and item_type is not None:
            return self.get_item_by_name(item_name, item_type)
        elif item_id is None:
            raise Exception("item_id or the combination item_name + item_type is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/items/{item_id}"

        item_dict = self.get_item_internal(url)
        if item_dict["type"] == "Lakehouse":
            return self.get_lakehouse(item_dict["id"])
        if item_dict["type"] == "Warehouse":
            return self.get_warehouse(item_dict["id"])
        if item_dict["type"] == "SparkJobDefinition":
            return self.get_spark_job_definition(item_dict["id"])
        

        item_obj = Item.from_dict(item_dict, auth=self.auth)
        if item_obj.type in ["Notebook", "Report", "SemanticModel"]:
            item_obj.get_definition()
        return item_obj


    def delete_item(self, item_id):
        """Delete an item from a workspace"""
        return self.get_item(item_id).delete()
  

    def get_item_object_w_properties(self, item_list):

        new_item_list = []
        for item in item_list:
            if item["type"] == "Lakehouse":
                item = self.get_lakehouse(item["id"])
            elif item["type"] == "Warehouse":
                item = self.get_warehouse(item["id"])
            elif item["type"] == "SparkJobDefinition":
                item = self.get_spark_job_definition(item["id"])
            else:
                item = Item.from_dict(item, auth=self.auth)
                if item.type in ["Notebook", "Report", "SemanticModel"]:
                    item.get_definition()
            new_item_list.append(item)
        return new_item_list

    def list_items(self, with_properties = False, continuationToken = None):
        """List items in a workspace"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/items"

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
                raise Exception(f"Error listing items: {response.text}")
            break
        
        resp_dict = json.loads(response.text)
        items = resp_dict["value"]
        if with_properties:
            items = self.get_item_object_w_properties(items)
        else:
            items = [Item.from_dict(item, auth=self.auth) for item in items]

        if "continuationToken" in resp_dict:
            item_list_next = self.list_items(with_properties=with_properties, 
                                             continuationToken=resp_dict["continuationToken"])
            items.extend(item_list_next)

        return items
    
    def get_item_definition(self, item_id):
        """Get the definition of an item from a workspace"""
        return self.get_item(item_id).get_definition()
    
    def update_item(self, item_id, display_name = None, description = None):
        """Update an item in a workspace"""
        return self.get_item(item_id=item_id).update(display_name=display_name, description=description)
    
    def update_item_definition(self, item_id, definition):
        """Update the definition of an item in a workspace"""
        return self.get_item(item_id=item_id).update_definition(definition=definition)
    
    def create_shortcut(self, item_id, path, name, target):
        return self.get_item(item_id=item_id).create_shortcut(path=path, name=name, target=target)
    
    def get_shortcut(self, item_id, path, name):
        return self.get_item(item_id=item_id).get_shortcut(path=path, name=name)
    
    def delete_shortcut(self, item_id, path, name):
        return self.get_item(item_id=item_id).delete_shortcut(path=path, name=name)
    
    def run_on_demand_item_job(self, item_id, job_type, execution_data = None):
        return self.get_item(item_id=item_id).run_on_demand_job(job_type=job_type, execution_data = execution_data)
    
    def get_item_job_instance(self, item_id, job_instance_id):
        return self.get_item(item_id=item_id).get_item_job_instance(job_instance_id=job_instance_id)
    
    def cancel_item_job_instance(self, item_id, job_instance_id):
        return self.get_item(item_id=item_id).cancel_item_job_instance(job_instance_id=job_instance_id)
    
    def git_connect(self, git_provider_details):
        """Connect git"""
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/connect
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/connect"

        payload = {
            'gitProviderDetails': git_provider_details
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=payload)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 204, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error connecting git: {response.text}")
            break
        return response.status_code

    def git_disconnect(self):
        """Disconnect git"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/disconnect"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 204, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error disconnecting git: {response.text}")
            break
        return response.status_code

    def git_initialize_connection(self, initialization_strategy):
    #        POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/initializeConnection
        """Initialize git connection"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/initializeConnection"

        body = {'initializeGitConnectionRequest':initialization_strategy}
            
        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error initializing connection: {response.text}")
            break
        return response.status_code
    
    def git_get_status(self):
        """Get git connection status"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/status"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting git connection status: {response.text}")
            break
        return json.loads(response.text)
    
    def git_get_connection(self):
        """Get git connection info"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/connection"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting git connection info: {response.text}")
            break
        return json.loads(response.text)
    
    def commit_to_git(self, mode, comment=None, items=None, workspace_head=None):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/commitToGit

        """Commit to git"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/commitToGit"

        body = {
            'mode': mode
        }

        if comment:
            body['comment'] = comment
        if items:
            body['items'] = items
        if workspace_head:
            body['workspaceHead'] = workspace_head

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)
            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error committing to git: {response.text}")
            break

        return response.status_code

    def update_from_git(self, remote_commit_hash, conflict_resolution = None, options = None, workspace_head = None):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/updateFromGit
        """Update from git"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/git/updateFromGit"

        body = {
            "remoteCommitHash" : remote_commit_hash
        }

        if conflict_resolution:
            body['conflictResolution'] = conflict_resolution
        if options:
            body['options'] = options
        if workspace_head:
            body['workspaceHead'] = workspace_head

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                check_long_running_operation( response.headers, self.auth)

            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error updating from git: {response.text}")
            break

        return response.status_code
    
    def list_tables(self, item_id):
        return self.get_item(item_id=item_id).list_tables()
    
    def load_table(self, item_id, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        return self.get_item(item_id).load_table(table_name, path_type, relative_path,
                    file_extension, format_options,
                    mode, recursive, wait_for_completion)

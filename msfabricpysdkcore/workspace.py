import json 
import requests
from time import sleep
from msfabricpysdkcore.item import Item
from msfabricpysdkcore.lakehouse import Lakehouse
from msfabricpysdkcore.environment import Environment
from msfabricpysdkcore.long_running_operation import check_long_running_operation
from msfabricpysdkcore.otheritems import DataPipeline, Eventstream, KQLDatabase, KQLQueryset, SparkJobDefinition
from msfabricpysdkcore.otheritems import Eventhouse, MLExperiment, MLModel, Notebook, Report, SemanticModel, Warehouse
from msfabricpysdkcore.spark_custom_pool import SparkCustomPool


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
                raise Exception(f"Error updating workspace: {response.status_code}, {response.text}")
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
    
    def get_item_specific(self, item_dict):
        if item_dict["type"] == "DataPipeline":
            return self.get_data_pipeline(item_dict["id"])
        if item_dict["type"] == "Eventstream":
            return self.get_eventstream(item_dict["id"])
        if item_dict["type"] == "Eventhouse":
            return self.get_eventhouse(item_dict["id"])
        if item_dict["type"] == "KQLDatabase":
            return self.get_kql_database(item_dict["id"])
        if item_dict["type"] == "KQLQueryset":
            return self.get_kql_queryset(item_dict["id"])
        if item_dict["type"] == "Lakehouse":
            return self.get_lakehouse(item_dict["id"])
        if item_dict["type"] == "MLExperiment":
            return self.get_ml_experiment(item_dict["id"])
        if item_dict["type"] == "MLModel":
            return self.get_ml_model(item_dict["id"])
        if item_dict["type"] == "Notebook":
            return self.get_notebook(item_dict["id"])
        if item_dict["type"] == "Report":
            return self.get_report(item_dict["id"])
        if item_dict["type"] == "SemanticModel":
            return self.get_semantic_model(item_dict["id"])
        if item_dict["type"] == "SparkJobDefinition":
            return self.get_spark_job_definition(item_dict["id"])
        if item_dict["type"] == "Warehouse":
            return self.get_warehouse(item_dict["id"])
        if item_dict["type"] == "Environment":
            return self.get_environment(item_dict["id"])

        item_obj = Item.from_dict(item_dict, auth=self.auth)
        return item_obj

    def create_item(self, display_name, type, definition = None, description = None, **kwargs):
        """Create an item in a workspace"""

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/items"
        body = {
            'displayName': display_name,
            'type': type
        }

        if definition:
            body['definition'] = definition
        if description:
            body['description'] = description

        if type in ["dataPipelines",
                    "environments",
                    "eventhouses",
                    "eventstreams",
                    "kqlDatabases",
                    "lakehouses",
                    "mlExperiments", 
                    "mlModels", 
                    "notebooks", 
                    "reports", 
                    "semanticModels", 
                    "sparkJobDefinitions", 
                    "warehouses"]:
            
            if type == "kqlDatabases":
                if "creation_payload" not in kwargs:
                    raise Exception("creation_payload is required for KQLDatabase")
                body["creationPayload"] = kwargs["creation_payload"]
            
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/{type}"
            body.pop('type')


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
            item = None
            i = 0

            type_mapping = {"dataPipelines": "DataPipeline",
                            "environments": "Environment",
                            "eventhouses": "Eventhouse",
                            "eventstreams": "Eventstream",
                            "kqlDatabases": "KQLDatabase",
                            "lakehouses": "Lakehouse", 
                            "mlExperiments": "MLExperiment",
                            "mlModels": "MLModel", 
                            "notebooks": "Notebook", 
                            "reports": "Report", 
                            "semanticModels": "SemanticModel",
                            "sparkJobDefinitions": "SparkJobDefinition", 
                            "warehouses": "Warehouse"
                            }
            
            if type in type_mapping.keys():
                type = type_mapping[type]
            while item is None and i < 12:
                item = self.get_item_by_name(display_name, type)
                if item is not None:
                    return item
                print("Item not found, waiting 5 seconds")
                sleep(5)
                i += 1

            print("Item not found after 1 minute, returning None")
            return None
                
        return self.get_item_specific(item_dict)
         

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
    
    def get_item(self, item_id = None, item_name = None, item_type = None):
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}
        """Get an item from a workspace"""
        if item_type:
            if item_type.lower() == "datapipeline":
                return self.get_data_pipeline(item_id, item_name)
            if item_type.lower() == "eventstream":
                return self.get_eventstream(item_id, item_name)
            if item_type.lower() == "kqldatabase":
                return self.get_kql_database(item_id, item_name)
            if item_type.lower() == "kqlqueryset":
                return self.get_kql_queryset(item_id, item_name)
            if item_type.lower() == "lakehouse":
                return self.get_lakehouse(item_id, item_name)
            if item_type.lower() == "mlmodel":
                return self.get_ml_model(item_id, item_name)
            if item_type.lower() == "mlexperiment":
                return self.get_ml_experiment(item_id, item_name)
            if item_type.lower() == "notebook":
                return self.get_notebook(item_id, item_name)
            if item_type.lower() == "report":
                return self.get_report(item_id, item_name)
            if item_type.lower() == "semanticmodel":
                return self.get_semantic_model(item_id, item_name)
            if item_type.lower() == "sparkjobdefinition":
                return self.get_spark_job_definition(item_id, item_name)
            if item_type.lower() == "warehouse":
                return self.get_warehouse(item_id, item_name)
                
        if item_id is None and item_name is not None and item_type is not None:
            return self.get_item_by_name(item_name, item_type)
        elif item_id is None:
            raise Exception("item_id or the combination item_name + item_type is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/items/{item_id}"

        item_dict = self.get_item_internal(url)

        return self.get_item_specific(item_dict)

    def delete_item(self, item_id):
        """Delete an item from a workspace"""
        return self.get_item(item_id).delete()
  

    def get_item_object_w_properties(self, item_list):

        new_item_list = []
        for item in item_list:
            item_ = self.get_item_specific(item)
            new_item_list.append(item_)
        return new_item_list

    def list_items(self, with_properties = False, continuationToken = None, type = None):
        """List items in a workspace"""

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/items"
        
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/{type}"
        

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
    
    def get_item_definition(self, item_id, type = None, format = None):
        """Get the definition of an item from a workspace"""
        return self.get_item(item_id).get_definition(type=type, format=format)
    
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
    
    def list_tables(self, lakehouse_id):
        """List tables in a workspace"""
        return self.get_lakehouse(lakehouse_id=lakehouse_id).list_tables()
    
    def load_table(self, lakehouse_id, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        
        return self.get_lakehouse(lakehouse_id=lakehouse_id).load_table(table_name, path_type, relative_path,
                    file_extension, format_options,
                    mode, recursive, wait_for_completion)
    
    def run_on_demand_table_maintenance(self, lakehouse_id, execution_data, 
                                        job_type = "TableMaintenance", wait_for_completion = True):
        """Run on demand table maintenance"""
        return self.get_lakehouse(lakehouse_id=lakehouse_id).run_on_demand_table_maintenance(execution_data,
                                                                                              job_type, 
                                                                                              wait_for_completion)

    def list_dashboards(self):
        """List dashboards in a workspace"""
        return self.list_items(type="dashboards")
    
    def list_datamarts(self):
        """List datamarts in a workspace"""
        return self.list_items(type="datamarts")
    
    def list_paginated_reports(self):
        """List paginated reports in a workspace"""
        return self.list_items(type="paginatedReports")

    def list_sql_endpoints(self):
        """List sql endpoints in a workspace"""
        return self.list_items(type="sqlEndpoints")

    def list_mirrored_warehouses(self):
        """List mirrored warehouses in a workspace"""
        return self.list_items(type="mirroredWarehouses")
    
    # datapipelines

    def create_data_pipeline(self, display_name, definition = None, description = None):
        """Create a data pipeline in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "dataPipelines",
                                definition = definition,
                                description = description)

    def list_data_pipelines(self, with_properties = False):
        """List data pipelines in a workspace"""
        return self.list_items(type="dataPipelines", with_properties=with_properties)
    
    def get_data_pipeline(self, data_pipeline_id = None, data_pipeline_name = None):
        """Get a data pipeline from a workspace"""
        if data_pipeline_id is None and data_pipeline_name is not None:
            return self.get_item_by_name(data_pipeline_name, "DataPipeline")
        elif data_pipeline_id is None:
            raise Exception("data_pipeline_id or the data_pipeline_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/dataPipelines/{data_pipeline_id}"

        item_dict = self.get_item_internal(url)
        dp = DataPipeline.from_dict(item_dict, auth=self.auth)
        dp.get_definition()
        return dp
    
    def delete_data_pipeline(self, data_pipeline_id):
        """Delete a data pipeline from a workspace"""
        return self.get_item(item_id=data_pipeline_id).delete(type="dataPipelines")
    
    def update_data_pipeline(self, data_pipeline_id, display_name = None, description = None):
        """Update a data pipeline in a workspace"""
        return self.get_item(item_id=data_pipeline_id).update(display_name=display_name, description=description, type="dataPipelines")
    
    # environments

    def list_environments(self, with_properties = False):
        """List environments in a workspace"""
        return self.list_items(type="environments", with_properties = with_properties)
    
    def create_environment(self, display_name, description = None):
        """Create an environment in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "environments",
                                definition = None,
                                description = description)
    
    def get_environment(self, environment_id = None, environment_name = None):
        """Get an environment from a workspace"""
        if environment_id is None and environment_name is not None:
            return self.get_item_by_name(environment_name, "Environment")
        elif environment_id is None:
            raise Exception("environment_id or the environment_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/environments/{environment_id}"

        item_dict = self.get_item_internal(url)
        env = Environment.from_dict(item_dict, auth=self.auth)
        return env
    
    def delete_environment(self, environment_id):
        """Delete an environment from a workspace"""
        return self.get_item(item_id=environment_id).delete(type="environments")
    
    def update_environment(self, environment_id, display_name = None, description = None):
        """Update an environment in a workspace"""
        return self.get_item(item_id=environment_id).update(display_name=display_name,
                                                            description=description,
                                                            type="environments")
    
    # environment spark compute

    def get_published_settings(self, environment_id):
        return self.get_environment(environment_id).get_published_settings()
    
    def get_staging_settings(self, environment_id):
        return self.get_environment(environment_id).get_staging_settings()
    
    def update_staging_settings(self, environment_id,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        return self.get_environment(environment_id).update_staging_settings(driver_cores=driver_cores,
                                                                            driver_memory=driver_memory,
                                                                            dynamic_executor_allocation=dynamic_executor_allocation,
                                                                            executor_cores=executor_cores,
                                                                            executor_memory=executor_memory,
                                                                            instance_pool=instance_pool,
                                                                            runtime_version=runtime_version,
                                                                            spark_properties=spark_properties)

    # environment spark libraries

    def get_published_libraries(self, environment_id):
        return self.get_environment(environment_id).get_published_libraries()
    
    def get_staging_libraries(self, environment_id):
        return self.get_environment(environment_id).get_staging_libraries()
    
    def upload_staging_library(self, environment_id, file_path):
        return self.get_environment(environment_id).upload_staging_library(file_path)
    
    def publish_environment(self, environment_id):
        return self.get_environment(environment_id).publish_environment()
    
    def delete_staging_library(self, environment_id, library_to_delete):
        return self.get_environment(environment_id).delete_staging_library(library_to_delete)
    
    def cancel_publish(self, environment_id):
        return self.get_environment(environment_id).cancel_publish()
    
    # eventhouses
    def list_eventhouses(self, with_properties = False):
        """List eventhouses in a workspace"""
        return self.list_items(type="eventhouses", with_properties=with_properties)
    
    def create_eventhouse(self, display_name, description = None):
        """Create an eventhouse in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "eventhouses",
                                definition = None,
                                description = description)
    
    def get_eventhouse(self, eventhouse_id = None, eventhouse_name = None):
        """Get an eventhouse from a workspace"""
        if eventhouse_id is None and eventhouse_name is not None:
            return self.get_item_by_name(eventhouse_name, "Eventhouse")
        elif eventhouse_id is None:
            raise Exception("eventhouse_id or the eventhouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/eventhouses/{eventhouse_id}"

        item_dict = self.get_item_internal(url)
        return Eventhouse.from_dict(item_dict, auth=self.auth)
    
    def delete_eventhouse(self, eventhouse_id):
        """Delete an eventhouse from a workspace"""
        return self.get_item(item_id=eventhouse_id).delete(type="eventhouses")
    
    def update_eventhouse(self, eventhouse_id, display_name = None, description = None):
        """Update an eventhouse in a workspace"""
        return self.get_item(item_id=eventhouse_id).update(display_name=display_name,
                                                            description=description,
                                                            type="eventhouses")

    # eventstreams

    def list_eventstreams(self, with_properties = False):
        """List eventstreams in a workspace"""
        return self.list_items(type="eventstreams", with_properties=with_properties)
    
    def create_eventstream(self, display_name, description = None):
        """Create an eventstream in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "eventstreams",
                                definition = None,
                                description = description)
    
    def get_eventstream(self, eventstream_id = None, eventstream_name = None):
        """Get an eventstream from a workspace"""
        if eventstream_id is None and eventstream_name is not None:
            return self.get_item_by_name(eventstream_name, "Eventstream")
        elif eventstream_id is None:
            raise Exception("eventstream_id or the eventstream_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/eventstreams/{eventstream_id}"

        item_dict = self.get_item_internal(url)
        return Eventstream.from_dict(item_dict, auth=self.auth)
    
    def delete_eventstream(self, eventstream_id):
        """Delete an eventstream from a workspace"""
        return self.get_item(item_id=eventstream_id).delete(type="eventstreams")
    
    def update_eventstream(self, eventstream_id, display_name = None, description = None):
        """Update an eventstream in a workspace"""
        return self.get_item(item_id=eventstream_id).update(display_name=display_name,
                                                            description=description,
                                                            type="eventstreams")
    
    # kqlDatabases

    def list_kql_databases(self, with_properties = False):
        """List kql databases in a workspace"""
        return self.list_items(type="kqlDatabases", with_properties = with_properties)
    
    def create_kql_database(self, creation_payload, display_name, description = None, ):
        """Create a kql database in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "kqlDatabases",
                                description = description,
                                creation_payload = creation_payload)
    
    def get_kql_database(self, kql_database_id = None, kql_database_name = None):
        """Get a kql database from a workspace"""

        if kql_database_id is None and kql_database_name is not None:
            return self.get_item_by_name(kql_database_name, "KQLDatabase")
        elif kql_database_id is None:
            raise Exception("kql_database_id or the kql_database_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/kqlDatabases/{kql_database_id}"

        item_dict = self.get_item_internal(url)
        return KQLDatabase.from_dict(item_dict, auth=self.auth)
    
    def delete_kql_database(self, kql_database_id):
        """Delete a kql database from a workspace"""
        return self.get_item(item_id=kql_database_id).delete(type="kqlDatabases")
    
    def update_kql_database(self, kql_database_id, display_name = None, description = None):
        """Update a kql database in a workspace"""
        return self.get_item(item_id=kql_database_id).update(display_name=display_name,
                                                            description=description,
                                                            type="kqlDatabases")

    # kqlQuerysets

    def list_kql_querysets(self, with_properties = False):
        """List kql querysets in a workspace"""
        return self.list_items(type="kqlQuerysets", with_properties = with_properties)

    def get_kql_queryset(self, kql_queryset_id = None, kql_queryset_name = None):
        """Get a kql queryset from a workspace"""

        if kql_queryset_id is None and kql_queryset_name is not None:
            return self.get_item_by_name(kql_queryset_name, "KQLQueryset")
        elif kql_queryset_id is None:
            raise Exception("kql_queryset_id or the kql_queryset_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/kqlQuerysets/{kql_queryset_id}"

        item_dict = self.get_item_internal(url)
        return KQLQueryset.from_dict(item_dict, auth=self.auth) 
    
    def delete_kql_queryset(self, kql_queryset_id):
        """Delete a kql queryset from a workspace"""
        return self.get_item(item_id=kql_queryset_id).delete(type="kqlQuerysets")
    
    def update_kql_queryset(self, kql_queryset_id, display_name = None, description = None):
        """Update a kql queryset in a workspace"""
        return self.get_item(item_id=kql_queryset_id).update(display_name=display_name,
                                                            description=description,
                                                            type="kqlQuerysets")


    # lakehouses

    def list_lakehouses(self, with_properties = False):
        """List lakehouses in a workspace"""
        return self.list_items(with_properties = with_properties, type="lakehouses")
    
    def create_lakehouse(self, display_name, description = None):
        """Create a lakehouse in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "lakehouses",
                                definition = None,
                                description = description)
    
    def delete_lakehouse(self, lakehouse_id):
        """Delete a lakehouse from a workspace"""
        return self.get_item(item_id=lakehouse_id).delete(type="lakehouses")
    
    def update_lakehouse(self, lakehouse_id, display_name = None, description = None):
        """Update a lakehouse in a workspace"""
        return self.get_item(item_id=lakehouse_id).update(display_name=display_name,
                                                            description=description,
                                                            type="lakehouses")
    
    def get_lakehouse(self, lakehouse_id = None, lakehouse_name = None):
        """Get a lakehouse from a workspace"""

        if lakehouse_id is None and lakehouse_name is not None:
            return self.get_item_by_name(lakehouse_name, "Lakehouse")
        elif lakehouse_id is None:
            raise Exception("lakehouse_id or the lakehouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/lakehouses/{lakehouse_id}"

        item_dict = self.get_item_internal(url)
        return Lakehouse.from_dict(item_dict, auth=self.auth)
    
    # mlExperiments

    def list_ml_experiments(self, with_properties = False):
        """List ml experiments in a workspace"""
        return self.list_items(type="mlExperiments", with_properties = with_properties)
    
    def create_ml_experiment(self, display_name, description = None):
        """Create an ml experiment in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "mlExperiments",
                                definition = None,
                                description = description)
    
    def get_ml_experiment(self, ml_experiment_id = None, ml_experiment_name = None):
        """Get an ml experiment from a workspace"""
        if ml_experiment_id is None and ml_experiment_name is not None:
            return self.get_item_by_name(ml_experiment_name, "MLExperiment")
        elif ml_experiment_id is None:
            raise Exception("ml_experiment_id or the ml_experiment_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/mlExperiments/{ml_experiment_id}"

        item_dict = self.get_item_internal(url)
        return MLExperiment.from_dict(item_dict, auth=self.auth)
    
    def delete_ml_experiment(self, ml_experiment_id):
        """Delete an ml experiment from a workspace"""
        return self.get_item(item_id=ml_experiment_id).delete(type="mlExperiments")
    
    def update_ml_experiment(self, ml_experiment_id, display_name = None, description = None):
        """Update an ml experiment in a workspace"""
        return self.get_item(item_id=ml_experiment_id).update(display_name=display_name,
                                                            description=description,
                                                            type="mlExperiments")
    
    # mlModels

    def list_ml_models(self, with_properties = False):
        """List ml models in a workspace"""
        return self.list_items(type="mlModels", with_properties = with_properties)

    def create_ml_model(self, display_name, description = None):
        """Create an ml model in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "mlModels",
                                definition = None,
                                description = description)
    
    def get_ml_model(self, ml_model_id = None, ml_model_name = None):
        """Get an ml model from a workspace"""
        if ml_model_id is None and ml_model_name is not None:
            return self.get_item_by_name(ml_model_name, "MLModel")
        elif ml_model_id is None:
            raise Exception("ml_model_id or the ml_model_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/mlModels/{ml_model_id}"

        item_dict = self.get_item_internal(url)
        return MLModel.from_dict(item_dict, auth=self.auth)
    
    def delete_ml_model(self, ml_model_id):
        """Delete an ml model from a workspace"""
        return self.get_item(item_id=ml_model_id).delete(type="mlModels")
    
    def update_ml_model(self, ml_model_id, display_name = None, description = None):
        """Update an ml model in a workspace"""
        return self.get_item(item_id=ml_model_id).update(display_name=display_name,
                                                            description=description,
                                                            type="mlModels")
    
    # notebooks

    def list_notebooks(self, with_properties = False):
        """List notebooks in a workspace"""
        return self.list_items(type="notebooks", with_properties = with_properties)
    
    def create_notebook(self, display_name, definition = None, description = None):
        """Create a notebook in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "notebooks",
                                definition = definition,
                                description = description)
    
    def get_notebook(self, notebook_id = None, notebook_name = None):
        """Get a notebook from a workspace"""
        if notebook_id is None and notebook_name is not None:
            return self.get_item_by_name(notebook_name, "Notebook")
        elif notebook_id is None:
            raise Exception("notebook_id or the notebook_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/notebooks/{notebook_id}"

        item_dict = self.get_item_internal(url)
        noteb =  Notebook.from_dict(item_dict, auth=self.auth)
        noteb.get_definition()
        return noteb
    
    def delete_notebook(self, notebook_id):
        """Delete a notebook from a workspace"""
        return self.get_item(item_id=notebook_id).delete(type="notebooks")
    
    def update_notebook(self, notebook_id, display_name = None, description = None):
        """Update a notebook in a workspace"""
        return self.get_item(item_id=notebook_id).update(display_name=display_name,
                                                            description=description,
                                                            type="notebooks")
    
    def get_notebook_definition(self, notebook_id, format = None):
        """Get the definition of a notebook from a workspace"""
        return self.get_notebook(notebook_id=notebook_id).get_definition(format=format)

    def update_notebook_definition(self, notebook_id, definition):
        """Update the definition of a notebook in a workspace"""
        return self.get_notebook(notebook_id=notebook_id).update_definition(definition=definition)
    
    # reports

    def list_reports(self, with_properties = False):
        """List reports in a workspace"""
        return self.list_items(type="reports", with_properties = with_properties)
    
    def create_report(self, display_name, definition = None, description = None):
        """Create a report in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "reports",
                                definition = definition,
                                description = description)
    
    def get_report(self, report_id = None, report_name = None):
        """Get a report from a workspace"""
        if report_id is None and report_name is not None:
            return self.get_item_by_name(report_name, "Report")
        elif report_id is None:
            raise Exception("report_id or the report_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/reports/{report_id}"

        item_dict = self.get_item_internal(url)
        rep = Report.from_dict(item_dict, auth=self.auth)
        rep.get_definition()
        return rep
    
    def delete_report(self, report_id):
        """Delete a report from a workspace"""
        return self.get_item(item_id=report_id).delete(type="reports")
    
    def get_report_definition(self, report_id, format = None):
        """Get the definition of a report from a workspace"""
        return self.get_report(report_id=report_id).get_definition(format=format)
    
    def update_report_definition(self, report_id, definition):
        """Update the definition of a report in a workspace"""
        return self.get_report(report_id=report_id).update_definition(definition=definition)

    # semanticModels

    def list_semantic_models(self, with_properties = False):
        """List semantic models in a workspace"""
        return self.list_items(type="semanticModels", with_properties = with_properties)
    
    def create_semantic_model(self, display_name, definition = None, description = None):
        """Create a semantic model in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "semanticModels",
                                definition = definition,
                                description = description)
    
    def get_semantic_model(self, semantic_model_id = None, semantic_model_name = None):
        """Get a semantic model from a workspace"""
        if semantic_model_id is None and semantic_model_name is not None:
            return self.get_item_by_name(semantic_model_name, "SemanticModel")
        elif semantic_model_id is None:
            raise Exception("semantic_model_id or the semantic_model_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/semanticModels/{semantic_model_id}"

        item_dict = self.get_item_internal(url)
        semmodel = SemanticModel.from_dict(item_dict, auth=self.auth)
        semmodel.get_definition()
        return semmodel
    
    def delete_semantic_model(self, semantic_model_id):
        """Delete a semantic model from a workspace"""
        return self.get_item(item_id=semantic_model_id).delete(type="semanticModels")
    
    # def update_semantic_model(self, semantic_model_id, display_name = None, description = None):
    #     """Update a semantic model in a workspace"""
    #     return self.get_item(item_id=semantic_model_id).update(display_name=display_name,
    #                                                         description=description,
    #                                                         type="semanticModels")
    
    def get_semantic_model_definition(self, semantic_model_id, format = None):
        """Get the definition of a semantic model from a workspace"""
        return self.get_semantic_model(semantic_model_id=semantic_model_id).get_definition(format=format)

    def update_semantic_model_definition(self, semantic_model_id, definition):
        """Update the definition of a semantic model in a workspace"""
        return self.get_semantic_model(semantic_model_id=semantic_model_id).update_definition(definition=definition)
    
    # sparkJobDefinitions

    def list_spark_job_definitions(self, with_properties = False):
        """List spark job definitions in a workspace"""
        return self.list_items(type="sparkJobDefinitions", with_properties = with_properties)
    
    def create_spark_job_definition(self, display_name, definition = None, description = None):
        """Create a spark job definition in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "sparkJobDefinitions",
                                definition = definition,
                                description = description)
    
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

    def delete_spark_job_definition(self, spark_job_definition_id):
        """Delete a spark job definition from a workspace"""
        return self.get_item(item_id=spark_job_definition_id).delete(type="sparkJobDefinitions")
    
    def update_spark_job_definition(self, spark_job_definition_id, display_name = None, description = None):
        """Update a spark job definition in a workspace"""
        return self.get_spark_job_definition(spark_job_definition_id=spark_job_definition_id).update(display_name=display_name,
                                                            description=description,
                                                            type="sparkJobDefinitions")

    def get_spark_job_definition_definition(self, spark_job_definition_id, format = None):
        """Get the definition of a spark job definition from a workspace"""
        return self.get_spark_job_definition(spark_job_definition_id=spark_job_definition_id).get_definition(format=format)

    def update_spark_job_definition_definition(self, spark_job_definition_id, definition):
        """Update the definition of a spark job definition in a workspace"""
        return self.get_spark_job_definition(spark_job_definition_id=spark_job_definition_id).update_definition(definition=definition)

    # warehouses

    def list_warehouses(self, with_properties = False):
        """List warehouses in a workspace"""
        return self.list_items(type="warehouses", with_properties = with_properties)
    
    def create_warehouse(self, display_name, description = None):
        """Create a warehouse in a workspace"""
        return self.create_item(display_name = display_name,
                                type = "warehouses",description = description)
    
    def get_warehouse(self, warehouse_id = None, warehouse_name = None):
        """Get a warehouse from a workspace"""
        if warehouse_id is None and warehouse_name is not None:
            return self.get_item_by_name(warehouse_name, "Warehouse")
        elif warehouse_id is None:
            raise Exception("warehouse_id or the warehouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/warehouses/{warehouse_id}"

        item_dict = self.get_item_internal(url)
        return Warehouse.from_dict(item_dict, auth=self.auth)
    
    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse from a workspace"""
        return self.get_item(item_id=warehouse_id).delete(type="warehouses")
    
    def update_warehouse(self, warehouse_id, display_name = None, description = None):
        """Update a warehouse in a workspace"""
        return self.get_item(item_id=warehouse_id).update(display_name=display_name,
                                                            description=description,
                                                            type="warehouses")
    


    # spark workspace custom pools

    def list_workspace_custom_pools(self, continuationToken = None):
        """List spark worspace custom pools in a workspace"""
        # GET http://api.fabric.microsoft.com/v1/workspaces/f089354e-8366-4e18-aea3-4cb4a3a50b48/spark/pools

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/spark/pools"
        
        if continuationToken:
            url = f"{url}?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error listing custom spark pools: {response.status_code}, {response.text}")
            break
        
        resp_dict = json.loads(response.text)
        items = resp_dict["value"]
        for item in items:
            item["workspaceId"] = self.id
        sppools = [SparkCustomPool.from_dict(item, auth=self.auth) for item in items]

        if "continuationToken" in resp_dict:
            item_list_next = self.list_workspace_custom_pools(continuationToken=resp_dict["continuationToken"])
            sppools.extend(item_list_next)

        return sppools
    
    def create_workspace_custom_pool(self, name, node_family, node_size, auto_scale, dynamic_executor_allocation):
        """Create a custom pool in a workspace"""
        
        # POST http://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/spark/pools"

        body = {
            "name": name,
            "nodeFamily": node_family,
            "nodeSize": node_size,
            "autoScale": auto_scale,
            "dynamicExecutorAllocation": dynamic_executor_allocation
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 201, 429):
                raise Exception(f"Error creating custom spark pool: {response.status_code}, {response.text}")
            break

        response_dict = json.loads(response.text)
        response_dict["workspaceId"] = self.id
        return SparkCustomPool.from_dict(response_dict, auth=self.auth)

    def get_workspace_custom_pool(self, pool_id):
        """Get a custom pool in a workspace"""
        # GET http://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools/{poolId}
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/spark/pools/{pool_id}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting custom spark pool: {response.status_code}, {response.text}")
            break

        response_dict = json.loads(response.text)
        response_dict["workspaceId"] = self.id
        return SparkCustomPool.from_dict(response_dict, auth=self.auth)
    
    def delete_workspace_custom_pool(self, pool_id):
        """Delete a custom pool in a workspace"""
        pool = self.get_workspace_custom_pool(pool_id)
        return pool.delete()
    
    def update_workspace_custom_pool(self, pool_id, name = None , node_family = None, node_size = None,
                                     auto_scale = None,
                                    dynamic_executor_allocation = None):
        """Update a custom pool in a workspace"""
        pool = self.get_workspace_custom_pool(pool_id)
        return pool.update(name = name,
                           node_family = node_family,
                           node_size = node_size,
                           auto_scale = auto_scale,
                           dynamic_executor_allocation = dynamic_executor_allocation)
    
    # spark workspace settings

    def get_spark_settings(self):

    # GET http://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/settings

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/spark/settings"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error getting spark settings: {response.status_code}, {response.text}")
            break

        return json.loads(response.text)
    

    def update_spark_settings(self, automatic_log = None, environment = None, high_concurrency = None, pool = None):

        # PATCH http://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/settings

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.id}/spark/settings"

        body = {}

        if automatic_log:
            body["automaticLog"] = automatic_log
        if environment:
            body["environment"] = environment
        if high_concurrency:
            body["highConcurrency"] = high_concurrency
        if pool:
            body["pool"] = pool

        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error updating spark settings: {response.status_code}, {response.text}")
            break

        return json.loads(response.text)


import requests
import json
from time import sleep

from msfabricpysdkcore.capacity import Capacity
from msfabricpysdkcore.client import FabricClient
from msfabricpysdkcore.deployment_pipeline import DeploymentPipeline
from msfabricpysdkcore.long_running_operation import LongRunningOperation
from msfabricpysdkcore.workspace import Workspace

class FabricClientCore(FabricClient):
    """FabricClientCore class to interact with Fabric Core APIs"""

    def __init__(self, tenant_id = None, client_id = None, client_secret = None, silent=False) -> None:
        """Initialize FabricClientCore object"""
        super().__init__(tenant_id, client_id, client_secret, silent=silent)


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
        
    def list_workspace_role_assignments(self, workspace_id):
        """Get role assignments for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_role_assignments()
    
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
    
    def delete_workspace_role_assignment(self, workspace_id, workspace_role_assignment_id):
        """Delete a role assignment from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_role_assignment(workspace_role_assignment_id)
    
    def update_workspace(self, workspace_id, display_name = None, description = None):
        """Update a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update(display_name, description)

    def get_workspace_role_assignment(self, workspace_id, workspace_role_assignment_id):
        """Get a role assignment for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_role_assignment(workspace_role_assignment_id)
    
    def update_workspace_role_assignment(self, workspace_id, role, workspace_role_assignment_id):
        """Update a role assignment for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_role_assignment(role, workspace_role_assignment_id)

    def assign_to_capacity(self, workspace_id, capacity_id):
        """Assign a workspace to a capacity"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.assign_to_capacity(capacity_id)
    
    def unassign_from_capacity(self, workspace_id):
        """Unassign a workspace from a capacity"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.unassign_from_capacity()
    
    def provision_identity(self, workspace_id):
        """Provision an identity for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.provision_identity()
    
    def deprovision_identity(self, workspace_id):
        """Deprovision an identity for a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.deprovision_identity()
 
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

    def list_items(self, workspace_id, with_properties = False):
        """List items in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_items(with_properties=with_properties)
    
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
    

    # long running operations

    def get_operation_results(self, operation_id):
        """Get the results of an operation"""
        lro = LongRunningOperation(operation_id=operation_id, auth=self.auth)
        return lro.get_operation_results()

    def get_operation_state(self, operation_id):
        """Get the state of an operation"""
        lro = LongRunningOperation(operation_id=operation_id, auth=self.auth)
        return lro.get_operation_state()

    # list things

    def list_dashboards(self, workspace_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_dashboards()
    
    def list_datamarts(self, workspace_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_datamarts()
    
    def list_paginated_reports(self, workspace_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_paginated_reports()
    
    def list_sql_endpoints(self, workspace_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_sql_endpoints()
    
    def list_mirrored_warehouses(self, workspace_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_mirrored_warehouses()
    
    # dataPipelines

    def create_data_pipeline(self, workspace_id, display_name, description = None):
        """Create a data pipeline in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_data_pipeline(display_name = display_name, description = description)

    def list_data_pipelines(self, workspace_id, with_properties = False):
        """List data pipelines in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_data_pipelines(with_properties = with_properties)

    def get_data_pipeline(self, workspace_id, data_pipeline_id = None, data_pipeline_name = None):
        """Get a data pipeline from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_data_pipeline(data_pipeline_id = data_pipeline_id, data_pipeline_name = data_pipeline_name)
    
    def delete_data_pipeline(self, workspace_id, data_pipeline_id):
        """Delete a data pipeline from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_data_pipeline(data_pipeline_id)

    def update_data_pipeline(self, workspace_id, data_pipeline_id, display_name = None, description = None):
        """Update a data pipeline in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_data_pipeline(data_pipeline_id).update(display_name=display_name, description=description)

    # environments

    def list_environments(self, workspace_id, with_properties = False):
        """List environments in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_environments(with_properties = with_properties)
    
    def create_environment(self, workspace_id, display_name, description = None):
        """Create an environment in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_environment(display_name = display_name, description = description)
    
    def get_environment(self, workspace_id, environment_id = None, environment_name = None):
        """Get an environment from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id = environment_id, environment_name = environment_name)
    
    def delete_environment(self, workspace_id, environment_id):
        """Delete an environment from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_environment(environment_id)
    
    def update_environment(self, workspace_id, environment_id, display_name = None, description = None):
        """Update an environment in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_environment(environment_id, display_name = display_name, description = description)
    
    # environmentSparkCompute

    def get_published_settings(self, workspace_id, environment_id):
        """Get published settings for an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).get_published_settings()
    
    def get_staging_settings(self, workspace_id, environment_id):
        """Get staging settings for an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).get_staging_settings()
    
    def update_staging_settings(self, workspace_id, environment_id,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        
        return self.get_environment(workspace_id, environment_id).update_staging_settings(driver_cores=driver_cores,
                                                                            driver_memory=driver_memory,
                                                                            dynamic_executor_allocation=dynamic_executor_allocation,
                                                                            executor_cores=executor_cores,
                                                                            executor_memory=executor_memory,
                                                                            instance_pool=instance_pool,
                                                                            runtime_version=runtime_version,
                                                                            spark_properties=spark_properties)

    
    # environmentSparkLibraries

    def get_published_libraries(self, workspace_id, environment_id):
        """Get published libraries for an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).get_published_libraries()
    
    def get_staging_libraries(self, workspace_id, environment_id):
        """Get staging libraries for an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).get_staging_libraries()
    
    def upload_staging_library(self, workspace_id, environment_id, file_path):
        """Update staging libraries for an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).upload_staging_library(file_path=file_path)
    
    def publish_environment(self, workspace_id, environment_id):
        """Publish an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).publish_environment()
    
    def delete_staging_library(self, workspace_id, environment_id, library_to_delete):
        """Delete a staging library from an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).delete_staging_library(library_to_delete)
    
    def cancel_publish(self, workspace_id, environment_id):
        """Cancel publishing an environment"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_environment(environment_id).cancel_publish()

    # eventhouses

    def list_eventhouses(self, workspace_id):
        """List eventhouses in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_eventhouses()
    
    def create_eventhouse(self, workspace_id, display_name, description = None):
        """Create an eventhouse in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_eventhouse(display_name = display_name, description = description)
    
    def get_eventhouse(self, workspace_id, eventhouse_id = None, eventhouse_name = None):
        """Get an eventhouse from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_eventhouse(eventhouse_id = eventhouse_id, eventhouse_name = eventhouse_name)
    
    def delete_eventhouse(self, workspace_id, eventhouse_id):
        """Delete an eventhouse from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_eventhouse(eventhouse_id)
    
    def update_eventhouse(self, workspace_id, eventhouse_id, display_name = None, description = None):
        """Update an eventhouse in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_eventhouse(eventhouse_id, display_name = display_name, description = description)

    # eventstreams

    def list_eventstreams(self, workspace_id):
        """List eventstreams in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_eventstreams()

    def create_eventstream(self, workspace_id, display_name, description = None):
        """Create an eventstream in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_eventstream(display_name = display_name, description = description)
    
    def get_eventstream(self, workspace_id, eventstream_id = None, eventstream_name = None):
        """Get an eventstream from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_eventstream(eventstream_id = eventstream_id, eventstream_name = eventstream_name)

    def delete_eventstream(self, workspace_id, eventstream_id):
        """Delete an eventstream from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_eventstream(eventstream_id)
    
    def update_eventstream(self, workspace_id, eventstream_id, display_name = None, description = None):
        """Update an eventstream in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_eventstream(eventstream_id, display_name = display_name, description = description)

    # kqlDatabases

    def list_kql_databases(self, workspace_id):
        """List kql databases in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_kql_databases()
    
    def create_kql_database(self, workspace_id, creation_payload, display_name, description = None):
        """Create a kql database in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_kql_database(creation_payload = creation_payload, display_name = display_name, description = description)
   
    def get_kql_database(self, workspace_id, kql_database_id = None, kql_database_name = None):
        """Get a kql database from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_kql_database(kql_database_id = kql_database_id, kql_database_name = kql_database_name)

    def delete_kql_database(self, workspace_id, kql_database_id):
        """Delete a kql database from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_kql_database(kql_database_id)
    
    def update_kql_database(self, workspace_id, kql_database_id, display_name = None, description = None):
        """Update a kql database in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_kql_database(kql_database_id, display_name = display_name, description = description)

    # kqlQuerysets

    def list_kql_querysets(self, workspace_id):
        """List kql querysets in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_kql_querysets()
    
    def get_kql_queryset(self, workspace_id, kql_queryset_id = None, kql_queryset_name = None):
        """Get a kql queryset from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_kql_queryset(kql_queryset_id = kql_queryset_id, kql_queryset_name = kql_queryset_name)

    def update_kql_queryset(self, workspace_id, kql_queryset_id, display_name = None, description = None):
        """Update a kql queryset in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_kql_queryset(kql_queryset_id, display_name = display_name, description = description)
    
    def delete_kql_queryset(self, workspace_id, kql_queryset_id):
        """Delete a kql queryset from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_kql_queryset(kql_queryset_id)

    # lakehouses

    def list_lakehouses(self, workspace_id):
        """List lakehouses in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_lakehouses()
    
    def create_lakehouse(self, workspace_id, display_name, description = None):
        """Create a lakehouse in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_lakehouse(display_name = display_name, description = description)
    
    def delete_lakehouse(self, workspace_id, lakehouse_id):
        """Delete a lakehouse from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_lakehouse(lakehouse_id)
    
    def update_lakehouse(self, workspace_id, lakehouse_id, display_name = None, description = None):
        """Update a lakehouse in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_lakehouse(lakehouse_id, display_name = display_name, description = description)
    
    def get_lakehouse(self, workspace_id, lakehouse_id = None, lakehouse_name = None):
        """Get a lakehouse from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_lakehouse(lakehouse_id = lakehouse_id, lakehouse_name = lakehouse_name)

    def list_tables(self, workspace_id, lakehouse_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_tables(lakehouse_id=lakehouse_id)
    
    def load_table(self, workspace_id, lakehouse_id, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.load_table(lakehouse_id, table_name, path_type, relative_path,
                    file_extension, format_options,
                    mode, recursive, wait_for_completion)

    def run_on_demand_table_maintenance(self, workspace_id, lakehouse_id, 
                                        execution_data = None,
                                        job_type = "TableMaintenance", wait_for_completion = True):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.run_on_demand_table_maintenance(lakehouse_id = lakehouse_id, 
                                                  execution_data = execution_data, 
                                                  job_type = job_type, 
                                                  wait_for_completion= wait_for_completion)

    # mlExperiments

    def list_ml_experiments(self, workspace_id):
        """List ml experiments in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_ml_experiments()
    
    def create_ml_experiment(self, workspace_id, display_name, description = None):
        """Create an ml experiment in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_ml_experiment(display_name = display_name, description = description)
    
    def get_ml_experiment(self, workspace_id, ml_experiment_id = None, ml_experiment_name = None):
        """Get an ml experiment from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_ml_experiment(ml_experiment_id = ml_experiment_id, ml_experiment_name = ml_experiment_name)
    
    def delete_ml_experiment(self, workspace_id, ml_experiment_id):
        """Delete an ml experiment from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_ml_experiment(ml_experiment_id)
    
    def update_ml_experiment(self, workspace_id, ml_experiment_id, display_name = None, description = None):
        """Update an ml experiment in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_ml_experiment(ml_experiment_id, display_name = display_name, description = description)
  
    # mlModels

    def list_ml_models(self, workspace_id):
        """List ml models in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_ml_models()
    
    def create_ml_model(self, workspace_id, display_name, description = None):
        """Create an ml model in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_ml_model(display_name = display_name, description = description)
    
    def get_ml_model(self, workspace_id, ml_model_id = None, ml_model_name = None):
        """Get an ml model from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_ml_model(ml_model_id = ml_model_id, ml_model_name = ml_model_name)
    
    def delete_ml_model(self, workspace_id, ml_model_id):
        """Delete an ml model from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_ml_model(ml_model_id)
    
    def update_ml_model(self, workspace_id, ml_model_id, display_name = None, description = None):
        """Update an ml model in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_ml_model(ml_model_id, display_name = display_name, description = description)
    
    # notebooks

    def list_notebooks(self, workspace_id):
        """List notebooks in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_notebooks()
    
    def create_notebook(self, workspace_id, display_name, definition = None, description = None):
        """Create a notebook in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_notebook(display_name = display_name, definition = definition, description = description)
    
    def get_notebook(self, workspace_id, notebook_id = None, notebook_name = None):
        """Get a notebook from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_notebook(notebook_id = notebook_id, notebook_name = notebook_name)
    
    def delete_notebook(self, workspace_id, notebook_id):
        """Delete a notebook from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_notebook(notebook_id)
    
    def update_notebook(self, workspace_id, notebook_id, display_name = None, description = None):
        """Update a notebook in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_notebook(notebook_id, display_name = display_name, description = description)
    
    def get_notebook_definition(self, workspace_id, notebook_id, format = None):
        """Get the definition of a notebook"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_notebook_definition(notebook_id, format = format)

    def update_notebook_definition(self, workspace_id, notebook_id, definition):
        """Update the definition of a notebook"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_notebook_definition(notebook_id, definition)
    
    # reports

    def list_reports(self, workspace_id, with_properties = False):
        """List reports in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_reports(with_properties = with_properties)

    def create_report(self, workspace_id, display_name, definition = None, description = None):
        """Create a report in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_report(display_name = display_name, definition = definition, description = description)
    
    def get_report(self, workspace_id, report_id = None, report_name = None):
        """Get a report from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_report(report_id = report_id, report_name = report_name)
    
    def delete_report(self, workspace_id, report_id):
        """Delete a report from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_report(report_id)
    
    def get_report_definition(self, workspace_id, report_id, format = None):
        """Get the definition of a report"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_report_definition(report_id, format = format)
    
    def update_report_definition(self, workspace_id, report_id, definition):
        """Update the definition of a report"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_report_definition(report_id, definition)

    # semanticModels

    def list_semantic_models(self, workspace_id, with_properties = False):
        """List semantic models in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_semantic_models(with_properties = with_properties)
    
    def create_semantic_model(self, workspace_id, display_name, definition = None, description = None):
        """Create a semantic model in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_semantic_model(display_name = display_name, definition = definition, description = description)
    
    def get_semantic_model(self, workspace_id, semantic_model_id = None, semantic_model_name = None):
        """Get a semantic model from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_semantic_model(semantic_model_id = semantic_model_id, semantic_model_name = semantic_model_name)
    
    def delete_semantic_model(self, workspace_id, semantic_model_id):
        """Delete a semantic model from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_semantic_model(semantic_model_id)
    
    # def update_semantic_model(self, workspace_id, semantic_model_id, display_name = None, description = None):
    #     """Update a semantic model in a workspace"""
    #     ws = self.get_workspace_by_id(workspace_id)
    #     return ws.update_semantic_model(semantic_model_id, display_name = display_name, description = description)
    
    def get_semantic_model_definition(self, workspace_id, semantic_model_id, format = None):
        """Get the definition of a semantic model"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_semantic_model_definition(semantic_model_id, format = format)

    def update_semantic_model_definition(self, workspace_id, semantic_model_id, definition):
        """Update the definition of a semantic model"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_semantic_model_definition(semantic_model_id, definition)
   
    # sparkJobDefinitions

    def list_spark_job_definitions(self, workspace_id, with_properties = False):
        """List spark job definitions in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_spark_job_definitions(with_properties = with_properties)
    
    def create_spark_job_definition(self, workspace_id, display_name, definition = None, description = None):
        """Create a spark job definition in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_spark_job_definition(display_name = display_name, definition = definition, description = description)
    
    def get_spark_job_definition(self, workspace_id, spark_job_definition_id = None, spark_job_definition_name = None):
        """Get a spark job definition from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_spark_job_definition(spark_job_definition_id = spark_job_definition_id, spark_job_definition_name = spark_job_definition_name)
    
    def delete_spark_job_definition(self, workspace_id, spark_job_definition_id):
        """Delete a spark job definition from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_spark_job_definition(spark_job_definition_id)
    
    def update_spark_job_definition(self, workspace_id, spark_job_definition_id, display_name = None, description = None):
        """Update a spark job definition in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_spark_job_definition(spark_job_definition_id, display_name = display_name, description = description)
    
    def get_spark_job_definition_definition(self, workspace_id, spark_job_definition_id, format = None):
        """Get the definition of a spark job definition"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_spark_job_definition_definition(spark_job_definition_id, format = format)

    def update_spark_job_definition_definition(self, workspace_id, spark_job_definition_id, definition):
        """Update the definition of a spark job definition"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_spark_job_definition_definition(spark_job_definition_id, definition)
    
    def run_on_demand_spark_job_definition(self, workspace_id, spark_job_definition_id, job_type = "sparkjob"):
        """Run an on demand spark job definition"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.run_on_demand_spark_job_definition(spark_job_definition_id, job_type)
    
    # warehouses

    def list_warehouses(self, workspace_id, with_properties = False):
        """List warehouses in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_warehouses(with_properties = with_properties)

    def create_warehouse(self, workspace_id, display_name, description = None):
        """Create a warehouse in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_warehouse(display_name = display_name, description = description)
    
    def get_warehouse(self, workspace_id, warehouse_id = None, warehouse_name = None):
        """Get a warehouse from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_warehouse(warehouse_id = warehouse_id, warehouse_name = warehouse_name)
    
    def delete_warehouse(self, workspace_id, warehouse_id):
        """Delete a warehouse from a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_warehouse(warehouse_id)
    
    def update_warehouse(self, workspace_id, warehouse_id, display_name = None, description = None):
        """Update a warehouse in a workspace"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_warehouse(warehouse_id, display_name = display_name, description = description)

    # spark workspace custom pools

    def list_workspace_custom_pools(self, workspace_id):
        """List workspace custom pools"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_workspace_custom_pools()
    
    def create_workspace_custom_pool(self, workspace_id, name, node_family, node_size, auto_scale, dynamic_executor_allocation):
        """Create a workspace custom pool"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_workspace_custom_pool(name = name, 
                                               node_family = node_family,
                                               node_size = node_size,
                                               auto_scale = auto_scale,
                                               dynamic_executor_allocation = dynamic_executor_allocation)
    

    def get_workspace_custom_pool(self, workspace_id, pool_id):
        """Get a workspace custom pool"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_workspace_custom_pool(pool_id)
    
    def delete_workspace_custom_pool(self, workspace_id, pool_id):
        """Delete a workspace custom pool"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.delete_workspace_custom_pool(pool_id)
    
    def update_workspace_custom_pool(self, workspace_id, pool_id, name = None, node_family = None, node_size = None, auto_scale = None, dynamic_executor_allocation = None):
        """Update a workspace custom pool"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_workspace_custom_pool(pool_id, name = name, node_family = node_family, node_size = node_size, auto_scale = auto_scale, dynamic_executor_allocation = dynamic_executor_allocation)
    
    # Deployment Pipelines

    def deploy_stage_content(self, deployment_pipeline_id, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, wait_for_completion = True):
        """Deploy stage content
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            source_stage_id (str): The ID of the source stage
            target_stage_id (str): The ID of the target stage
            created_workspace_details (list): A list of created workspace details
            items (list): A list of items
            note (str): A note
            wait_for_completion (bool): Whether to wait for the deployment to complete
        Returns:
            Details about the dpeloyment"""

        pipeline = DeploymentPipeline.get_pipeline(deployment_pipeline_id, auth=self.auth)

        return pipeline.deploy(source_stage_id, target_stage_id, created_workspace_details = created_workspace_details,
               items = items, note = note, wait_for_completion = wait_for_completion)

    def list_deployment_pipelines(self, continuationToken = None):
        """List deployment pipelines
        Args:
            continuationToken (str): The continuation token for pagination
        Returns:
            list: List of DeploymentPipeline objects
        """
        # GET https://api.fabric.microsoft.com/v1/deploymentPipelines

        url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"

        if continuationToken:
            url = f"{url}?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error listing deployment pipelines: {response.status_code}, {response.text}")
            break

        resp_dict = json.loads(response.text)
        items = resp_dict["value"]

        dep_pipes = [DeploymentPipeline.from_dict(i, auth=self.auth) for i in items]

        if "continuationToken" in resp_dict:
            dep_pipes_next = self.list_deployment_pipelines(continuationToken=resp_dict["continuationToken"])
            dep_pipes.extend(dep_pipes_next)

        return dep_pipes
    
    def get_deployment_pipeline(self, pipeline_id):
        """Get a deployment pipeline by ID
        Args:
            pipeline_id (str): The ID of the deployment pipeline
        Returns:
            DeploymentPipeline: The deployment pipeline
        """
        return DeploymentPipeline.get_pipeline(pipeline_id, auth=self.auth)
    
    def get_deployment_pipeline_stages_items(self, pipeline_id, stage_id = None, stage_name = None):
        """Get the items in a deployment stage
        Args:
            pipeline_id (str): The ID of the deployment pipeline
            stage_id (str): The ID of the deployment stage
            stage_name (str): The name of the deployment stage
        Returns:
            list: List of DeploymentStageItem objects
        """
        pipeline = DeploymentPipeline.get_pipeline(pipeline_id, auth=self.auth)
        return pipeline.get_deployment_pipeline_stages_items(stage_id, stage_name)

    def get_deployment_pipeline_stages(self, pipeline_id):
        """Get the stages of a deployment pipeline
        Args:
            pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: List of DeploymentPipelineStage objects
        """
        pipeline = self.get_deployment_pipeline(pipeline_id)
        return pipeline.get_stages()
    
    def list_deployment_pipeline_stages(self, pipeline_id):
        """Get the stages of a deployment pipeline
        Args:
            pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: List of DeploymentPipelineStage objects
        """
        return self.get_deployment_pipeline_stages(pipeline_id)
    

    # Spark workspace settings

    def get_spark_settings(self, workspace_id):
        """Get spark settings for a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The spark settings"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_spark_settings()
    
    def update_spark_settings(self, workspace_id, automatic_log = None, 
                              environment = None, high_concurrency = None, pool = None):
        """Update spark settings for a workspace
        Args:
            workspace_id (str): The ID of the workspace
            automatic_log (bool): Whether to automatically log
            environment (str): The environment
            high_concurrency (bool): Whether to use high concurrency
            pool (str): The pool
        Returns:
            dict: The updated spark settings"""
        ws = self.get_workspace_by_id(workspace_id)
        return ws.update_spark_settings(automatic_log=automatic_log, 
                                        environment=environment, 
                                        high_concurrency=high_concurrency, 
                                        pool=pool)
    

    # External Data Shares

    # create

    def create_external_data_share(self, workspace_id, item_id, paths, recipient):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.create_external_data_share(item_id=item_id, paths = paths, recipient = recipient)

    # get

    def get_external_data_share(self, workspace_id, item_id, external_data_share_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.get_external_data_share(item_id=item_id, external_data_share_id=external_data_share_id)

    # list

    def list_external_data_shares_in_item(self, workspace_id, item_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.list_external_data_shares_in_item(item_id=item_id)

    # revoke

    def revoke_external_data_share(self, workspace_id, item_id, external_data_share_id):
        ws = self.get_workspace_by_id(workspace_id)
        return ws.revoke_external_data_share(item_id=item_id, external_data_share_id=external_data_share_id)
    

    # One Lake Data Access Security

    # create and update

    def create_or_update_data_access_roles(self, workspace_id, item_id, data_access_roles, dryrun = False, etag_match = None):
        ws = self.get_workspace_by_id(workspace_id)
        item =  ws.get_item(item_id=item_id).create_or_update_data_access_roles(data_access_roles = data_access_roles,
                                                                                  dryrun = dryrun, etag_match = etag_match)
        return item
    
    # list 

    def list_data_access_roles(self, workspace_id, item_id):
        ws = self.get_workspace_by_id(workspace_id)
        item = ws.get_item(item_id=item_id)
        return item.list_data_access_roles()
import json 

from msfabricpysdkcore.coreapi import FabricClientCore


class Workspace:
    """Class to represent a workspace in Microsoft Fabric"""

    def __init__(self, id, display_name, description, type, core_client: FabricClientCore, capacity_id = None) -> None:
        self.id = id
        self.display_name = display_name
        self.description = description
        self.type = type
        self.capacity_id = capacity_id

        self.core_client = core_client
        
    
    def from_dict(dict,  core_client):
        """Create a Workspace object from a dictionary"""
        return Workspace(id=dict['id'], display_name=dict['displayName'], description=dict['description'], type=dict['type'], capacity_id=dict.get('capacityId', None),
                         core_client=core_client)
    
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

    # General workspace operations

    def add_role_assignment(self, role, principal):
        """Add a role assignment to the workspace
        
        Args:
            role (str): The role to assign
            principal (dict): The principal to assign the role to
        Returns:
            int: The status code of the response
        """

        return self.core_client.add_workspace_role_assignment(workspace_id=self.id, role=role, principal=principal)
    
    def assign_to_capacity(self, capacity_id, wait_for_completion=True):
        """Assign the workspace to a capacity
        Args:
            capacity_id (str): The id of the capacity to assign the workspace to
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        response = self.core_client.assign_to_capacity(workspace_id=self.id, capacity_id=capacity_id, wait_for_completion=wait_for_completion)
        self.capacity_id = capacity_id
        return response
    
    def delete(self):
        """Delete the workspace
        
        Returns:
            int: The status code of the response
        """
        return self.core_client.delete_workspace(workspace_id=self.id)
    

    def delete_role_assignment(self, workspace_role_assignment_id):
        """Delete a role assignment from the workspace
        Args:
            workspace_role_assignment_id (str): The id of the role assignment to delete
        Returns:
            int: The status code of the response
        """
        return self.core_client.delete_workspace_role_assignment(workspace_id=self.id, workspace_role_assignment_id=workspace_role_assignment_id)
    
    def deprovision_identity(self):
        """Deprovision identity for the workspace

        Returns:
            int: The status code of the response"""
        return self.core_client.deprovision_identity(workspace_id=self.id)

    
    def get_role_assignment(self, workspace_role_assignment_id):
        """Get a role assignment from the workspace
        Args:
            workspace_role_assignment_id (str): The id of the role assignment to get
        Returns:
            dict: The role assignment
        """

        return self.core_client.get_workspace_role_assignment(workspace_id=self.id, workspace_role_assignment_id=workspace_role_assignment_id)

    def list_role_assignments(self):
        """List role assignments for the workspace
        Returns:
            list: A list of role assignments
        """
        return self.core_client.list_workspace_role_assignments(workspace_id = self.id)
    
    def provision_identity(self):
        """Provision identity for the workspace
        Returns:
            dict: The identity
        """
        return self.core_client.provision_identity(workspace_id=self.id)
    
    def unassign_from_capacity(self, wait_for_completion=False):
        """Unassign the workspace from a capacity
        Args:
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        response_status_code = self.core_client.unassign_from_capacity(workspace_id=self.id,
                                                                       wait_for_completion = wait_for_completion)
        self.capacity_id = None
        return response_status_code
    
    def update(self, display_name = None, description = None):
        """Update the workspace
        Args:
            display_name (str): The new display name for the workspace
            description (str): The new description for the workspace
        Returns:
            Workspace: The updated workspace object
        """
        self.core_client.update_workspace(workspace_id=self.id, display_name=display_name, description=description)

        if display_name:
            self.display_name = display_name
        if description:
            self.description = description

        return self
    
    def update_role_assignment(self, role, workspace_role_assignment_id):
        """Update a role assignment in the workspace
        Args:
            role (str): The new role to assign
            workspace_role_assignment_id (str): The id of the role assignment to update
        Returns:
            int: The status code of the response
        """

        return self.core_client.update_workspace_role_assignment(workspace_id=self.id, role=role, workspace_role_assignment_id=workspace_role_assignment_id)


    # External Data Shares

    # create

    def create_external_data_share(self, item_id, paths, recipient):
        return self.core_client.create_external_data_share(workspace_id=self.id, item_id=item_id, paths=paths, recipient=recipient)

    # get

    def get_external_data_share(self, item_id, external_data_share_id):
        return self.core_client.get_external_data_share(workspace_id=self.id, item_id=item_id, external_data_share_id=external_data_share_id)

    # list

    def list_external_data_shares_in_item(self, item_id):
        return self.core_client.list_external_data_shares_in_item(workspace_id=self.id, item_id=item_id)

    # revoke

    def revoke_external_data_share(self, item_id, external_data_share_id):
        return self.core_client.revoke_external_data_share(workspace_id=self.id, item_id=item_id, external_data_share_id=external_data_share_id)
    

    # Item specific operations

    def create_item(self, display_name, type, definition = None, description = None, **kwargs):
        """Create an item in a workspace"""

        return self.core_client.create_item(workspace_id=self.id, display_name=display_name, 
                                            type=type, definition=definition, description=description, **kwargs)
         


    
    def get_item(self, item_id = None, item_name = None, item_type = None):
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}
        """Get an item from a workspace"""
        return self.core_client.get_item(workspace_id=self.id, item_id=item_id, item_name=item_name, item_type=item_type)

    def delete_item(self, item_id, type = None):
        """Delete an item from a workspace"""
        return self.core_client.delete_item(workspace_id=self.id, item_id=item_id, type=type)
  
    def list_items(self, with_properties = False, type = None):
        """List items in a workspace"""

        return self.core_client.list_items(workspace_id=self.id, with_properties=with_properties,
                                           type=type)
    
    def list_item_connections(self, item_id):
        """List connections of an item in a workspace"""
        return self.core_client.list_item_connections(workspace_id=self.id, item_id=item_id)

    def get_item_definition(self, item_id, type = None, format = None):
        """Get the definition of an item from a workspace"""
        return self.core_client.get_item_definition(workspace_id=self.id, item_id=item_id, type=type, format=format)

    def update_item(self, item_id, display_name = None, description = None, return_item=False):
        """Update an item in a workspace"""
        return self.core_client.update_item(workspace_id=self.id,
                                            item_id=item_id, display_name=display_name, description=description,
                                            return_item=return_item)
    
    def update_item_definition(self, item_id, definition):
        """Update the definition of an item in a workspace"""
        return self.core_client.update_item_definition(workspace_id=self.id, item_id=item_id, definition=definition)
    

    def create_shortcut(self, item_id, path, name, target):
        return self.core_client.create_shortcut(workspace_id=self.id, item_id=item_id, 
                                                path=path, name=name, target=target)
        
    def delete_shortcut(self, item_id, path, name):
        return self.core_client.delete_shortcut(self.id, item_id, path=path, name=name)
    
    def get_shortcut(self, item_id, path, name):
        return self.core_client.get_shortcut(self.id, item_id, path=path, name=name)
    
    def list_shortcuts(self, item_id, parent_path = None):
        return self.core_client.list_shortcuts(self.id, item_id, parent_path=parent_path)

    def reset_shortcut_cache(self, wait_for_completion = False):
        return self.core_client.reset_shortcut_cache(self.id, wait_for_completion=wait_for_completion)

    def cancel_item_job_instance(self, item_id, job_instance_id):
        return self.core_client.cancel_item_job_instance(workspace_id=self.id, item_id=item_id,
                                                         job_instance_id=job_instance_id)
    
    def create_item_schedule(self, item_id, job_type, configuration, enabled):
        return self.core_client.create_item_schedule(workspace_id=self.id, item_id=item_id, job_type=job_type,
                                                     configuration=configuration, enabled=enabled)
    
    def get_item_job_instance(self, item_id, job_instance_id):
        return self.core_client.get_item_job_instance(workspace_id=self.id, item_id=item_id,
                                                      job_instance_id=job_instance_id)

    def get_item_schedule(self, item_id, job_type, schedule_id):
        return self.core_client.get_item_schedule(workspace_id=self.id, item_id=item_id, job_type=job_type, schedule_id=schedule_id)
    
    def list_item_job_instances(self, item_id):
        return self.core_client.list_item_job_instances(workspace_id=self.id, item_id=item_id)
    
    def list_item_schedules(self, item_id, job_type):
        return self.core_client.list_item_schedules(workspace_id=self.id, item_id=item_id, job_type=job_type)

    def run_on_demand_item_job(self, item_id, job_type, execution_data = None):
        return self.core_client.run_on_demand_item_job(workspace_id=self.id, item_id=item_id,
                                                       job_type=job_type, execution_data=execution_data)
    
    def update_item_schedule(self, item_id, job_type, schedule_id, configuration, enabled):
        return self.core_client.update_item_schedule(workspace_id=self.id, item_id=item_id, job_type=job_type,
                                                    schedule_id=schedule_id, configuration=configuration, enabled=enabled)


    def commit_to_git(self, mode, comment=None, items=None, workspace_head=None):
        return self.core_client.commit_to_git(workspace_id=self.id, mode=mode, comment=comment,
                                              items=items, workspace_head=workspace_head)


    def git_connect(self, git_provider_details):
        return self.core_client.git_connect(workspace_id=self.id, git_provider_details=git_provider_details)

    def git_disconnect(self):
        return self.core_client.git_disconnect(workspace_id=self.id)

    def git_initialize_connection(self, initialization_strategy):
        return self.core_client.git_initialize_connection(workspace_id=self.id,
                                                          initialization_strategy=initialization_strategy)
    def git_get_connection(self):
        return self.core_client.git_get_connection(workspace_id=self.id)
 
    def get_my_git_credentials(self):
        return self.core_client.get_my_git_credentials(workspace_id=self.id)
    
    def git_get_status(self):
        return self.core_client.git_get_status(workspace_id=self.id)

    def update_from_git(self, remote_commit_hash, conflict_resolution = None, options = None, workspace_head = None):
        return self.core_client.update_from_git(workspace_id=self.id, remote_commit_hash=remote_commit_hash,
                                               conflict_resolution=conflict_resolution,
                                               options=options, workspace_head=workspace_head)
    
    def update_my_git_credentials(self, git_credentials):
        return self.core_client.update_my_git_credentials(workspace_id=self.id, git_credentials=git_credentials)

    # Managed Private Endpoints:

    def create_workspace_managed_private_endpoint(self, name, target_private_link_resource_id,
                                                    target_subresource_type, request_message = None):
        return self.core_client.create_workspace_managed_private_endpoint(workspace_id=self.id, name=name,
                                                                         target_private_link_resource_id=target_private_link_resource_id,
                                                                         target_subresource_type=target_subresource_type,
                                                                         request_message=request_message)
        
    def delete_workspace_managed_private_endpoint(self, managed_private_endpoint_id):
        return self.core_client.delete_workspace_managed_private_endpoint(workspace_id=self.id,
                                                                          managed_private_endpoint_id=managed_private_endpoint_id)

    def get_workspace_managed_private_endpoint(self, managed_private_endpoint_id):
        return self.core_client.get_workspace_managed_private_endpoint(workspace_id=self.id,
                                                                      managed_private_endpoint_id=managed_private_endpoint_id)

    def list_workspace_managed_private_endpoints(self):
        return self.core_client.list_workspace_managed_private_endpoints(workspace_id=self.id)

    # One Lake Data Access Security

    # create and update

    def create_or_update_data_access_roles(self, item_id, data_access_roles, dryrun = False, etag_match = None):
        return self.core_client.create_or_update_data_access_roles(workspace_id=self.id, item_id=item_id, data_access_roles=data_access_roles,
                                                                   dryrun=dryrun, etag_match=etag_match)
    
    # list 

    def list_data_access_roles(self, item_id):
        return self.core_client.list_data_access_roles(workspace_id=self.id, item_id=item_id)
    
    # List other items

    def list_dashboards(self):
        return self.core_client.list_dashboards(workspace_id=self.id)
    
    def list_datamarts(self):
        return self.core_client.list_datamarts(workspace_id=self.id)

    def list_sql_endpoints(self):
        return self.core_client.list_sql_endpoints(workspace_id=self.id)
    
    def list_mirrored_warehouses(self):
        return self.core_client.list_mirrored_warehouses(workspace_id=self.id)

    # datapipelines

    def create_data_pipeline(self, display_name, definition = None, description = None):
        return self.core_client.create_data_pipeline(workspace_id=self.id, display_name=display_name,
                                                    definition=definition, description=description)

    def list_data_pipelines(self, with_properties = False):
        return self.core_client.list_data_pipelines(workspace_id=self.id, with_properties=with_properties)
    
    def get_data_pipeline(self, data_pipeline_id = None, data_pipeline_name = None):
        return self.core_client.get_data_pipeline(workspace_id=self.id, data_pipeline_id=data_pipeline_id,
                                                 data_pipeline_name=data_pipeline_name)
    
    def delete_data_pipeline(self, data_pipeline_id):
        return self.core_client.delete_data_pipeline(workspace_id=self.id, data_pipeline_id=data_pipeline_id)
    
    def update_data_pipeline(self, data_pipeline_id, display_name = None, description = None):
        return self.core_client.update_data_pipeline(workspace_id=self.id, data_pipeline_id=data_pipeline_id,
                                                    display_name=display_name, description=description)
    
    # environments

    def list_environments(self, with_properties = False):
        """List environments in a workspace"""
        return self.core_client.list_environments(workspace_id=self.id, with_properties=with_properties)
    
    def create_environment(self, display_name, description = None):
        """Create an environment in a workspace"""
        return self.core_client.create_environment(workspace_id=self.id, display_name=display_name, description=description)
    
    def get_environment(self, environment_id = None, environment_name = None):
        """Get an environment from a workspace"""
        return self.core_client.get_environment(workspace_id=self.id, environment_id=environment_id,
                                                environment_name=environment_name)
    
    def delete_environment(self, environment_id):
        """Delete an environment from a workspace"""
        return self.core_client.delete_environment(workspace_id=self.id, environment_id=environment_id)
    
    def update_environment(self, environment_id, display_name = None, description = None):
        """Update an environment in a workspace"""
        return self.core_client.update_environment(workspace_id=self.id, environment_id=environment_id,
                                                   display_name=display_name, description=description)
    
    # environment spark compute

    def get_published_settings(self, environment_id):
        return self.core_client.get_published_settings(workspace_id=self.id, environment_id=environment_id)
    
    def get_staging_settings(self, environment_id):
        return self.core_client.get_staging_settings(workspace_id=self.id, environment_id=environment_id)
    
    def update_staging_settings(self, environment_id,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        return self.core_client.update_staging_settings(workspace_id=self.id, environment_id=environment_id,
                                                       driver_cores=driver_cores, driver_memory=driver_memory,
                                                       dynamic_executor_allocation=dynamic_executor_allocation,
                                                       executor_cores=executor_cores, executor_memory=executor_memory,
                                                       instance_pool=instance_pool, runtime_version=runtime_version,
                                                       spark_properties=spark_properties)

    # environment spark libraries

    def get_published_libraries(self, environment_id):
        return self.core_client.get_published_libraries(workspace_id=self.id, environment_id=environment_id)
    
    def get_staging_libraries(self, environment_id):
        return self.core_client.get_staging_libraries(workspace_id=self.id, environment_id=environment_id)
    
    def upload_staging_library(self, environment_id, file_path):
        return self.core_client.upload_staging_library(workspace_id=self.id, environment_id=environment_id, file_path=file_path) 
    
    def publish_environment(self, environment_id):
        return self.core_client.publish_environment(workspace_id=self.id, environment_id=environment_id)
    
    def delete_staging_library(self, environment_id, library_to_delete):
        return self.core_client.delete_staging_library(workspace_id=self.id, environment_id=environment_id, library_to_delete=library_to_delete)
        
    def cancel_publish(self, environment_id):
        return self.core_client.cancel_publish(workspace_id=self.id, environment_id=environment_id)
    
    # eventhouses

    def list_eventhouses(self, with_properties = False):
        """List eventhouses in a workspace"""
        return self.core_client.list_eventhouses(workspace_id=self.id, with_properties=with_properties)
    
    def create_eventhouse(self, display_name, description = None):
        """Create an eventhouse in a workspace"""
        return self.core_client.create_eventhouse(workspace_id=self.id, display_name=display_name, description=description)
    
    def get_eventhouse(self, eventhouse_id = None, eventhouse_name = None):
        """Get an eventhouse from a workspace"""
        return self.core_client.get_eventhouse(workspace_id=self.id, eventhouse_id=eventhouse_id,
                                                eventhouse_name=eventhouse_name)
    
    def get_eventhouse_definition(self, eventhouse_id, format = None):
        """Get the definition of an eventhouse from a workspace"""
        return self.core_client.get_eventhouse_definition(workspace_id=self.id, eventhouse_id=eventhouse_id, format=format)

    def delete_eventhouse(self, eventhouse_id):
        """Delete an eventhouse from a workspace"""
        return self.core_client.delete_eventhouse(workspace_id=self.id, eventhouse_id=eventhouse_id)
    
    def update_eventhouse(self, eventhouse_id, display_name = None, description = None):
        """Update an eventhouse in a workspace"""
        return self.core_client.update_eventhouse(workspace_id=self.id, eventhouse_id=eventhouse_id,
                                                  display_name=display_name, description=description)

    def update_eventhouse_definition(self, eventhouse_id, definition, update_metadata = None):
        """Update the definition of an eventhouse in a workspace"""
        return self.core_client.update_eventhouse_definition(workspace_id=self.id, eventhouse_id=eventhouse_id,
                                                             definition=definition, update_metadata=update_metadata)

    # eventstreams


    def create_eventstream(self, display_name, description = None):
        """Create an eventstream in a workspace"""
        return self.core_client.create_eventstream(workspace_id=self.id, display_name=display_name, description=description)
    
    def delete_eventstream(self, eventstream_id):
        """Delete an eventstream from a workspace"""
        return self.core_client.delete_eventstream(workspace_id=self.id, eventstream_id=eventstream_id)
    
    def get_eventstream(self, eventstream_id = None, eventstream_name = None):
        return self.core_client.get_eventstream(workspace_id=self.id, eventstream_id=eventstream_id, eventstream_name=eventstream_name)
    
    def get_eventstream_definition(self, eventstream_id, format = None):
        """Get the definition of an eventstream from a workspace"""
        return self.core_client.get_eventstream_definition(workspace_id=self.id, eventstream_id=eventstream_id, format=format)

    def list_eventstreams(self, with_properties = False):
        """List eventstreams in a workspace"""
        return self.core_client.list_eventstreams(workspace_id=self.id, with_properties=with_properties)
    
    def update_eventstream(self, eventstream_id, display_name = None, description = None):
        """Update an eventstream in a workspace"""
        return self.core_client.update_eventstream(workspace_id=self.id, eventstream_id=eventstream_id,
                                                  display_name=display_name, description=description)
    
    def update_eventstream_definition(self, eventstream_id, definition, update_metadata = None):
        """Update the definition of an eventstream in a workspace"""
        return self.core_client.update_eventstream_definition(workspace_id=self.id, eventstream_id=eventstream_id,
                                                             definition=definition, update_metadata=update_metadata)

    # graphQLapis

    def create_graphql_api(self, display_name, description = None):
        """Create a graphQL api in a workspace"""
        return self.core_client.create_graphql_api(workspace_id=self.id, display_name=display_name, description=description)
    
    def delete_graphql_api(self, graphql_api_id):
        """Delete a graphQL api from a workspace"""
        return self.core_client.delete_graphql_api(workspace_id=self.id, graphql_api_id=graphql_api_id)
    
    def get_graphql_api(self, graphql_api_id = None, graphql_api_name = None):
        """Get a graphQL api from a workspace"""
        return self.core_client.get_graphql_api(workspace_id=self.id, graphql_api_id=graphql_api_id, graphql_api_name=graphql_api_name)
    
    def list_graphql_apis(self, with_properties = False):   
        """List graphQL apis in a workspace"""
        return self.core_client.list_graphql_apis(workspace_id=self.id, with_properties=with_properties)

    def update_graphql_api(self, graphql_api_id, display_name = None, description = None):
        """Update a graphQL api in a workspace"""
        return self.core_client.update_graphql_api(workspace_id=self.id, graphql_api_id=graphql_api_id,
                                                 display_name=display_name, description=description)

    # kqlDashboards

    def create_kql_dashboard(self, display_name, description = None):
        """Create a kql dashboard in a workspace"""
        return self.core_client.create_kql_dashboard(workspace_id=self.id, display_name=display_name, description=description)
    
    def delete_kql_dashboard(self, kql_dashboard_id):
        """Delete a kql dashboard from a workspace"""
        return self.core_client.delete_kql_dashboard(workspace_id=self.id, kql_dashboard_id=kql_dashboard_id)
    
    def get_kql_dashboard(self, kql_dashboard_id = None, kql_dashboard_name = None):
        """Get a kql dashboard from a workspace"""
        return self.core_client.get_kql_dashboard(workspace_id=self.id, kql_dashboard_id=kql_dashboard_id,
                                                kql_dashboard_name=kql_dashboard_name)
    
    def get_kql_dashboard_definition(self, kql_dashboard_id, format = None):
        """Get the definition of a kql dashboard from a workspace"""
        return self.core_client.get_kql_dashboard_definition(workspace_id=self.id, kql_dashboard_id=kql_dashboard_id, format=format)
    
    def list_kql_dashboards(self, with_properties = False):
        """List kql dashboards in a workspace"""
        return self.core_client.list_kql_dashboards(workspace_id=self.id, with_properties=with_properties)
    
    def update_kql_dashboard(self, kql_dashboard_id, display_name = None, description = None):
        """Update a kql dashboard in a workspace"""
        return self.core_client.update_kql_dashboard(workspace_id=self.id, kql_dashboard_id=kql_dashboard_id,
                                                    display_name=display_name, description=description)
    
    def update_kql_dashboard_definition(self, kql_dashboard_id, definition, update_metadata = None):
        """Update the definition of a kql dashboard in a workspace"""
        return self.core_client.update_kql_dashboard_definition(workspace_id=self.id, kql_dashboard_id=kql_dashboard_id,
                                                                definition=definition, update_metadata=update_metadata)
    

    # kqlDatabases

    def create_kql_database(self, creation_payload, display_name, description = None, ):
        """Create a kql database in a workspace"""
        return self.core_client.create_kql_database(workspace_id=self.id, creation_payload=creation_payload,
                                                    display_name=display_name, description=description)
    def delete_kql_database(self, kql_database_id):
        """Delete a kql database from a workspace"""
        return self.core_client.delete_kql_database(workspace_id=self.id, kql_database_id=kql_database_id)
    
    def get_kql_database(self, kql_database_id = None, kql_database_name = None):
        """Get a kql database from a workspace"""
        return self.core_client.get_kql_database(workspace_id=self.id, kql_database_id=kql_database_id,
                                                  kql_database_name=kql_database_name)
    
    def get_kql_database_definition(self, kql_database_id, format = None):
        """Get the definition of a kql database from a workspace"""
        return self.core_client.get_kql_database_definition(workspace_id=self.id, kql_database_id=kql_database_id, format=format)
    
    def list_kql_databases(self, with_properties = False):
        """List kql databases in a workspace"""
        return self.core_client.list_kql_databases(workspace_id=self.id, with_properties=with_properties)
    
    def update_kql_database(self, kql_database_id, display_name = None, description = None):
        """Update a kql database in a workspace"""
        return self.core_client.update_kql_database(workspace_id=self.id, kql_database_id=kql_database_id,
                                                  display_name=display_name, description=description)

    def update_kql_database_definition(self, kql_database_id, definition, update_metadata = None):
        """Update the definition of a kql database in a workspace"""
        return self.core_client.update_kql_database_definition(workspace_id=self.id, kql_database_id=kql_database_id,
                                                              definition=definition, update_metadata=update_metadata)

    # kqlQuerysets

    def create_kql_queryset(self, display_name, description = None, definition = None):
        """Create a kql queryset in a workspace"""
        return self.core_client.create_kql_queryset(workspace_id=self.id, display_name=display_name, description=description,
                                                    definition=definition)

    def delete_kql_queryset(self, kql_queryset_id):
        """Delete a kql queryset from a workspace"""
        return self.core_client.delete_kql_queryset(workspace_id=self.id, kql_queryset_id=kql_queryset_id)

    def get_kql_queryset(self, kql_queryset_id = None, kql_queryset_name = None):
        """Get a kql queryset from a workspace"""
        return self.core_client.get_kql_queryset(self.id, kql_queryset_id, kql_queryset_name)
    
    def get_kql_queryset_definition(self, kql_queryset_id, format = None):
        """Get the definition of a kql queryset from a workspace"""
        return self.core_client.get_kql_queryset_definition(workspace_id=self.id, kql_queryset_id=kql_queryset_id, format=format)

    def list_kql_querysets(self, with_properties = False):
        """List kql querysets in a workspace"""
        return self.core_client.list_kql_querysets(workspace_id=self.id, with_properties=with_properties)

    def update_kql_queryset(self, kql_queryset_id, display_name = None, description = None):
        """Update a kql queryset in a workspace"""
        return self.core_client.update_kql_queryset(workspace_id=self.id, kql_queryset_id=kql_queryset_id,
                                                    display_name=display_name, description=description)
    
    def update_kql_queryset_definition(self, kql_queryset_id, definition, update_metadata = None):
        """Update the definition of a kql queryset in a workspace"""
        return self.core_client.update_kql_queryset_definition(workspace_id=self.id, kql_queryset_id=kql_queryset_id,
                                                               definition=definition, update_metadata=update_metadata)

    # lakehouses
    def run_on_demand_table_maintenance(self, lakehouse_id, execution_data, 
                                        job_type = "TableMaintenance", wait_for_completion = True):
        """Run on demand table maintenance"""
        return self.core_client.run_on_demand_table_maintenance(workspace_id=self.id, lakehouse_id=lakehouse_id,
                                                                execution_data=execution_data, job_type=job_type,
                                                                wait_for_completion=wait_for_completion)

    def create_lakehouse(self, display_name, description = None):
        """Create a lakehouse in a workspace"""
        return self.core_client.create_lakehouse(workspace_id=self.id, display_name=display_name, description=description)
    
    def delete_lakehouse(self, lakehouse_id):
        """Delete a lakehouse from a workspace"""
        return self.core_client.delete_lakehouse(workspace_id=self.id, lakehouse_id=lakehouse_id)
    
    def get_lakehouse(self, lakehouse_id = None, lakehouse_name = None):
        """Get a lakehouse from a workspace"""
        return self.core_client.get_lakehouse(workspace_id=self.id, lakehouse_id=lakehouse_id, lakehouse_name=lakehouse_name)
        
    def list_lakehouses(self, with_properties = False):
        """List lakehouses in a workspace"""
        return self.core_client.list_lakehouses(workspace_id=self.id, with_properties=with_properties)
    
    def update_lakehouse(self, lakehouse_id, display_name = None, description = None):
        """Update a lakehouse in a workspace"""
        return self.core_client.update_lakehouse(workspace_id=self.id, lakehouse_id=lakehouse_id,
                                                 display_name=display_name, description=description)
    
    def list_tables(self, lakehouse_id):
        """List tables in a workspace"""
        return self.core_client.list_tables(workspace_id=self.id, lakehouse_id=lakehouse_id)
    
    def load_table(self, lakehouse_id, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        
        return self.core_client.load_table(workspace_id=self.id, lakehouse_id=lakehouse_id, table_name=table_name,
                                            path_type=path_type, relative_path=relative_path,
                                            file_extension=file_extension, format_options=format_options,
                                            mode=mode, recursive=recursive, wait_for_completion=wait_for_completion)
    
    # mirroredDatabases

    def create_mirrored_database(self, display_name, description = None, definition = None):
        return self.core_client.create_mirrored_database(workspace_id=self.id, display_name=display_name, description=description,
                                                         definition=definition)
    
    def delete_mirrored_database(self, mirrored_database_id):
        return self.core_client.delete_mirrored_database(workspace_id=self.id, mirrored_database_id=mirrored_database_id)
    
    def get_mirrored_database(self, mirrored_database_id = None, mirrored_database_name = None):
        return self.core_client.get_mirrored_database(workspace_id=self.id, mirrored_database_id=mirrored_database_id,
                                                     mirrored_database_name=mirrored_database_name)
    
    def get_mirrored_database_definition(self, mirrored_database_id):
        return self.core_client.get_mirrored_database_definition(workspace_id=self.id,
                                                                 mirrored_database_id=mirrored_database_id)
    
    def list_mirrored_databases(self, with_properties = False):
        return self.core_client.list_mirrored_databases(workspace_id=self.id, with_properties=with_properties)
    
    def update_mirrored_database(self, mirrored_database_id, display_name = None, description = None, return_item = False):
        return self.core_client.update_mirrored_database(workspace_id=self.id, mirrored_database_id=mirrored_database_id,
                                                         display_name=display_name, description=description, return_item=return_item)
    
    def update_mirrored_database_definition(self, mirrored_database_id, definition):
        return self.core_client.update_mirrored_database_definition(workspace_id=self.id, mirrored_database_id=mirrored_database_id,
                                                                   definition=definition)

    def get_mirroring_status(self, mirrored_database_id):
        return self.core_client.get_mirroring_status(workspace_id=self.id, mirrored_database_id=mirrored_database_id)

    def get_tables_mirroring_status(self, mirrored_database_id):
        return self.core_client.get_tables_mirroring_status(workspace_id=self.id, mirrored_database_id=mirrored_database_id)
      
    def start_mirroring(self, mirrored_database_id):
        return self.core_client.start_mirroring(workspace_id=self.id, mirrored_database_id=mirrored_database_id)

    def stop_mirroring(self, mirrored_database_id):
        return self.core_client.stop_mirroring(workspace_id=self.id, mirrored_database_id=mirrored_database_id)

    # mlExperiments

    def create_ml_experiment(self, display_name, description = None):
        """Create an ml experiment in a workspace"""
        return self.core_client.create_ml_experiment(workspace_id=self.id, display_name=display_name, description=description)
    
    def delete_ml_experiment(self, ml_experiment_id):
        """Delete an ml experiment from a workspace"""
        return self.core_client.delete_ml_experiment(workspace_id=self.id, ml_experiment_id=ml_experiment_id)

    def get_ml_experiment(self, ml_experiment_id = None, ml_experiment_name = None):
        """Get an ml experiment from a workspace"""
        return self.core_client.get_ml_experiment(workspace_id=self.id, ml_experiment_id=ml_experiment_id, ml_experiment_name=ml_experiment_name)

    def list_ml_experiments(self, with_properties = False):
        """List ml experiments in a workspace"""
        return self.core_client.list_ml_experiments(workspace_id=self.id, with_properties=with_properties)
    
    def update_ml_experiment(self, ml_experiment_id, display_name = None, description = None):
        """Update an ml experiment in a workspace"""
        return self.core_client.update_ml_experiment(workspace_id=self.id, ml_experiment_id=ml_experiment_id, display_name=display_name, description=description)
    
    # mlModels

    def list_ml_models(self, with_properties = False):
        """List ml models in a workspace"""
        return self.core_client.list_ml_models(workspace_id=self.id, with_properties=with_properties)

    def create_ml_model(self, display_name, description = None):
        """Create an ml model in a workspace"""
        return self.core_client.create_ml_model(workspace_id=self.id, display_name=display_name, description=description)
    
    def get_ml_model(self, ml_model_id = None, ml_model_name = None):
        """Get an ml model from a workspace"""
        return self.core_client.get_ml_model(workspace_id=self.id, ml_model_id=ml_model_id, ml_model_name=ml_model_name)
    
    def delete_ml_model(self, ml_model_id):
        """Delete an ml model from a workspace"""
        return self.core_client.delete_ml_model(workspace_id=self.id, ml_model_id=ml_model_id)
    
    def update_ml_model(self, ml_model_id, display_name = None, description = None):
        """Update an ml model in a workspace"""
        return self.core_client.update_ml_model(workspace_id=self.id, ml_model_id=ml_model_id, display_name=display_name, description=description)
    
    # mounted data factory

    def create_mounted_data_factory(self, display_name, description = None, definition = None):
        """Create a mounted data factory in a workspace"""
        return self.core_client.create_mounted_data_factory(workspace_id=self.id, display_name=display_name,
                                                          description=description, definition=definition)

    def delete_mounted_data_factory(self, mounted_data_factory_id):
        """Delete a mounted data factory from a workspace"""
        return self.core_client.delete_mounted_data_factory(workspace_id=self.id, mounted_data_factory_id=mounted_data_factory_id)
    
    def get_mounted_data_factory(self, mounted_data_factory_id = None, mounted_data_factory_name = None):
        """Get a mounted data factory from a workspace"""
        return self.core_client.get_mounted_data_factory(workspace_id=self.id, mounted_data_factory_id=mounted_data_factory_id,
                                                      mounted_data_factory_name=mounted_data_factory_name)
    
    def get_mounted_data_factory_definition(self, mounted_data_factory_id, format = None):
        """Get the definition of a mounted data factory from a workspace"""
        return self.core_client.get_mounted_data_factory_definition(workspace_id=self.id, mounted_data_factory_id=mounted_data_factory_id, format=format)
    
    def list_mounted_data_factories(self, with_properties = False):
        """List mounted data factories in a workspace"""
        return self.core_client.list_mounted_data_factories(workspace_id=self.id, with_properties=with_properties)
    
    def update_mounted_data_factory(self, mounted_data_factory_id, display_name = None, description = None):
        """Update a mounted data factory in a workspace"""
        return self.core_client.update_mounted_data_factory(workspace_id=self.id, mounted_data_factory_id=mounted_data_factory_id,
                                                         display_name=display_name, description=description)
    
    def update_mounted_data_factory_definition(self, mounted_data_factory_id, definition, update_metadata = None):
        """Update the definition of a mounted data factory in a workspace"""
        return self.core_client.update_mounted_data_factory_definition(workspace_id=self.id, mounted_data_factory_id=mounted_data_factory_id, definition=definition,
                                                                       update_metadata=update_metadata)

    # notebooks

    def create_notebook(self, display_name, definition = None, description = None):
        """Create a notebook in a workspace"""
        return self.core_client.create_notebook(workspace_id=self.id, display_name=display_name,
                                                definition=definition, description=description)

    def delete_notebook(self, notebook_id):
        """Delete a notebook from a workspace"""
        return self.core_client.delete_notebook(workspace_id=self.id, notebook_id=notebook_id)

    def get_notebook(self, notebook_id = None, notebook_name = None):
        """Get a notebook from a workspace"""
        return self.core_client.get_notebook(workspace_id=self.id, notebook_id=notebook_id, notebook_name=notebook_name)
    
    def get_notebook_definition(self, notebook_id, format = None):
        """Get the definition of a notebook from a workspace"""
        return self.core_client.get_notebook_definition(workspace_id=self.id, notebook_id=notebook_id, format=format)

    def list_notebooks(self, with_properties = False):
        """List notebooks in a workspace"""
        return self.core_client.list_notebooks(workspace_id=self.id, with_properties=with_properties)
    
    def update_notebook(self, notebook_id, display_name = None, description = None):
        """Update a notebook in a workspace"""
        return self.core_client.update_notebook(workspace_id=self.id, notebook_id=notebook_id, display_name=display_name, description=description)

    def update_notebook_definition(self, notebook_id, definition):
        """Update the definition of a notebook in a workspace"""
        return self.core_client.update_notebook_definition(workspace_id=self.id, notebook_id=notebook_id, definition=definition)
    
    # paginated reports
        
    def list_paginated_reports(self):
        return self.core_client.list_paginated_reports(workspace_id=self.id)
    
    def update_paginated_report(self, paginated_report_id, display_name = None, description = None):
        return self.core_client.update_paginated_report(workspace_id=self.id, paginated_report_id=paginated_report_id,
                                                       display_name=display_name, description=description)

    # reflex

    def create_reflex(self, display_name, description = None):
        """Create a reflex in a workspace"""
        return self.core_client.create_reflex(workspace_id=self.id, display_name=display_name, description=description)

    def delete_reflex(self, reflex_id):
        """Delete a reflex from a workspace"""
        return self.core_client.delete_reflex(workspace_id=self.id, reflex_id=reflex_id)
    
    def get_reflex(self, reflex_id = None, reflex_name = None):
        """Get a reflex from a workspace"""
        return self.core_client.get_reflex(workspace_id=self.id, reflex_id=reflex_id, reflex_name=reflex_name)
    
    def get_reflex_definition(self, reflex_id, format = None):
        """Get the definition of a reflex from a workspace"""
        return self.core_client.get_reflex_definition(workspace_id=self.id, reflex_id=reflex_id, format=format)

    def list_reflexes(self, with_properties = False):
        """List reflexes in a workspace"""
        return self.core_client.list_reflexes(workspace_id=self.id, with_properties=with_properties)
    
    def update_reflex(self, reflex_id, display_name = None, description = None):
        """Update a reflex in a workspace"""
        return self.core_client.update_reflex(workspace_id=self.id, reflex_id=reflex_id, display_name=display_name, description=description)
    
    def update_reflex_definition(self, reflex_id, definition, update_metadata = None):
        """Update the definition of a reflex in a workspace"""
        return self.core_client.update_reflex_definition(workspace_id=self.id, reflex_id=reflex_id, definition=definition,
                                                       update_metadata=update_metadata)


    # reports

    def create_report(self, display_name, definition = None, description = None):
        """Create a report in a workspace"""
        return self.core_client.create_report(workspace_id=self.id, display_name=display_name,
                                              definition=definition, description=description)
    def delete_report(self, report_id):
        """Delete a report from a workspace"""
        return self.core_client.delete_report(workspace_id=self.id, report_id=report_id)
    
    def get_report(self, report_id = None, report_name = None):
        """Get a report from a workspace"""
        return self.core_client.get_report(workspace_id=self.id, report_id=report_id, report_name=report_name)
    
    def get_report_definition(self, report_id, format = None):
        """Get the definition of a report from a workspace"""
        return self.core_client.get_report_definition(workspace_id=self.id, report_id=report_id, format=format)

    def list_reports(self, with_properties = False):
        """List reports in a workspace"""
        return self.core_client.list_reports(workspace_id=self.id, with_properties=with_properties)
    
    def update_report(self, report_id, display_name = None, description = None):
        """Update a report in a workspace"""
        return self.core_client.update_report(workspace_id=self.id, report_id=report_id, display_name=display_name, description=description)
    
    def update_report_definition(self, report_id, definition):
        """Update the definition of a report in a workspace"""
        return self.core_client.update_report_definition(workspace_id=self.id, report_id=report_id, definition=definition)

    # semanticModels

    def list_semantic_models(self, with_properties = False):
        """List semantic models in a workspace"""
        return self.core_client.list_semantic_models(workspace_id=self.id, with_properties=with_properties)
    
    def create_semantic_model(self, display_name, definition = None, description = None):
        """Create a semantic model in a workspace"""
        return self.core_client.create_semantic_model(workspace_id=self.id, display_name=display_name,
                                                      definition=definition, description=description)
    
    def get_semantic_model(self, semantic_model_id = None, semantic_model_name = None):
        """Get a semantic model from a workspace"""
        return self.core_client.get_semantic_model(workspace_id=self.id, semantic_model_id=semantic_model_id,
                                                    semantic_model_name=semantic_model_name)
    
    def delete_semantic_model(self, semantic_model_id):
        """Delete a semantic model from a workspace"""
        return self.core_client.delete_semantic_model(workspace_id=self.id, semantic_model_id=semantic_model_id)
    
    def update_semantic_model(self, semantic_model_id, display_name = None, description = None):
        """Update a semantic model in a workspace"""
        return self.core_client.update_semantic_model(workspace_id=self.id, semantic_model_id=semantic_model_id,
                                                        display_name=display_name, description=description)
    
    def get_semantic_model_definition(self, semantic_model_id, format = None):
        """Get the definition of a semantic model from a workspace"""
        return self.core_client.get_semantic_model_definition(workspace_id=self.id, semantic_model_id=semantic_model_id, format=format)

    def update_semantic_model_definition(self, semantic_model_id, definition):
        """Update the definition of a semantic model in a workspace"""
        return self.core_client.update_semantic_model_definition(workspace_id=self.id, semantic_model_id=semantic_model_id, definition=definition)

    # spark workspace custom pools

    def list_workspace_custom_pools(self):
        """List spark worspace custom pools in a workspace"""
        return self.core_client.list_workspace_custom_pools(workspace_id=self.id)
    
    def create_workspace_custom_pool(self, name, node_family, node_size, auto_scale, dynamic_executor_allocation):
        """Create a custom pool in a workspace"""
        return self.core_client.create_workspace_custom_pool(workspace_id=self.id, name=name, node_family=node_family,
                                                            node_size=node_size, auto_scale=auto_scale,
                                                            dynamic_executor_allocation=dynamic_executor_allocation)

    def get_workspace_custom_pool(self, pool_id):
        """Get a custom pool in a workspace"""
        return self.core_client.get_workspace_custom_pool(workspace_id=self.id, pool_id=pool_id)
    
    def delete_workspace_custom_pool(self, pool_id):
        """Delete a custom pool in a workspace"""
        return self.core_client.delete_workspace_custom_pool(workspace_id=self.id, pool_id=pool_id)
    
    def update_workspace_custom_pool(self, pool_id, name = None , node_family = None, node_size = None,
                                     auto_scale = None,
                                    dynamic_executor_allocation = None):
        """Update a custom pool in a workspace"""
        return self.core_client.update_workspace_custom_pool(workspace_id=self.id, pool_id=pool_id, name=name,
                                                            node_family=node_family, node_size=node_size,
                                                            auto_scale=auto_scale,
                                                            dynamic_executor_allocation=dynamic_executor_allocation)
    
    # spark workspace settings

    def get_spark_settings(self):
        return self.core_client.get_spark_settings(workspace_id=self.id)
    
    def update_spark_settings(self, automatic_log = None, environment = None, high_concurrency = None, pool = None):
        return self.core_client.update_spark_settings(workspace_id=self.id, automatic_log=automatic_log,
                                                      environment=environment, high_concurrency=high_concurrency, pool=pool)

    # sparkJobDefinitions

    def list_spark_job_definitions(self, with_properties = False):
        """List spark job definitions in a workspace"""
        return self.core_client.list_spark_job_definitions(workspace_id=self.id, with_properties=with_properties)
    
    def create_spark_job_definition(self, display_name, definition = None, description = None):
        """Create a spark job definition in a workspace"""
        return self.core_client.create_spark_job_definition(workspace_id=self.id, display_name=display_name,
                                                           definition=definition, description=description)
    
    def get_spark_job_definition(self, spark_job_definition_id = None, spark_job_definition_name = None):
        """Get a spark job definition from a workspace"""
        return self.core_client.get_spark_job_definition(workspace_id=self.id, spark_job_definition_id=spark_job_definition_id,
                                                       spark_job_definition_name=spark_job_definition_name)

    def delete_spark_job_definition(self, spark_job_definition_id):
        """Delete a spark job definition from a workspace"""
        return self.core_client.delete_spark_job_definition(workspace_id=self.id, spark_job_definition_id=spark_job_definition_id)
    
    def update_spark_job_definition(self, spark_job_definition_id, display_name = None, description = None):
        """Update a spark job definition in a workspace"""
        return self.core_client.update_spark_job_definition(workspace_id=self.id, spark_job_definition_id=spark_job_definition_id,
                                                            display_name=display_name, description=description)

    def get_spark_job_definition_definition(self, spark_job_definition_id, format = None):
        """Get the definition of a spark job definition from a workspace"""
        return self.core_client.get_spark_job_definition_definition(workspace_id=self.id, spark_job_definition_id=spark_job_definition_id, format=format)

    def update_spark_job_definition_definition(self, spark_job_definition_id, definition):
        """Update the definition of a spark job definition in a workspace"""
        return self.core_client.update_spark_job_definition_definition(workspace_id=self.id, spark_job_definition_id=spark_job_definition_id, definition=definition)

    def run_on_demand_spark_job_definition(self, spark_job_definition_id, job_type = "sparkjob"):
        """Run on demand spark job definition"""
        return self.core_client.run_on_demand_spark_job_definition(workspace_id=self.id, spark_job_definition_id=spark_job_definition_id, job_type=job_type)
    
    # sql databases

    def create_sql_database(self, display_name, description = None):
        """Create a sql database in a workspace"""
        return self.core_client.create_sql_database(workspace_id=self.id, display_name=display_name, description=description)
    
    def delete_sql_database(self, sql_database_id):
        """Delete a sql database from a workspace"""
        return self.core_client.delete_sql_database(workspace_id=self.id, sql_database_id=sql_database_id)
    
    def get_sql_database(self, sql_database_id = None, sql_database_name = None):
        """Get a sql database from a workspace"""
        return self.core_client.get_sql_database(workspace_id=self.id, sql_database_id=sql_database_id, sql_database_name=sql_database_name)

    def list_sql_databases(self, with_properties = False):
        """List sql databases in a workspace"""
        return self.core_client.list_sql_databases(workspace_id=self.id, with_properties=with_properties)
    
    def update_sql_database(self, sql_database_id, display_name = None, description = None):
        """Update a sql database in a workspace"""
        return self.core_client.update_sql_database(workspace_id=self.id, sql_database_id=sql_database_id,
                                                  display_name=display_name, description=description)

    # warehouses

    def list_warehouses(self, with_properties = False):
        """List warehouses in a workspace"""
        return self.core_client.list_warehouses(workspace_id=self.id, with_properties=with_properties)
    
    def create_warehouse(self, display_name, description = None):
        """Create a warehouse in a workspace"""
        return self.core_client.create_warehouse(workspace_id=self.id, display_name=display_name, description=description)
    
    def get_warehouse(self, warehouse_id = None, warehouse_name = None):
        """Get a warehouse from a workspace"""
        return self.core_client.get_warehouse(workspace_id=self.id, warehouse_id=warehouse_id, warehouse_name=warehouse_name)
    
    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse from a workspace"""
        return self.core_client.delete_warehouse(workspace_id=self.id, warehouse_id=warehouse_id)
    
    def update_warehouse(self, warehouse_id, display_name = None, description = None):
        """Update a warehouse in a workspace"""
        return self.core_client.update_warehouse(workspace_id=self.id, warehouse_id=warehouse_id, display_name=display_name, description=description)    

import json 

from msfabricpysdkcore.coreapi import FabricClientCore

class Item:
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, core_client: FabricClientCore, properties = None, definition=None, description="") -> None:
        
        self.id = id
        self.display_name = display_name
        self.description = description
        self.type = type
        self.definition = definition
        self.properties = properties
        self.workspace_id = workspace_id
        
        self.core_client = core_client

    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            'id': self.id,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.type,
            'definition': self.definition,
            'workspace_id': self.workspace_id,
            'properties': self.properties
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(item_dict, core_client):
        """Create Item object from dictionary"""
        
        return Item(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
                    properties=item_dict.get('properties', None),
                    definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def delete(self, type = None):
        """Delete the workspace item"""

        return self.core_client.delete_item(self.workspace_id, self.id, type=type)
    
    def get_definition(self, type = None, format = None, **kwargs):
        """Get the definition of the item"""
        resp_dict = self.core_client.get_item_definition(self.workspace_id, self.id, type=type, format=format, **kwargs)

        self.definition = resp_dict['definition']
        return resp_dict

    def list_connections(self):
        """List connections of an item in a workspace"""
        return self.core_client.list_item_connections(workspace_id=self.workspace_id, item_id=self.id)

    def update(self, display_name = None, description = None, type = None, return_item=False):
        """Update the item"""

        resp_dict = self.core_client.update_item(workspace_id=self.workspace_id, item_id=self.id,
                                                 display_name=display_name, description=description, type=type,
                                                 return_item=return_item)
        if display_name:
            self.display_name = display_name
        if description:
            self.description = description

        return resp_dict

    def update_definition(self, definition, type = None, **kwargs):
        """Update the item definition"""
        if not type:
            type = self.type
        response = self.core_client.update_item_definition(workspace_id=self.workspace_id, item_id=self.id, 
                                                           definition=definition, type=type, **kwargs)

        self.definition = definition 
        return response
    
    # Tags   
    def apply_tags(self, tags):
        """Apply tags to an item in a workspace"""
        return self.core_client.apply_tags(workspace_id=self.workspace_id, item_id=self.id, tags=tags)
    
    def unapply_tags(self, tags):
        """Unapply tags from an item in a workspace"""
        return self.core_client.unapply_tags(workspace_id=self.workspace_id, item_id=self.id, tags=tags)
    
    # Shortcut

    def create_shortcut(self, path, name, target):
        """Create a shortcut in the item"""
        return self.core_client.create_shortcut(workspace_id=self.workspace_id, item_id=self.id,
                                                path=path, name=name, target=target)
    
    def delete_shortcut(self, path, name):
        """Delete the shortcut in the item"""
        return self.core_client.delete_shortcut(workspace_id=self.workspace_id, item_id=self.id,
                                                path=path, name=name)

    def get_shortcut(self, path, name):
        """Get the shortcut in the item"""
        return self.core_client.get_shortcut(workspace_id=self.workspace_id, item_id=self.id,
                                                path=path, name=name)
    
    def list_shortcuts(self, parent_path = None):
        return self.core_client.list_shortcuts(workspace_id=self.workspace_id, item_id=self.id, parent_path=parent_path)

    # Job Scheduler

    def cancel_item_job_instance(self, job_instance_id):
        """Cancel a job instance ofjob the item"""
        return self.core_client.cancel_item_job_instance(workspace_id=self.workspace_id, item_id=self.id,
                                                         job_instance_id=job_instance_id)
    
    def create_item_schedule(self, job_type, configuration, enabled):
        """Create a schedule for the job instance"""
        return self.core_client.create_item_schedule(workspace_id=self.workspace_id,
                                                     item_id=self.id,
                                                     job_type=job_type,
                                                     configuration=configuration,
                                                     enabled=enabled)
    
    def get_item_job_instance(self, job_instance_id):
        """Get the job instance of the item"""
        return self.core_client.get_item_job_instance(workspace_id=self.workspace_id, item_id=self.id,
                                                      job_instance_id=job_instance_id)
    def get_item_schedule(self, job_type, schedule_id):
        """Get the schedule for the job instance"""
        return self.core_client.get_item_schedule(workspace_id=self.workspace_id,
                                                 item_id=self.id,
                                                 job_type=job_type,
                                                 schedule_id=schedule_id)
    
    def list_item_job_instances(self):
        """List all job instances for the job instance"""
        return self.core_client.list_item_job_instances(workspace_id=self.workspace_id,
                                                        item_id=self.id)                                      
    
    def list_item_schedules(self, job_type):
        """List all schedules for the job instance"""
        return self.core_client.list_item_schedules(workspace_id=self.workspace_id,
                                                  item_id=self.id,
                                                  job_type=job_type)

    def run_on_demand_item_job(self, job_type, execution_data = None):
        return self.core_client.run_on_demand_item_job(workspace_id=self.workspace_id, item_id=self.id,
                                                       job_type=job_type, execution_data=execution_data)
    
    def update_item_schedule(self, job_type, schedule_id, configuration, enabled):
        """Update the schedule for the job instance"""
        return self.core_client.update_item_schedule(workspace_id=self.workspace_id,
                                                     item_id=self.id,
                                                     job_type=job_type,
                                                     schedule_id=schedule_id,
                                                     configuration=configuration,
                                                     enabled=enabled)

    
    # External Data Shares

    def create_external_data_share(self, paths, recipient):
        return self.core_client.create_external_data_share(workspace_id=self.workspace_id, item_id=self.id,
                                                           paths=paths, recipient=recipient)

    def get_external_data_share(self, external_data_share_id):
        return self.core_client.get_external_data_share(workspace_id=self.workspace_id, item_id=self.id,
                                                       external_data_share_id=external_data_share_id)

    def list_external_data_shares_in_item(self):
        return self.core_client.list_external_data_shares_in_item(workspace_id=self.workspace_id, item_id=self.id)
    
    def revoke_external_data_share(self, external_data_share_id):
        return self.core_client.revoke_external_data_share(workspace_id=self.workspace_id, item_id=self.id,
                                                          external_data_share_id=external_data_share_id)

    # One Lake data access security

    def list_data_access_roles(self):
        return self.core_client.list_data_access_roles(workspace_id=self.workspace_id, item_id=self.id)
    
    def create_or_update_data_access_roles(self, data_access_roles, dryrun = False, etag_match = None):
        return self.core_client.create_or_update_data_access_roles(workspace_id=self.workspace_id, item_id=self.id,
                                                                     data_access_roles=data_access_roles, dryrun=dryrun, etag_match=etag_match)
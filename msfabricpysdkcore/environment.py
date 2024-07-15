from msfabricpysdkcore.item import Item

class Environment(Item):
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Environment(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""),
            auth=core_client)

    def get_published_settings(self):
        """Get the published settings of the environment"""
        return self.core_client.get_published_settings(self.workspace_id, self.id)
    
    def get_staging_settings(self):
        """Get the staging settings of the environment"""
        return self.core_client.get_staging_settings(self.workspace_id, self.id)


    def update_staging_settings(self,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        """Update the staging settings of the environment"""
        return self.core_client.update_staging_settings(self.workspace_id, self.id, driver_cores, driver_memory,
                                                        dynamic_executor_allocation, executor_cores, executor_memory,
                                                        instance_pool, runtime_version, spark_properties)

    def get_published_libraries(self):
        """Get the published libraries of the environment"""
        return self.core_client.get_published_libraries(self.workspace_id, self.id)
    
    def get_staging_libraries(self):
        """Get the staging libraries of the environment"""
        return self.core_client.get_staging_libraries(self.workspace_id, self.id)
    
    def upload_staging_library(self, file_path):
        return self.core_client.upload_staging_library(self.workspace_id, self.id, file_path)
    
    def delete_staging_library(self, library_to_delete):
        return self.core_client.delete_staging_library(self.workspace_id, self.id, library_to_delete)
    
    def publish_environment(self):
        return self.core_client.publish_environment(self.workspace_id, self.id) 

    def cancel_publish(self):
        return self.core_client.cancel_publish(self.workspace_id, self.id)
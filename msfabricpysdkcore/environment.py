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

    def cancel_publish(self):
        return self.core_client.cancel_publish(self.workspace_id, self.id)
    
    def publish_environment(self, preview="false"):
        return self.core_client.publish_environment(self.workspace_id, self.id, preview=preview)

    # published

    def export_published_external_libraries(self):
        """Export the external libraries of the environment"""
        return self.core_client.export_published_external_libraries(self.workspace_id, self.id)
    
    def get_published_spark_compute(self, preview="false"):
        """Get the spark compute settings of the environment"""
        return self.core_client.get_published_spark_compute(self.workspace_id, self.id, preview=preview)
    
    def get_published_settings(self, preview="false"):
        """Get the published settings of the environment"""
        return self.core_client.get_published_settings(self.workspace_id, self.id, preview=preview)
    
    def list_published_libraries(self, preview="false"):
        return self.core_client.list_published_libraries(workspace_id=self.workspace_id, environment_id=self.id, preview=preview)

    def get_published_libraries(self, preview="false"):
        """Get the published libraries of the environment"""
        return self.core_client.get_published_libraries(self.workspace_id, self.id, preview=preview)



   # staging

    def delete_custom_library(self, library_name):
        return self.core_client.delete_custom_library(workspace_id=self.workspace_id, environment_id=self.id, library_name=library_name)
    
    def delete_staging_library(self, library_to_delete):
        return self.core_client.delete_staging_library(self.workspace_id, self.id, library_to_delete)
    
    def export_staging_external_libraries(self):
        return self.core_client.export_staging_external_libraries(workspace_id=self.workspace_id, environment_id=self.id)

    def get_staging_spark_compute(self, preview="false"):
        return self.core_client.get_staging_spark_compute(workspace_id=self.workspace_id, environment_id=self.id, preview=preview)

    def get_staging_settings(self, preview="false"):
        """Get the staging settings of the environment"""
        return self.core_client.get_staging_settings(self.workspace_id, self.id, preview=preview)

    def import_external_libraries_to_staging(self, file_path):
        return self.core_client.import_external_libraries_to_staging(workspace_id=self.workspace_id, environment_id=self.id, file_path=file_path)

    def list_staging_libraries(self, preview="false"):
        return self.core_client.list_staging_libraries(workspace_id=self.workspace_id, environment_id=self.id, preview=preview)
   
    def get_staging_libraries(self):
        """Get the staging libraries of the environment"""
        return self.core_client.get_staging_libraries(self.workspace_id, self.id)

    def remove_external_library(self, name, version):
        return self.core_client.remove_external_library(workspace_id=self.workspace_id, environment_id=self.id,
                                                        name=name, version=version)

    def update_staging_spark_compute(self, driver_cores = None, driver_memory = None,
                                     dynamic_executor_allocation = None, executor_cores = None, executor_memory = None,
                                     instance_pool = None, runtime_version = None, spark_properties = None, preview="false"):
        return self.core_client.update_staging_spark_compute(workspace_id=self.workspace_id, environment_id=self.id,
                                                            driver_cores=driver_cores, driver_memory=driver_memory,
                                                            dynamic_executor_allocation=dynamic_executor_allocation,
                                                            executor_cores=executor_cores, executor_memory=executor_memory,
                                                            instance_pool=instance_pool, runtime_version=runtime_version,
                                                            spark_properties=spark_properties, preview=preview)

    def update_staging_settings(self,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        """Update the staging settings of the environment"""
        return self.core_client.update_staging_settings(self.workspace_id, self.id, driver_cores, driver_memory,
                                                        dynamic_executor_allocation, executor_cores, executor_memory,
                                                        instance_pool, runtime_version, spark_properties)


    def upload_custom_library(self, library_name, file_path):
        return self.core_client.upload_custom_library(self.workspace_id, self.id, library_name, file_path)
    
    def upload_staging_library(self, file_path):
        return self.core_client.upload_staging_library(self.workspace_id, self.id, file_path)

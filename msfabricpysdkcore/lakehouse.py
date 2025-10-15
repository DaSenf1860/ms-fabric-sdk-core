from msfabricpysdkcore.item import Item

class Lakehouse(Item):
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Lakehouse(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def list_tables(self):
        """List all tables in the lakehouse"""
        return self.core_client.list_tables(self.workspace_id, self.id)
    
    def load_table(self, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        """Load a table in the lakehouse"""
        return self.core_client.load_table(self.workspace_id, self.id, table_name, path_type, relative_path,
                                           file_extension, format_options, mode, recursive, wait_for_completion)
    
    def run_on_demand_table_maintenance(self, execution_data, job_type = "TableMaintenance", wait_for_completion = True):
        """Run on demand table maintenance"""
        return self.core_client.run_on_demand_table_maintenance(self.workspace_id, self.id, execution_data, job_type, wait_for_completion)
    
    def list_livy_sessions(self):
        """List all livy sessions in the lakehouse"""
        return self.core_client.list_lakehouse_livy_sessions(self.workspace_id, self.id)

    def get_livy_session(self, livy_id):
        """Get a livy session in the lakehouse"""
        return self.core_client.get_lakehouse_livy_session(self.workspace_id, self.id, livy_id)
    
    def create_refresh_materialized_lake_view_schedule(self, enabled, configuration):
        """Create a refresh materialized lake view schedule
        Args:
            enabled (bool): Whether the schedule is enabled
            configuration (dict): The configuration of the schedule
        Returns:
            dict: The created schedule
        """
        return self.core_client.create_refresh_materialized_lake_view_schedule(workspace_id=self.workspace_id, lakehouse_id=self.id,
                                                                               enabled=enabled, configuration=configuration)
    
    def delete_refresh_materialized_lake_view_schedule(self, schedule_id):
        """Delete a refresh materialized lake view schedule
        Args:
            schedule_id (str): The ID of the schedule
        Returns:
            int: The status code of the response
        """
        return self.core_client.delete_refresh_materialized_lake_view_schedule(workspace_id=self.workspace_id, lakehouse_id=self.id,
                                                                               schedule_id=schedule_id)

    def run_on_demand_refresh_materialized_lake_view(self, job_type="RefreshMaterializedLakeViews"):
        """Run refresh materialized lake view
        Args:
            job_type (str): The job type
        Returns:
            dict: The operation result or response value
        """
        return self.core_client.run_on_demand_refresh_materialized_lake_view(workspace_id=self.workspace_id, lakehouse_id=self.id, job_type=job_type)

    def update_refresh_materialized_lake_view_schedule(self, schedule_id, enabled, configuration):
        """Update a refresh materialized lake view schedule
        Args:
            schedule_id (str): The ID of the schedule
            schedule_id (str): The ID of the schedule
            enabled (bool): Whether the schedule is enabled
            configuration (dict): The configuration of the schedule
        Returns:
            dict: The updated schedule
        """
        return self.core_client.update_refresh_materialized_lake_view_schedule(workspace_id=self.workspace_id, lakehouse_id=self.id,
                                                                               schedule_id=schedule_id, enabled=enabled,
                                                                               configuration=configuration)
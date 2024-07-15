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
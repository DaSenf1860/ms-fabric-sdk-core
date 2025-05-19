from msfabricpysdkcore.item import Item

class Eventstream(Item):
    """Class to represent a eventstream in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, core_client, properties=None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)
    
    def from_dict(item_dict, core_client):
        return Eventstream(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def get_definition(self, type=None, format=None):
        """Method to get the definition of the eventstream"""
        return super().get_definition(type="eventstreams", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the eventstream"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="eventstreams")
    
    # eventstream topology
    def get_eventstream_destination(self, destination_id):
        """Get the destination of an eventstream in a workspace"""
        return self.core_client.get_eventstream_destination(workspace_id=self.workspace_id, eventstream_id=self.id, destination_id=destination_id)
    
    def get_eventstream_destination_connection(self, destination_id):
        """Get the connection of a destination in an eventstream in a workspace"""
        return self.core_client.get_eventstream_destination_connection(workspace_id=self.workspace_id, eventstream_id=self.id, destination_id=destination_id)

    def get_eventstream_source(self, source_id):
        """Get the source of an eventstream in a workspace"""
        return self.core_client.get_eventstream_source(workspace_id=self.workspace_id, eventstream_id=self.id, source_id=source_id)

    def get_eventstream_source_connection(self, source_id):
        """Get the connection of a source in an eventstream in a workspace"""
        return self.core_client.get_eventstream_source_connection(workspace_id=self.workspace_id, eventstream_id=self.id, source_id=source_id)

    def get_eventstream_topology(self):
        """Get the topology of an eventstream in a workspace"""
        return self.core_client.get_eventstream_topology(workspace_id=self.workspace_id, eventstream_id=self.id)
    
    def pause_eventstream(self):
        """Pause an eventstream in a workspace"""
        return self.core_client.pause_eventstream(workspace_id=self.workspace_id, eventstream_id=self.id)
    
    def pause_eventstream_destination(self, destination_id):
        """Pause a destination in an eventstream in a workspace"""
        return self.core_client.pause_eventstream_destination(workspace_id=self.workspace_id, eventstream_id=self.id, destination_id=destination_id)

    def pause_eventstream_source(self, source_id):
        """Pause a source in an eventstream in a workspace"""
        return self.core_client.pause_eventstream_source(workspace_id=self.workspace_id, eventstream_id=self.id, source_id=source_id)

    def resume_eventstream(self, start_type, custom_start_date_time = None):
        """Resume an eventstream in a workspace"""
        return self.core_client.resume_eventstream(workspace_id=self.workspace_id, eventstream_id=self.id, start_type=start_type, custom_start_date_time=custom_start_date_time)

    def resume_eventstream_destination(self, destination_id, start_type, custom_start_date_time = None):
        """Resume a destination in an eventstream in a workspace"""
        return self.core_client.resume_eventstream_destination(workspace_id=self.workspace_id, eventstream_id=self.id,
                                                               destination_id=destination_id, start_type=start_type, custom_start_date_time=custom_start_date_time)

    def resume_eventstream_source(self, source_id, start_type, custom_start_date_time = None):
        """Resume a source in an eventstream in a workspace"""
        return self.core_client.resume_eventstream_source(workspace_id=self.workspace_id, eventstream_id=self.id,
                                                          source_id=source_id, start_type=start_type, custom_start_date_time=custom_start_date_time)


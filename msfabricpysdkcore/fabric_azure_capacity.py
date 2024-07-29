import json 

from msfabricpysdkcore.fabric_azure_client import FabricAzureClient

class FabricAzureCapacity:
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, name, subscription_id, resource_group_name, type, location, properties, sku, azure_client: FabricAzureClient, tags=None) -> None:
        
        self.id = id
        self.name = name
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.type = type
        self.location = location
        self.properties = properties
        self.sku = sku
        self.tags = tags

        self.azure_client = azure_client

    def __str__(self) -> str:
        """Return a string representation of the fabric azure capacity object"""
        dict_ = {
            'id': self.id,
            'name': self.name,
            'subscription_id': self.subscription_id,
            'resource_group_name': self.resource_group_name,
            'type': self.type,
            'location': self.location,
            'properties': self.properties,
            'sku': self.sku,
            'tags': self.tags
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(dict, azure_client):
        """Create FabricAzureCapacity object from dictionary"""
            
        return FabricAzureCapacity(id=dict['id'], name=dict['name'], subscription_id=dict['subscription_id'],
                                   resource_group_name=dict['resource_group_name'],
                                   type=dict['type'],
                                   location=dict['location'],
                                   properties=dict['properties'], sku=dict['sku'],
                                   tags=dict.get('tags', None), azure_client=azure_client)
    
    # Delete

    def delete(self):
        """Delete the capacity"""

        return self.azure_client.delete_capacity(self.subscription_id, self.resource_group_name, self.name)
    
    # Resume

    def resume(self):
        """Resume the capacity"""

        return self.azure_client.resume_capacity(self.subscription_id, self.resource_group_name, self.name)
    
    # Suspend

    def suspend(self):
        """Suspend the capacity"""

        return self.azure_client.suspend_capacity(self.subscription_id, self.resource_group_name, self.name)
    
    # Update

    def update(self, properties_administration=None, sku=None, tags=None):
        """Update the capacity"""

        return self.azure_client.update_capacity(self.subscription_id, self.resource_group_name, self.name, properties_administration=properties_administration, sku=sku, tags=tags)


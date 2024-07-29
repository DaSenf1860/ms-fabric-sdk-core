import json
from msfabricpysdkcore.coreapi import FabricClientCore


class SparkCustomPool:
    """Class to represent a custom pool in Microsoft Fabric"""

    def __init__(self, id, name, type, node_family, node_size, auto_scale, dynamic_executor_allocation, workspace_id, core_client: FabricClientCore) -> None:
        
        self.id = id
        self.name = name
        self.type = type
        self.node_family = node_family
        self.node_size = node_size
        self.auto_scale = auto_scale
        self.dynamic_executor_allocation = dynamic_executor_allocation
        self.workspace_id = workspace_id
        
        self.core_client = core_client

    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "nodeFamily": self.node_family,
            "nodeSize": self.node_size,
            "autoScale": self.auto_scale,
            "dynamicExecutorAllocation": self.dynamic_executor_allocation,
            "workspaceId": self.workspace_id
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(item_dict, core_client):
        """Create Item object from dictionary"""

        if 'autoScale' not in item_dict:
            item_dict['autoScale'] = item_dict['auto_scale']

        if 'dynamicExecutorAllocation' not in item_dict:
            item_dict['dynamicExecutorAllocation'] = item_dict['dynamic_executor_allocation']
        
        if 'nodeFamily' not in item_dict:
            item_dict['nodeFamily'] = item_dict['node_family']
        
        if 'nodeSize' not in item_dict:
            item_dict['nodeSize'] = item_dict['node_size']
        
        return SparkCustomPool(id=item_dict['id'], name=item_dict['name'], type=item_dict['type'], node_family=item_dict['nodeFamily'],
                                node_size=item_dict['nodeSize'], auto_scale=item_dict['autoScale'], dynamic_executor_allocation=item_dict['dynamicExecutorAllocation'],
                                workspace_id=item_dict['workspaceId'], core_client=core_client)


    def delete(self):
        """Delete the custom pool item"""
        return self.core_client.delete_workspace_custom_pool(self.workspace_id, self.id)
    

    def update(self, name, node_family, node_size, auto_scale, dynamic_executor_allocation):
        """Update the custom pool item"""
        _ = self.core_client.update_workspace_custom_pool(self.workspace_id, self.id, name, node_family, node_size, auto_scale, dynamic_executor_allocation)
        if name is not None:
            self.name = name
        if node_family is not None:
            self.node_family = node_family
        if node_size is not None:
            self.node_size = node_size
        if auto_scale is not None:
            self.auto_scale = auto_scale
        if dynamic_executor_allocation is not None:
            self.dynamic_executor_allocation = dynamic_executor_allocation

        return self
    
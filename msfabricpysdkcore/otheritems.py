import json
from time import sleep
import requests
from msfabricpysdkcore.item import Item


class Eventhouse(Item):
    """Class to represent a eventhouse in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, description=""):
        super().__init__(id = id, display_name=display_name, type=type, 
                         workspace_id=workspace_id, auth=auth, properties=properties, 
                         description=description)
        
    def from_dict(item_dict, auth):
        if "displayName" not in item_dict:
            item_dict["displayName"] = item_dict["display_name"]
        if "workspaceId" not in item_dict:
            item_dict["workspaceId"] = item_dict["workspace_id"]

        return Eventhouse(id=item_dict['id'], display_name=item_dict['displayName'], 
                          type=item_dict['type'], workspace_id=item_dict['workspaceId'],
                          properties=item_dict.get('properties', None),
                          description=item_dict.get('description', ""), auth=auth)

    def create_kql_database(self, display_name = None, description= None):
        from msfabricpysdkcore.coreapi import FabricClientCore
        """Method to create a kql database in the eventhouse"""
        creation_payload = {"databaseType" : "ReadWrite",
                            "parentEventhouseItemId" : self.id}
        
        fcc = FabricClientCore(silent=True)

        return fcc.create_kql_database(workspace_id = self.workspace_id,
                                       display_name = display_name, description = description,
                                       creation_payload= creation_payload)

class SparkJobDefinition(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return SparkJobDefinition(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)
    
    def get_definition(self, format=None):
        return super().get_definition(type="sparkJobDefinitions", format=format)
    
    def update_definition(self, definition):
        return super().update_definition(definition=definition, type="sparkJobDefinitions")
    
class Warehouse(Item):
    """Class to represent a warehouse in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return Warehouse(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

class KQLDatabase(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return KQLDatabase(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

class KQLQueryset(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return KQLQueryset(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

class Eventstream(Item):
    """Class to represent a eventstream in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)
    
    def from_dict(item_dict, auth):
        return Eventstream(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)
    
class MLExperiment(Item):
    """Class to represent a ml experiment in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)
    
    def from_dict(item_dict, auth):
        return MLExperiment(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

class MLModel(Item):
    """Class to represent a ml model in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return MLModel(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

class Notebook(Item):
    """Class to represent a notebook in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return Notebook(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)
    
    def get_definition(self, format=None):
        """Method to get the definition of the notebook"""
        return super().get_definition(type = "notebooks", format = format)
    
    def update_definition(self, definition):
        """Method to update the definition of the notebook"""
        return super().update_definition(definition, type = "notebooks")

class Report(Item):
    """Class to represent a report in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return Report(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)
    
    def get_definition(self, type=None, format=None):
        """Method to get the definition of the report"""
        return super().get_definition(type = "reports", format = format)
    
    def update_definition(self, definition):
        """Method to update the definition of the report"""
        return super().update_definition(definition, type = "reports")

class SemanticModel(Item):
    """Class to represent a semantic model in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return SemanticModel(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)
    
    def get_definition(self, format=None):
        """Method to get the definition of the semantic model"""
        return super().get_definition(type="semanticModels", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the semantic model"""
        return super().update_definition(definition, type = "semanticModels")

class DataPipeline(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return DataPipeline(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)
    
    def run_on_demand_item_job(self, execution_data=None):
        return super().run_on_demand_item_job(job_type = "Pipeline", execution_data=execution_data)
    

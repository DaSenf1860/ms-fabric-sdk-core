from msfabricpysdkcore.item import Item


class Eventhouse(Item):
    """Class to represent a eventhouse in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, description=""):
        super().__init__(id = id, display_name=display_name, type=type, 
                         workspace_id=workspace_id, core_client=core_client, properties=properties, 
                         description=description)
        
    def from_dict(item_dict, core_client):
        if "displayName" not in item_dict:
            item_dict["displayName"] = item_dict["display_name"]
        if "workspaceId" not in item_dict:
            item_dict["workspaceId"] = item_dict["workspace_id"]

        return Eventhouse(id=item_dict['id'], display_name=item_dict['displayName'], 
                          type=item_dict['type'], workspace_id=item_dict['workspaceId'],
                          properties=item_dict.get('properties', None),
                          description=item_dict.get('description', ""), core_client=core_client)

    def create_kql_database(self, display_name = None, description= None):
        from msfabricpysdkcore.coreapi import FabricClientCore
        """Method to create a kql database in the eventhouse"""
        creation_payload = {"databaseType" : "ReadWrite",
                            "parentEventhouseItemId" : self.id}
        
        return self.core_client.create_kql_database(self.workspace_id, display_name=display_name, description=description, creation_payload=creation_payload)

class SparkJobDefinition(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return SparkJobDefinition(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        resp_dict = self.core_client.get_spark_job_definition_definition(self.workspace_id, self.id, format=format)
        self.definition = resp_dict['definition']
        return resp_dict
    
    def update_definition(self, definition):
        return self.core_client.update_spark_job_definition_definition(self.workspace_id, self.id, definition)
    
    def run_on_demand_spark_job_definition(self, job_type = "sparkjob"):
        return self.core_client.run_on_demand_spark_job_definition(workspace_id=self.workspace_id, spark_job_definition_id=self.id, job_type=job_type)


class Warehouse(Item):
    """Class to represent a warehouse in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Warehouse(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class KQLDatabase(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return KQLDatabase(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class KQLQueryset(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return KQLQueryset(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class Eventstream(Item):
    """Class to represent a eventstream in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)
    
    def from_dict(item_dict, core_client):
        return Eventstream(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
class MLExperiment(Item):
    """Class to represent a ml experiment in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)
    
    def from_dict(item_dict, core_client):
        return MLExperiment(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class MLModel(Item):
    """Class to represent a ml model in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return MLModel(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class Notebook(Item):
    """Class to represent a notebook in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Notebook(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        """Method to get the definition of the notebook"""
        definition = self.core_client.get_item_definition(self.workspace_id, self.id, type="notebooks", format=format)
        self.definition = definition
        return definition
    
    def update_definition(self, definition):
        """Method to update the definition of the notebook"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="notebooks")

class Report(Item):
    """Class to represent a report in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Report(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, type=None, format=None):
        """Method to get the definition of the report"""
        self.definition = self.core_client.get_item_definition(self.workspace_id, self.id, type="reports", format=format)
        return self.definition
    
    def update_definition(self, definition):
        """Method to update the definition of the report"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="reports")

class SemanticModel(Item):
    """Class to represent a semantic model in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return SemanticModel(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        """Method to get the definition of the semantic model"""
        self.definition = self.core_client.get_item_definition(self.workspace_id, self.id, type="semanticModels", format=format)
        return self.definition
    
    def update_definition(self, definition):
        """Method to update the definition of the semantic model"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="semanticModels")

class DataPipeline(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return DataPipeline(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def run_on_demand_item_job(self, execution_data=None):
        return self.core_client.run_on_demand_item_job(workspace_id=self.workspace_id, item_id=self.id, job_type="Pipeline", execution_data=execution_data)
    
    

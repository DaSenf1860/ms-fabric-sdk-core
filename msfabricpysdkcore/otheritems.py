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

    def get_definition(self, type=None, format=None):
        """Method to get the definition of the eventhouse"""
        return super().get_definition(type="eventhouses", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the eventhouse"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="eventhouses")

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
        return super().get_definition(type="sparkJobDefinitions", format=format)
    
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

class KQLDashboard(Item):
    """Class to represent a kql dashboard in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return KQLDashboard(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        """Method to get the definition of the kql dashboard"""
        return super().get_definition(type="kqlDashboards", format=format)

    def update_definition(self, definition):
        """Method to update the definition of the kql dashboard"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="kqlDashboards")

class KQLDatabase(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return KQLDatabase(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def get_definition(self, type=None, format=None):
        """Method to get the definition of the kql database"""
        return super().get_definition(type="kqlDatabases", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the kql database"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="kqlDatabases")

class KQLQueryset(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return KQLQueryset(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        """Method to get the definition of the kql queryset"""
        return super().get_definition(type="kqlQuerysets", format=format)
    
    def update_definition(self, definition, update_metadata=None):
        """Method to update the definition of the kql queryset"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="kqlQuerysets",
                                                       update_metadata=update_metadata)
    
    

class Eventstream(Item):
    """Class to represent a eventstream in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
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

class GraphQLApi(Item):
    """Class to represent a graphql api in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)
    
    def from_dict(item_dict, core_client):
        return GraphQLApi(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
class MirroredDatabase(Item):
    """Class to represent a mirrored database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)
    
    def from_dict(item_dict, core_client):
        return MirroredDatabase(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self): 
        """Method to get the definition of the mirrored database"""
        return super().get_definition(type="mirroredDatabases")
    
    def update_definition(self, definition):
        """Method to update the definition of the mirrored database"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="mirroredDatabases")

    def get_mirrored_database_definition(self, mirrored_database_id):
        return self.core_client.get_mirrored_database_definition(workspace_id=self.id,
                                                                 mirrored_database_id=mirrored_database_id)
    def get_mirroring_status(self):
        return self.core_client.get_mirroring_status(workspace_id=self.workspace_id, mirrored_database_id=self.id)

    def get_tables_mirroring_status(self):
        return self.core_client.get_tables_mirroring_status(workspace_id=self.workspace_id, mirrored_database_id=self.id)

    def start_mirroring(self):
        return self.core_client.start_mirroring(workspace_id=self.workspace_id, mirrored_database_id=self.id)

    def stop_mirroring(self):
        return self.core_client.stop_mirroring(workspace_id=self.workspace_id, mirrored_database_id=self.id)

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

class MountedDataFactory(Item):
    """Class to represent a mounted data factory in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)
    
    def from_dict(item_dict, core_client):
        return MountedDataFactory(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def get_definition(self, type=None, format=None):
        """Method to get the definition of the mountedDataFactory"""
        return super().get_definition(type="mountedDataFactories", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the mountedDataFactory"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="mountedDataFactories")

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
        return super().get_definition(type="notebooks", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the notebook"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="notebooks")

class Reflex(Item):
    """Class to represent a reflex in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Reflex(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def get_definition(self, type=None, format=None):
        """Method to get the definition of the reflex"""
        return super().get_definition(type="reflexes", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the reflex"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="reflexes")
    
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
        return super().get_definition(type="reports", format=format)
    
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
        return super().get_definition(type="semanticModels", format=format)
    
    def update_definition(self, definition):
        """Method to update the definition of the semantic model"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="semanticModels")

class SQLDatabase(Item):
    """Class to represent a sql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return SQLDatabase(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class DataPipeline(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return DataPipeline(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, type=None, format=None, **kwargs):
        return super().get_definition(type="dataPipelines", format=format, **kwargs)
    
    def update_definition(self, definition):
        """Method to update the definition of the dataPipeline"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="dataPipelines")
    
    def run_on_demand_item_job(self, execution_data=None):
        return self.core_client.run_on_demand_item_job(workspace_id=self.workspace_id, item_id=self.id, job_type="Pipeline", execution_data=execution_data)
    
    

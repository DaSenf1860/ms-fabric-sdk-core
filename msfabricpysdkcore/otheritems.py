from msfabricpysdkcore.item import Item

class AnomalyDetector(Item):
    """Class to represent an anomaly detector in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return AnomalyDetector(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        """Method to get the definition of the anomaly detector"""
        return super().get_definition(type="anomalydetectors", format=format)
    
    def update_definition(self, definition, update_metadata=None):
        """Method to update the definition of the anomaly detector"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="anomalydetectors",
                                                       update_metadata=update_metadata)

class ApacheAirflowJob(Item):
    """Class to represent a ApacheAirflowJob in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return ApacheAirflowJob(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class CopyJob(Item):
    """Class to represent a copy job in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return CopyJob(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class Dataflow(Item):
    """Class to represent a dataflow in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Dataflow(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

    def discover_parameters(self):
        return self.core_client.discover_dataflow_parameters(workspace_id=self.workspace_id, dataflow_id=self.id)

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

class DigitalTwinBuilder(Item):
    """Class to represent a DigitalTwinBuilder in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return DigitalTwinBuilder(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class DigitalTwinBuilderFlow(Item):
    """Class to represent a DigitalTwinBuilderFlow in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return DigitalTwinBuilderFlow(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)

class MirroredAzureDatabricksCatalog(Item):
    """Class to represent a mirrored Azure Databricks catalog in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return MirroredAzureDatabricksCatalog(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def refresh_catalog_metadata(self):
        """Method to refresh the metadata of the mirrored Azure Databricks catalog"""
        return self.core_client.refresh_mirrored_azure_databricks_catalog_metadata(self.workspace_id, self.id)

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

    def list_livy_sessions(self):
        """List all livy sessions in the spark job definition"""
        return self.core_client.list_spark_job_definition_livy_sessions(self.workspace_id, self.id)

    def get_livy_session(self, livy_id):
        """Get a livy session in the spark job definition"""
        return self.core_client.get_spark_job_definition_livy_session(self.workspace_id, self.id, livy_id)

class Warehouse(Item):
    """Class to represent a warehouse in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Warehouse(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_connection_string(self, guest_tenant_id = None, private_link_type = None):
        return self.core_client.get_warehouse_connection_string(workspace_id=self.workspace_id, warehouse_id=self.id,
                                                               guest_tenant_id=guest_tenant_id, private_link_type=private_link_type)
    
    def create_restore_point(self, display_name = None, description = None):
        return self.core_client.create_warehouse_restore_point(workspace_id=self.workspace_id, warehouse_id=self.id,
                                                               display_name=display_name, description=description)
    
    def delete_restore_point(self, restore_point_id):
        return self.core_client.delete_warehouse_restore_point(workspace_id=self.workspace_id, warehouse_id=self.id,
                                                               restore_point_id=restore_point_id)
    
    def get_restore_point(self, restore_point_id):
        return self.core_client.get_warehouse_restore_point(workspace_id=self.workspace_id, warehouse_id=self.id,
                                                            restore_point_id=restore_point_id)
    
    def list_restore_points(self):
        return self.core_client.list_warehouse_restore_points(workspace_id=self.workspace_id, warehouse_id=self.id)
    
    def restore_to_restore_point(self, restore_point_id, wait_for_completion = False):
        return self.core_client.restore_warehouse_to_restore_point(workspace_id=self.workspace_id, warehouse_id=self.id,
                                                                  restore_point_id=restore_point_id,
                                                                  wait_for_completion=wait_for_completion)
    
    def update_restore_point(self, restore_point_id, display_name = None, description = None):
        return self.core_client.update_warehouse_restore_point(workspace_id=self.workspace_id, warehouse_id=self.id,
                                                               restore_point_id=restore_point_id,
                                                               display_name=display_name, description=description)

    def get_sql_audit_settings(self):
        """Get the audit settings of a warehouse
        Returns:
            dict: The audit settings of the warehouse
        """

        return self.core_client.get_warehouse_sql_audit_settings(self.workspace_id, self.id)

    def set_warehouse_audit_actions_and_groups(self, set_audit_actions_and_groups_request):
        """Set the audit actions and groups of a warehouse
        Args:
            set_audit_actions_and_groups_request (list): The list of audit actions and groups
        Returns:
            dict: The updated audit settings of the warehouse
        """
        return self.core_client.set_warehouse_audit_actions_and_groups(workspace_id=self.workspace_id,
                                                                       warehouse_id=self.id,
                                                                       set_audit_actions_and_groups_request=set_audit_actions_and_groups_request)

    def update_warehouse_sql_audit_settings(self, retention_days, state):
        """Update the audit settings of a warehouse
        Args:
            retention_days (int): The number of days to retain the audit logs
            state (str): The state of the audit settings
        Returns:
            dict: The updated audit settings of the warehouse
        """
        return self.core_client.update_warehouse_sql_audit_settings(self.workspace_id, self.id,
                                                                    retention_days, state)


class WarehouseSnapshot(Item):
    """Class to represent a warehouse snapshot in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return WarehouseSnapshot(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
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
    

class GraphQLApi(Item):
    """Class to represent a graphql api in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, core_client, properties=None, definition=None, description=""):
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
    
        
    def activate_ml_model_endpoint_version(self, name, wait_for_completion = False):
        """Activate an ml model endpoint version
        Args:
            name (str): The name of the endpoint version    
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            dict: The activated endpoint version
        """

        return self.core_client.activate_ml_model_endpoint_version(workspace_id=self.workspace_id, model_id=self.id,
                                                                   name=name, wait_for_completion=wait_for_completion)

    def deactivate_all_ml_model_endpoint_versions(self, wait_for_completion = False):
        """Deactivate all ml model endpoint versions
        Args:
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            Response: The operation result
        """
        return self.core_client.deactivate_all_ml_model_endpoint_versions(workspace_id=self.workspace_id, model_id=self.id,
                                                                          wait_for_completion=wait_for_completion)

    def deactivate_ml_model_endpoint_version(self, name, wait_for_completion = False):
        """Deactivate an ml model endpoint version
        Args:
            name (str): The name of the endpoint version
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            Response: The operation result
        """
        return self.core_client.deactivate_ml_model_endpoint_version(workspace_id=self.workspace_id, model_id=self.id,
                                                                     name=name, wait_for_completion=wait_for_completion)

    def get_ml_model_endpoint(self):
        """Get the ml model endpoint
        Returns:
            dict: The ml model endpoint
        """
        return self.core_client.get_ml_model_endpoint(workspace_id=self.workspace_id, model_id=self.id)

    def get_ml_model_endpoint_version(self, name):
        """Get an ml model endpoint version
        Args:
            name (str): The name of the endpoint version
        Returns:
            dict: The ml model endpoint version
        """
        return self.core_client.get_ml_model_endpoint_version(workspace_id=self.workspace_id, model_id=self.id, name=name)

    def list_ml_model_endpoint_versions(self):
        """List all ml model endpoint versions
        
        Returns:
            list: The list of ml model endpoint versions
        """
        return self.core_client.list_ml_model_endpoint_versions(workspace_id=self.workspace_id, model_id=self.id)

    def score_ml_model_endpoint(self, inputs, format_type = None, orientation = None):
        """Score an ml model endpoint
        Args:
            inputs (list): The inputs to score
            format_type (str): The format type
            orientation (str): The orientation
        Returns:
            dict: The scoring result
        """
        return self.core_client.score_ml_model_endpoint(workspace_id=self.workspace_id, model_id=self.id, inputs=inputs,
                                                        format_type=format_type, orientation=orientation)

    def score_ml_model_endpoint_version(self, name, inputs, format_type = None, orientation = None):
        """Score an ml model endpoint version
        Args:
            name (str): The name of the endpoint version    
            inputs (list): The inputs to score
            format_type (str): The format type
            orientation (str): The orientation
        Returns:
            dict: The scoring result
        """
        return self.core_client.score_ml_model_endpoint_version(workspace_id=self.workspace_id, model_id=self.id, name=name,
                                                               inputs=inputs, format_type=format_type, orientation=orientation)                                

    def update_ml_model_endpoint(self, default_version_assignment_behavior, default_version_name):
        """Update an ml model endpoint
        Args:
            default_version_assignment_behavior (str): The default version assignment behavior
            default_version_name (str): The default version name
        Returns:
            dict: The updated endpoint
        """
        return self.core_client.update_ml_model_endpoint(workspace_id=self.workspace_id, model_id=self.id,
                                                        default_version_assignment_behavior=default_version_assignment_behavior,
                                                        default_version_name=default_version_name)

    def update_ml_model_endpoint_version(self, name, scale_rule):
        """Update an ml model endpoint version
        Args:
            name (str): The name of the endpoint version
            scale_rule (str): The scale rule
        Returns:
            dict: The updated endpoint version
        """
        return self.core_client.update_ml_model_endpoint_version(workspace_id=self.workspace_id, model_id=self.id,
                                                                 name=name, scale_rule=scale_rule)


class Map(Item):
    """Class to represent a map in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, core_client, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return Map(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
    
    def get_definition(self, format=None):
        """Method to get the definition of the map"""
        return super().get_definition(type="Maps", format=format)
    
    def update_definition(self, definition, update_metadata=None):
        """Method to update the definition of the map"""
        return self.core_client.update_item_definition(self.workspace_id, self.id, definition, type="Maps",
                                                       update_metadata=update_metadata)

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
    
    def list_livy_sessions(self):
        """List all livy sessions in the notebook"""
        return self.core_client.list_notebook_livy_sessions(self.workspace_id, self.id)

    def get_livy_session(self, livy_id):
        """Get a livy session in the notebook"""
        return self.core_client.get_notebook_livy_session(self.workspace_id, self.id, livy_id)

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
    
    def bind_connection(self, connection_binding):
        """Bind a connection to the semantic model"""
        return self.core_client.bind_semantic_model_connection(workspace_id=self.workspace_id, semantic_model_id=self.id,
                                                               connection_binding=connection_binding)

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

class VariableLibrary(Item):
    """Class to represent a variable library in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, core_client, properties=None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, core_client, properties, definition, description)

    def from_dict(item_dict, core_client):
        return VariableLibrary(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), core_client=core_client)
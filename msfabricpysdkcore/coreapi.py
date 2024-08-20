import json
from time import sleep
from warnings import warn

from msfabricpysdkcore.client import FabricClient
from msfabricpysdkcore.util import logger


class FabricClientCore(FabricClient):
    """FabricClientCore class to interact with Fabric Core APIs"""

    def __init__(self, tenant_id = None, client_id = None, client_secret = None,
                 username = None, password = None, silent=None) -> None:
        """Initialize FabricClientCore object"""
        super().__init__(scope="https://api.fabric.microsoft.com/.default", 
                         tenant_id=tenant_id,
                         client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password)
        if silent is not None:
            warn("The 'silent' parameter is deprecated and will be removed in a future version.", DeprecationWarning, stacklevel=2)

    def long_running_operation(self, response_headers):
        """Check the status of a long running operation"""
        from msfabricpysdkcore.long_running_operation import check_long_running_operation

        return check_long_running_operation(response_headers, self)

    ### Capacities

    def get_capacity(self, capacity_id = None, capacity_name = None):
        """Get a capacity
        
        Args:
            capacity_id (str): The ID of the capacity
            capacity_name (str): The name of the capacity
            
        Returns:
            Capacity: The capacity object
            
        Raises:
            ValueError: If no capacity is found
        """
        if capacity_id is None and capacity_name is None:
            raise ValueError("Either capacity_id or capacity_name must be provided")
        caps = self.list_capacities()
        for cap in caps:
            if capacity_id and cap.id == capacity_id:
                return cap
            if capacity_name and cap.display_name == capacity_name:
                return cap
        raise ValueError("No capacity found") 
    
    def list_capacities(self):
        """List all capacities in the tenant
        Returns:
            list: The list of capacities
        """
        from msfabricpysdkcore.capacity import Capacity
        url = "https://api.fabric.microsoft.com/v1/capacities"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error listing capacities", return_format="value_json", paging=True)

        items = [Capacity.from_dict(i) for i in items]
        return items
    
    # Deployment Pipelines

    def deploy_stage_content(self, deployment_pipeline_id, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, wait_for_completion = True):
        """Deploy stage content
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            source_stage_id (str): The ID of the source stage
            target_stage_id (str): The ID of the target stage
            created_workspace_details (list): A list of created workspace details
            items (list): A list of items
            note (str): A note
            wait_for_completion (bool): Whether to wait for the deployment to complete
        Returns:
            Details about the dpeloyment
        """
        
        # POST https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/deploy

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/deploy"

        body = {
            "sourceStageId": source_stage_id,
            "targetStageId": target_stage_id
        }

        if created_workspace_details:
            body["createdWorkspaceDetails"] = created_workspace_details
        if items:
            body["items"] = items
        if note:
            body["note"] = note
            
        json_operation_result = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 202, 429], error_message="Error deploying stage content", 
                                                     return_format="json+operation_result", wait_for_completion=wait_for_completion)

        return json_operation_result
    
    def get_deployment_pipeline(self, deployment_pipeline_id):
        """Get a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
        Returns:
            DeploymentPipeline: The deployment pipeline
        """
        from msfabricpysdkcore.deployment_pipeline import DeploymentPipeline
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}"

        result_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting deployment pipeline", return_format="json")

        return DeploymentPipeline.from_dict(result_json, self)
    
    def get_deployment_pipeline_stages_items(self, pipeline_id, stage_id = None, stage_name = None):
        warn("DEPRECATED: get_deployment_pipeline_stages_items. get_deployment_pipeline_stages_items. Use list_deployment_pipeline_stages_items instead", DeprecationWarning, stacklevel=2)
        return self.list_deployment_pipeline_stages_items(pipeline_id, stage_id, stage_name)

    def list_deployment_pipeline_stages_items(self, deployment_pipeline_id, stage_id = None, stage_name = None):
        """List the items in a deployment stage
        Args:
            pipeline_id (str): The ID of the deployment pipeline
            stage_id (str): The ID of the deployment stage
            stage_name (str): The name of the deployment stage
        Returns:
            list: List of DeploymentStageItem objects
        """

        if stage_id == None and stage_name == None:
            raise Exception("Please provide either stage_id or stage_name")

        if stage_id is None:
            stages = self.list_deployment_pipeline_stages(deployment_pipeline_id)
            dep_pip_stages = [stage for stage in stages if stage.display_name == stage_name]
            if len(dep_pip_stages) == 0:
                raise Exception(f"Stage with name {stage_name} not found")
            stage_id = dep_pip_stages[0].id

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages/{stage_id}/items"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error getting deployment pipeline stage items", return_format="value_json", paging=True)

        return items

    def get_deployment_pipeline_stages(self, pipeline_id):
        """Get the stages of a deployment pipeline
        Args:
            pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: List of DeploymentPipelineStage objects
        """
        warn("DEPRECATED: get_deployment_pipeline_stages. Use list_deployment_pipeline_stages instead", DeprecationWarning, stacklevel=2)
        return self.list_deployment_pipeline_stages(pipeline_id)

    def list_deployment_pipeline_stages(self, deployment_pipeline_id):
        """Get the stages of a deployment pipeline
        Args:
            pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: List of DeploymentPipelineStage objects
        """
        from msfabricpysdkcore.deployment_pipeline import Deployment_Pipeline_Stage

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                      error_message="Error getting deployment pipeline stages", return_format="value_json", paging=True)

        for item in items:
            item["deploymentPipelineId"] = deployment_pipeline_id
        stages = [Deployment_Pipeline_Stage.from_dict(item, self) for item in items]
        
        return stages

    def list_deployment_pipelines(self):
        """List deployment pipelines
        Returns:
            list: List of DeploymentPipeline objects
        """
        from msfabricpysdkcore.deployment_pipeline import DeploymentPipeline

        url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing deployment pipelines", return_format="value_json", paging=True)


        dep_pipes = [DeploymentPipeline.from_dict(i, core_client=self) for i in items]

        return dep_pipes

    # External Data Shares

    # create

    def create_external_data_share(self, workspace_id, item_id, paths, recipient):
        """Create an external data share in an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            paths (list): The paths to share
            recipient (str): The recipient of the share
        Returns:
            dict: The external data share
        """
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/externalDataShares"

        body = {
            'paths': paths,
            'recipient': recipient
        }
        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429],
                                             error_message="Error creating external data share", return_format="json")
        return response_json

    def get_external_data_share(self, workspace_id, item_id, external_data_share_id):
        """Get an external data share in an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            external_data_share_id (str): The ID of the external data share
        Returns:
            dict: The external data share
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/externalDataShares/{external_data_share_id}"
        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting external data share", return_format="json")
        return response_json
    
    # list

    def list_external_data_shares_in_item(self, workspace_id, item_id):
        """List external data shares in an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
        Returns:
            list: The list of external data shares
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/externalDataShares"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing external data shares", return_format="value_json", paging=True)
        return items
    
    # revoke

    def revoke_external_data_share(self, workspace_id, item_id, external_data_share_id):
        """Revoke an external data share in an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            external_data_share_id (str): The ID of the external data share
        Returns:
            int: The status code of the response
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/externalDataShares/{external_data_share_id}/revoke"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error revoking external data share", return_format="response")
        return response.status_code
    
    # Git
    
    def commit_to_git(self, workspace_id, mode, comment=None, items=None, workspace_head=None):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/commitToGit
        """Commit to git
        Args:
            workspace_id (str): The ID of the workspace
            mode (str): The mode of the commit
            comment (str): The comment of the commit
            items (list): The list of items
            workspace_head (str): The workspace head
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/commitToGit"

        body = {
            'mode': mode
        }

        if comment:
            body['comment'] = comment
        if items:
            body['items'] = items
        if workspace_head:
            body['workspaceHead'] = workspace_head

        response = self.calling_routine(url=url, operation="POST", body=body,
                                        response_codes=[200, 202, 429],
                                        error_message="Error committing to git", return_format="response")

        return response.status_code

    def git_connect(self, workspace_id, git_provider_details):
        """Connect git
        Args:
            workspace_id (str): The ID of the workspace
            git_provider_details (dict): The git provider details
        Returns:
            int: The status code of the response
        """
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/connect
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/connect"

        payload = {
            'gitProviderDetails': git_provider_details
        }

        response = self.calling_routine(url=url, operation="POST", body=payload,
                                        response_codes=[200, 202, 429],
                                        error_message="Error connecting git", return_format="response")

        return response.status_code

    def git_disconnect(self, workspace_id):
        """Disconnect git
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/disconnect"

        response = self.calling_routine(url=url, operation="POST", response_codes=[200, 204, 429],
                                        error_message="Error disconnecting git", return_format="response")
        return response.status_code

    def git_get_connection(self, workspace_id):
        """Get git connection info
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The git connection info
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/connection"

        response_json = self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting git connection info", return_format="json")

        return response_json

    def git_get_status(self, workspace_id):
        """Get git connection status
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The git connection status
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/status"

        response_json = self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting git connection status",
                                             return_format="json")

        return response_json

    def git_initialize_connection(self, workspace_id, initialization_strategy):
    #        POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/initializeConnection
        """Initialize git connection
        Args:
            workspace_id (str): The ID of the workspace
            initialization_strategy (dict): The initialization strategy
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/initializeConnection"

        body = {'initializeGitConnectionRequest':initialization_strategy}
        
        response = self.calling_routine(url=url, operation="POST", body=body, response_codes=[200, 202, 429],
                                        error_message="Error initializing connection", return_format="response")
        
        return response.status_code
    
    def update_from_git(self, workspace_id, remote_commit_hash, conflict_resolution = None,
                        options = None, workspace_head = None):
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/updateFromGit
        """Update from git"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/updateFromGit"

        body = {
            "remoteCommitHash" : remote_commit_hash
        }

        if conflict_resolution:
            body['conflictResolution'] = conflict_resolution
        if options:
            body['options'] = options
        if workspace_head:
            body['workspaceHead'] = workspace_head

        response = self.calling_routine(url=url, operation="POST", body=body,
                                        response_codes=[200, 202, 429],
                                        error_message="Error updating from git", return_format="response")

        return response.status_code


    # Items

    # Helper Functions

    def get_item_by_name(self, workspace_id, item_name, item_type):
        """Get an item from a workspace by name
        Args:
            workspace_id (str): The ID of the workspace
            item_name (str): The name of the item
            item_type (str): The type of the item
        Returns:
            Item: The item object
        """
        ws_items = self.list_items(workspace_id = workspace_id, with_properties=False)
        for item in ws_items:
            if item.display_name == item_name and item.type == item_type:
                return self.get_item(workspace_id, item.id, item_type)    


    
    def get_item_specific(self, workspace_id, item_dict):
        """Get the item object based on the type
        Args:
            workspace_id (str): The ID of the workspace
            item_dict (dict): The dictionary representing the item
        Returns:
            Item: The item object
        """
        from msfabricpysdkcore.item import Item

        if item_dict["type"] == "DataPipeline":
            return self.get_data_pipeline(workspace_id, item_dict["id"])
        if item_dict["type"] == "Eventstream":
            return self.get_eventstream(workspace_id, item_dict["id"])
        if item_dict["type"] == "Eventhouse":
            return self.get_eventhouse(workspace_id, item_dict["id"])
        if item_dict["type"] == "KQLDatabase":
            return self.get_kql_database(workspace_id, item_dict["id"])
        if item_dict["type"] == "KQLQueryset":
            return self.get_kql_queryset(workspace_id, item_dict["id"])
        if item_dict["type"] == "Lakehouse":
            return self.get_lakehouse(workspace_id, item_dict["id"])
        if item_dict["type"] == "MLExperiment":
            return self.get_ml_experiment(workspace_id, item_dict["id"])
        if item_dict["type"] == "MLModel":
            return self.get_ml_model(workspace_id, item_dict["id"])
        if item_dict["type"] == "Notebook":
            return self.get_notebook(workspace_id, item_dict["id"])
        if item_dict["type"] == "Report":
            return self.get_report(workspace_id, item_dict["id"])
        if item_dict["type"] == "SemanticModel":
            return self.get_semantic_model(workspace_id, item_dict["id"])
        if item_dict["type"] == "SparkJobDefinition":
            return self.get_spark_job_definition(workspace_id, item_dict["id"])
        if item_dict["type"] == "Warehouse":
            return self.get_warehouse(workspace_id, item_dict["id"])
        if item_dict["type"] == "Environment":
            return self.get_environment(workspace_id, item_dict["id"])

        item_obj = Item.from_dict(item_dict, core_client=self)
        return item_obj

    def get_item_object_w_properties(self, workspace_id, item_list):
        """Get the item object with properties
        Args:
            workspace_id (str): The ID of the workspace
            item_list (list): The list of items
        Returns:
            list: The list of item objects
        """

        new_item_list = [self.get_item_specific(workspace_id, item)  for item in item_list]
        return new_item_list
    
    # Create
  
    def create_item(self, workspace_id, display_name, type, definition = None, description = None, wait_for_completion = True, **kwargs):
        """Create an item in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the item
            type (str): The type of the item
            definition (dict): The definition of the item
            description (str): The description of the item
            kwargs: Additional arguments
        Returns:
            Item: The created item
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items"
        body = {
            'displayName': display_name,
            'type': type
        }

        if definition:
            body['definition'] = definition
        if description:
            body['description'] = description

        if type in ["dataPipelines",
                    "environments",
                    "eventhouses",
                    "eventstreams",
                    "kqlDatabases",
                    "lakehouses",
                    "mlExperiments", 
                    "mlModels", 
                    "notebooks", 
                    "reports", 
                    "semanticModels", 
                    "sparkJobDefinitions", 
                    "warehouses"]:
            
            if type == "kqlDatabases":
                if "creation_payload" not in kwargs:
                    raise Exception("creation_payload is required for KQLDatabase")
                body["creationPayload"] = kwargs["creation_payload"]
            
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{type}"
            body.pop('type')


        item_dict = self.calling_routine(url, operation="POST", 
                                         body=body, response_codes=[201, 202, 429], 
                                         error_message="Error creating item", return_format="json+operation_result",
                                         wait_for_completion=wait_for_completion)


        if item_dict is None or "no_operation_result" in item_dict:
            self._logger.debug("Item not returned by API, trying to get it by name")
            item = None
            i = 0

            type_mapping = {"dataPipelines": "DataPipeline",
                            "environments": "Environment",
                            "eventhouses": "Eventhouse",
                            "eventstreams": "Eventstream",
                            "kqlDatabases": "KQLDatabase",
                            "lakehouses": "Lakehouse", 
                            "mlExperiments": "MLExperiment",
                            "mlModels": "MLModel", 
                            "notebooks": "Notebook", 
                            "reports": "Report", 
                            "semanticModels": "SemanticModel",
                            "sparkJobDefinitions": "SparkJobDefinition", 
                            "warehouses": "Warehouse"
                            }
            
            if type in type_mapping.keys():
                type = type_mapping[type]
            while item is None and i < 12:
                item = self.get_item_by_name(workspace_id, display_name, type)
                if item is not None:
                    return item
                self._logger.debug("Item not found, waiting 5 seconds")
                sleep(5)
                i += 1

            self._logger.info("Item not found after 1 minute, returning None")
            return None
                
        return self.get_item_specific(workspace_id, item_dict)

    # Get
 
    def get_item(self, workspace_id, item_id = None, item_name = None, item_type = None):
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}
        """Get an item from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            item_name (str): The name of the item
            item_type (str): The type of the item
        Returns:
            Item: The item object
        Raises:
            Exception: If item_id or the combination item_name + item_type is required
        """
        if item_type:
            if item_type.lower() == "datapipeline":
                return self.get_data_pipeline(workspace_id, item_id, item_name)
            if item_type.lower() == "eventstream":
                return self.get_eventstream(workspace_id, item_id, item_name)
            if item_type.lower() == "kqldatabase":
                return self.get_kql_database(workspace_id, item_id, item_name)
            if item_type.lower() == "kqlqueryset":
                return self.get_kql_queryset(workspace_id, item_id, item_name)
            if item_type.lower() == "lakehouse":
                return self.get_lakehouse(workspace_id, item_id, item_name)
            if item_type.lower() == "mlmodel":
                return self.get_ml_model(workspace_id, item_id, item_name)
            if item_type.lower() == "mlexperiment":
                return self.get_ml_experiment(workspace_id, item_id, item_name)
            if item_type.lower() == "notebook":
                return self.get_notebook(workspace_id, item_id, item_name)
            if item_type.lower() == "report":
                return self.get_report(workspace_id, item_id, item_name)
            if item_type.lower() == "semanticmodel":
                return self.get_semantic_model(workspace_id, item_id, item_name)
            if item_type.lower() == "sparkjobdefinition":
                return self.get_spark_job_definition(workspace_id, item_id, item_name)
            if item_type.lower() == "warehouse":
                return self.get_warehouse(workspace_id, item_id, item_name)
                
        if item_id is None and item_name is not None and item_type is not None:
            return self.get_item_by_name(workspace_id, item_name, item_type)
        elif item_id is None:
            raise Exception("item_id or the combination item_name + item_type is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting item", return_format="json")

        return self.get_item_specific(workspace_id=workspace_id, item_dict = item_dict)

    # Delete

    def delete_item(self, workspace_id, item_id, type = None):
        """Delete an item from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{type}/{item_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting item")
        
        return response.status_code

    # List
 
    def list_items(self, workspace_id, with_properties = False, type = None):
        """List items in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
            type (str): The type of the item
        Returns:
            list: The list of items
        """
        from msfabricpysdkcore.item import Item

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{type}"
        
        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                error_message="Error listing items", return_format="value_json", paging=True)
        
        if with_properties:
            items = self.get_item_object_w_properties(workspace_id=workspace_id, item_list=items)
        else:
            items = [Item.from_dict(item, core_client=self) for item in items]

        return items

    
    def get_item_definition(self, workspace_id, item_id, type = None, format = None):
        """Get the item definition
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            type (str): The type of the item
            format (str): The format of the item
        Returns:
            dict: The item definition
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/getDefinition"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{type}/{item_id}/getDefinition"

        if format:
            url += f"?format={format}"

        return self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                    error_message="Error getting item definition",
                                    return_format="json+operation_result")
    
    
    def update_item(self, workspace_id, item_id, display_name = None, description = None, type = None, return_item="Default"):
        """Update the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            display_name (str): The display name of the item
            description (str): The description of the item
            type (str): The type of the item
        Returns:
            dict: The updated item
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}"
        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{type}/{item_id}"

        payload = dict()
        if display_name:
            payload['displayName'] = display_name
        if description:
            payload['description'] = description

        resp_dict = self.calling_routine(url, operation="PATCH", body=payload,
                                         response_codes=[200, 429], error_message="Error updating item",
                                         return_format="json")
        if return_item == "Default":
            warn(
                message="Updating an item currently will make invoke an additional API call to get the item object. "
                        "The default behaviour of returning the item object will change in newer versions of the SDK. "
                        "To keep this behaviour, set return_item=True in the function call.",
                category=FutureWarning,
                stacklevel=2
            )
        if return_item:
            return self.get_item_specific(workspace_id, resp_dict)
        return resp_dict

    def update_item_definition(self, workspace_id, item_id, definition, type = None, wait_for_completion=True):
        """Update the item definition
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            definition (dict): The definition of the item
            type (str): The type of the item
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/updateDefinition"

        if type:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{type}/{item_id}/updateDefinition"
            
        payload = {
            'definition': definition
        }

        response = self.calling_routine(url, operation="POST", body=payload, response_codes=[200, 202, 429],
                                        error_message="Error updating item definition", return_format="response",
                                        wait_for_completion=wait_for_completion)
        return response

    # Job Scheduler
    
    def cancel_item_job_instance(self, workspace_id, item_id, job_instance_id):
        """Cancel the job instance
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_instance_id (str): The ID of the job instance
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/instances/{job_instance_id}/cancel"
        
        response = self.calling_routine(url=url, operation="POST", response_codes=[202, 429],
                                        error_message="Error cancelling job instance", return_format="response",
                                        wait_for_completion=False)

        return response.status_code
    

    def get_item_job_instance(self, workspace_id, item_id, job_instance_id):
        """Get the job instance of the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_instance_id (str): The ID of the job instance
        Returns:
            JobInstance: The job instance object
        """
        from msfabricpysdkcore.job_instance import JobInstance

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/instances/{job_instance_id}"
        
        job_dict = self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                        error_message="Error getting job instance", return_format="json")
        
        job_dict['workspaceId'] = workspace_id
        job_dict['itemId'] = item_id
        return JobInstance.from_dict(job_dict, core_client=self)
    

    def run_on_demand_item_job(self, workspace_id, item_id, job_type, execution_data = None):
        """Run an on demand job on the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_type (str): The type of the job
            execution_data (dict): The execution data of the job
        Returns:
            JobInstance: The job instance object
        """

        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/jobs/instances?jobType={jobType}
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/instances?jobType={job_type}"
        payload = {
            'executionData': execution_data
        }

        response = self.calling_routine(url, operation="POST", body=payload, response_codes=[202, 429],
                                        error_message="Error running on demand job",
                                        wait_for_completion=False, return_format="response")

        job_instance_id = response.headers["Location"].split("/")[-1]
        job_instance = self.get_item_job_instance(workspace_id, item_id, job_instance_id=job_instance_id)
        return job_instance
    
    # long running operations

    def get_operation_results(self, operation_id):
        """Get the results of an operation
        Args:
            operation_id (str): The ID of the operation
        Returns:
            dict: The results of the operation
        """
        url = f"https://api.fabric.microsoft.com/v1/operations/{operation_id}/result"

        response = self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting operation results", return_format="response",
                                             continue_on_error_code=True)
        if response.status_code == 400:
            return {"no_operation_result": True}
        return json.loads(response.text)
    
    def get_operation_state(self, operation_id):
        """Get the state of an operation
        Args:
            operation_id (str): The ID of the operation
        Returns:
            dict: The state of the operation
        """ 
        url = f"https://api.fabric.microsoft.com/v1/operations/{operation_id}"

        response_json = self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting operation state", return_format="json")

        return response_json

    # One Lake Data Access Security

    # create and update

    def create_or_update_data_access_roles(self, workspace_id, item_id, data_access_roles, dryrun = False, etag_match = None):
        # PUT https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/dataAccessRoles

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/dataAccessRoles"

        if dryrun:
            url += "?dryrun=true"
        
        headers = self.auth.get_headers()
        if etag_match:
            if 'If-Match' in etag_match:
                headers['If-Match'] = etag_match['If-Match']
            elif 'If-None-Match' in etag_match:
                headers['If-None-Match'] = etag_match['If-None-Match']
            else:
                raise Exception("Etag match should include If-Match or If-None-Match")

        body = {"value" : data_access_roles}

        response = self.calling_routine(url, operation="PUT", body=body, headers=headers, 
                                        response_codes=[200, 429], error_message="Error creating or updating data access roles", return_format="response")

        return response
    
    
    # list 
    
    def list_data_access_roles(self, workspace_id, item_id):

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/dataAccessRoles"

        items, etag = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error listing data access roles", return_format="value_json+etag")
        return items, etag
    
    # ShortCuts

    def create_shortcut(self, workspace_id, item_id, path, name, target):
        """Create a shortcut in the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            path (str): The path of the shortcut
            name (str): The name of the shortcut
            target (str): The target of the shortcut
        Returns:
            OneLakeShortcut: The created shortcut
        """
        from msfabricpysdkcore.onelakeshortcut import OneLakeShortcut

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/shortcuts"

        body = {'name': name,
                'path': path,
                'target': target}
        
        response_json = self.calling_routine(url, operation="POST", body=body,
                                             response_codes=[201, 429], error_message="Error creating shortcut",
                                             return_format="json")

        shortcut_dict = response_json
        shortcut_dict['workspaceId'] = workspace_id
        shortcut_dict['itemId'] = item_id
        return OneLakeShortcut.from_dict(shortcut_dict,
                                         core_client = self)
    

    def get_shortcut(self, workspace_id, item_id, path, name):
        """Get the shortcut in the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            path (str): The path of the shortcut
            name (str): The name of the shortcut
        Returns:
            OneLakeShortcut: The shortcut object
        """
        from msfabricpysdkcore.onelakeshortcut import OneLakeShortcut
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/shortcuts/{path}/{name}"
        
        shortcut_dict = self.calling_routine(url=url, operation="GET",
                                             response_codes=[200, 429], error_message="Error getting shortcut",
                                             return_format="json")

        shortcut_dict['workspaceId'] = workspace_id
        shortcut_dict['itemId'] = id
        return OneLakeShortcut.from_dict(shortcut_dict,
                                         core_client = self)
    
    def delete_shortcut(self, workspace_id, item_id, path, name):
        """Delete the shortcut
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            path (str): The path of the shortcut
            name (str): The name of the shortcut
        Returns:
            int: The status code of the response
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/shortcuts/{path}/{name}"
        response = self.calling_routine(url=url, operation="DELETE",
                                             response_codes=[200, 429], error_message="Error creating shortcut",
                                             return_format="response")


        return response.status_code
    
    ### Workspaces

    def add_workspace_role_assignment(self, workspace_id, role, principal):
        """Add a role assignment to a workspace
        Args:
            workspace_id (str): The ID of the workspace
            role (str): The role to assign
            principal (str): The principal to assign the role to    
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments"

        payload = {
            'principal': principal,
            'role': role
        }

        response = self.calling_routine(url, operation="POST", body=payload, response_codes=[201, 429], error_message="Error adding role assignments", return_format="response")

        return response.status_code
    
    def assign_to_capacity(self, workspace_id, capacity_id, wait_for_completion=True):
        """Assign a workspace to a capacity
        Args:
            workspace_id (str): The ID of the workspace
            capacity_id (str): The ID of the capacity
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/assignToCapacity"

        body = {
            'capacityId': capacity_id
        }

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[202, 429], error_message="Error assigning capacity", return_format="response", wait_for_completion=wait_for_completion)

        return response.status_code
    
    def create_workspace(self, display_name, capacity_id = None, description = None, exists_ok = True):
        """Create a workspace
        Args:
            display_name (str): The display name of the workspace
            capacity_id (str): The ID of the capacity to assign the workspace to
            description (str): The description of the workspace
            exists_ok (bool): Whether to return the existing workspace if it already exists
        Returns:
            Workspace: The created workspace
        """
        from msfabricpysdkcore.workspace import Workspace

        body = dict()
        body["displayName"] = display_name
        if capacity_id:
            body["capacityId"] = capacity_id
        if description:
            body["description"] = description
        
        url = "https://api.fabric.microsoft.com/v1/workspaces"

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429], error_message="Error creating workspace", return_format="response", continue_on_error_code=True)
        ws_dict = json.loads(response.text)
        if response.status_code not in (201, 429):
            if "errorCode" in ws_dict and ws_dict["errorCode"] == "WorkspaceNameAlreadyExists" and exists_ok:
                return self.get_workspace_by_name(display_name)
            else:
                raise Exception(f"Error creating workspace: {response.status_code}, {response.text}")

        ws = Workspace.from_dict(ws_dict, core_client=self)
        return ws
    
    def delete_workspace(self, workspace_id = None, display_name = None):
        """Delete a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the workspace
        Returns:
            int: The status code of the response
        """
        if workspace_id is None and display_name is None:
            raise ValueError("Either workspace_id or display_name must be provided")
        if workspace_id is None:
            ws = self.get_workspace_by_name(display_name)
            workspace_id = ws.id

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], error_message="Error deleting workspace", return_format="response")

        return response.status_code
    
    def delete_workspace_role_assignment(self, workspace_id, workspace_role_assignment_id):
        """Delete a role assignment from the workspace
        Args:
            workspace_id (str): The ID of the workspace
            workspace_role_assignment_id (str): The ID of the role assignment
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments/{workspace_role_assignment_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], error_message="Error deleting role assignments", return_format="response")
        
        return response.status_code
    
    def deprovision_identity(self, workspace_id):
        """Deprovision an identity for a workspace
        Args:
            workspace_id (str): The ID of the workspace 
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/deprovisionIdentity"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 201, 202, 429], error_message="Error deprovisioning identity", return_format="response")

        return response

    def get_workspace(self, id = None, name = None):
        """Get workspace by id or name
        Args:
            id (str): The ID of the workspace
            name (str): The name of the workspace
        Returns:
            Workspace: The workspace object
        Raises:
            ValueError: If neither id nor name is provided
        """
        if id:
            return self.get_workspace_by_id(id)
        if name:
            return self.get_workspace_by_name(name)
        raise ValueError("Either id or name must be provided")
    
    def get_workspace_by_id(self, id):
        """Get workspace by id
        Args:
            id (str): The ID of the workspace
        Returns:
            Workspace: The workspace object
        """
        from msfabricpysdkcore.workspace import Workspace

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{id}"

        ws_dict = self.calling_routine(url, operation="GET", response_codes=[200, 404], error_message="Error getting workspace", return_format="json")

        ws = Workspace.from_dict(ws_dict, core_client=self)

        return ws

    def get_workspace_by_name(self, name):
        """Get workspace by name
        Args:
            name (str): The name of the workspace
        Returns:
            Workspace: The workspace object
        """
        ws_list = self.list_workspaces()
        for ws in ws_list:
            if ws.display_name == name:
                return ws
            
    def get_workspace_role_assignment(self, workspace_id, workspace_role_assignment_id):
        """Get a role assignment for a workspace
        Args:
            workspace_id (str): The ID of the workspace
            workspace_role_assignment_id (str): The ID of the role assignment
        Returns:
            dict: The role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments/{workspace_role_assignment_id}"

        return self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting role assignments", return_format="json")
           
    def list_workspace_role_assignments(self, workspace_id):
        """List role assignments for the workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            list: The list of role assignments
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments"

       
        role_assignments = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                                error_message="Error listing workspace role assignments", return_format = "value_json",
                                                paging = True)

        return role_assignments
       
    def list_workspaces(self):
        """List all workspaces in the tenant
        Returns:
            list: The list of workspaces
        """
        from msfabricpysdkcore.workspace import Workspace

        url = "https://api.fabric.microsoft.com/v1/workspaces"

        ws_list = self.calling_routine(url, operation="GET", response_codes=[200], error_message="Error listing workspaces", return_format="value_json", paging=True)
        ws_list = [Workspace.from_dict(ws, core_client=self) for ws in ws_list]

        return ws_list

    def provision_identity(self, workspace_id):
        """Provision an identity for a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/provisionIdentity"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 201, 202, 429], error_message="Error provisioning identity", return_format="response")
        return response
    
    def unassign_from_capacity(self, workspace_id, wait_for_completion = True):        
        """Unassign a workspace from a capacity
        Args:
            workspace_id (str): The ID of the workspace
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/unassignFromCapacity"

        response = self.calling_routine(url, operation="POST", response_codes=[202, 429], error_message="Error unassigning capacity", return_format="response", wait_for_completion=wait_for_completion)

        return response.status_code

        
    def update_workspace(self, workspace_id, display_name = None, description = None):
        """Update the workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the workspace
            description (str): The description of the workspace
        Returns:
            Workspace: The updated workspace
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"

        body = dict()
        if display_name:
            body["displayName"] = display_name
        if description:
            body["description"] = description

        response = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429], error_message="Error updating workspace", return_format="response")

        assert response.status_code == 200

        return self.get_workspace_by_id(workspace_id)


    def update_workspace_role_assignment(self, workspace_id, role, workspace_role_assignment_id):
        """Update a role assignment for a workspace
        Args:
            workspace_id (str): The ID of the workspace
            role (str): The role to assign
            workspace_role_assignment_id (str): The ID of the role assignment
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments/{workspace_role_assignment_id}"
        body = {
            'role': role
        }

        response = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429], error_message="Error updating role assignments", return_format="response")

        return response.status_code   


    
    # list things
    def list_dashboards(self, workspace_id):
        """List dashboards in a workspace"""
        return self.list_items(workspace_id, type="dashboards")
    
    def list_datamarts(self, workspace_id):
        """List datamarts in a workspace"""
        return self.list_items(workspace_id, type="datamarts")
    
    def list_paginated_reports(self, workspace_id):
        """List paginated reports in a workspace"""
        return self.list_items(workspace_id, type="paginatedReports")

    def list_sql_endpoints(self, workspace_id):
        """List sql endpoints in a workspace"""
        return self.list_items(workspace_id, type="sqlEndpoints")

    def list_mirrored_warehouses(self, workspace_id):
        """List mirrored warehouses in a workspace"""
        return self.list_items(workspace_id, type="mirroredWarehouses")
    
    # dataPipelines

    def create_data_pipeline(self, workspace_id, display_name, definition = None, description = None):
        """Create a data pipeline in a workspace"""
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "dataPipelines",
                                definition = definition,
                                description = description)
    
    def delete_data_pipeline(self, workspace_id, data_pipeline_id):
        """Delete a data pipeline from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            data_pipeline_id (str): The ID of the data pipeline
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=data_pipeline_id, type="dataPipelines")
    
    def get_data_pipeline(self, workspace_id, data_pipeline_id = None, data_pipeline_name = None):
        """Get a data pipeline from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            data_pipeline_id (str): The ID of the data pipeline
            data_pipeline_name (str): The name of the data pipeline
        Returns:
            DataPipeline: The data pipeline object
        """
        from msfabricpysdkcore.otheritems import DataPipeline

        if data_pipeline_id is None and data_pipeline_name is not None:
            data_pipelines = self.list_data_pipelines(workspace_id)
            dps = [dp for dp in data_pipelines if dp.display_name == data_pipeline_name]
            if len(dps) == 0:
                raise Exception(f"Data pipeline with name {data_pipeline_name} not found")
            data_pipeline_id = dps[0].id
        elif data_pipeline_id is None:
            raise Exception("data_pipeline_id or the data_pipeline_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines/{data_pipeline_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting data pipeline", return_format="json")

        dp = DataPipeline.from_dict(item_dict, core_client=self)
        dp.get_definition()
        return dp
    
    def list_data_pipelines(self, workspace_id, with_properties = False):
        """List data pipelines in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of data pipelines
        """
        return self.list_items(workspace_id, type="dataPipelines", with_properties=with_properties)
    
    def update_data_pipeline(self, workspace_id, data_pipeline_id, display_name = None, description = None, return_item="Default"):
        """Update a data pipeline in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            data_pipeline_id (str): The ID of the data pipeline
            display_name (str): The display name of the data pipeline
            description (str): The description of the data pipeline
        Returns:
            dict: The updated data pipeline
        """
        return self.update_item(workspace_id, item_id=data_pipeline_id, display_name=display_name, description=description, type="dataPipelines",
                                return_item=return_item)
    

    # environments

    def create_environment(self, workspace_id, display_name, description = None):
        """Create an environment in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the environment
            description (str): The description of the environment
        Returns:
            dict: The created environment
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "environments",
                                definition = None,
                                description = description)
    
    def delete_environment(self, workspace_id, environment_id):
        """Delete an environment from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=environment_id, type="environments")
    
    def get_environment(self, workspace_id, environment_id = None, environment_name = None):
        """Get an environment from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            environment_name (str): The name of the environment
        Returns:
            dict: The environment
        """
        from msfabricpysdkcore.environment import Environment
        if environment_id is None and environment_name is not None:
            envs = self.list_environments(workspace_id)
            envs = [env for env in envs if env.display_name == environment_name]
            if len(envs) == 0:
                raise Exception(f"Environment with name {environment_name} not found")
            environment_id = envs[0].id
        elif environment_id is None:
            raise Exception("environment_id or the environment_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}"
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting environment", return_format="json")
        env = Environment.from_dict(item_dict, core_client=self)
        return env

    def list_environments(self, workspace_id, with_properties = False):
        """List environments in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of environments
        """
        return self.list_items(workspace_id, type="environments", with_properties=with_properties)
    
    def update_environment(self, workspace_id, environment_id, display_name = None, description = None, return_item="Default"):
        """Update an environment in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            display_name (str): The display name of the environment
            description (str): The description of the environment
        Returns:
            dict: The updated environment
        """
        return self.update_item(workspace_id, item_id=environment_id, display_name=display_name, description=description, 
                                type="environments", return_item=return_item)

    # environmentSparkCompute

    def get_published_settings(self, workspace_id, environment_id):
        """Get the published settings of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The published settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/sparkcompute"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting published settings", return_format="json")     
        return resp_json

    def get_staging_settings(self, workspace_id, environment_id):
        """Get the staging settings of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The staging settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/sparkcompute"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting staging settings", return_format="json")       
        return resp_json
    
    def update_staging_settings(self, workspace_id, environment_id,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None):
        """Update the staging settings of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            driver_cores (int): The number of driver cores
            driver_memory (str): The memory for the driver
            dynamic_executor_allocation (bool): Whether to dynamically allocate executors
            executor_cores (int): The number of executor cores
            executor_memory (str): The memory for the executor
            instance_pool (str): The instance pool
            runtime_version (str): The runtime version
            spark_properties (dict): The spark properties
        Returns:
            dict: The updated staging settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/sparkcompute"
        body = {}
        if driver_cores is not None:
            body['driverCores'] = driver_cores
        if driver_memory is not None:
            body['driverMemory'] = driver_memory
        if dynamic_executor_allocation is not None:
            body['dynamicExecutorAllocation'] = dynamic_executor_allocation
        if executor_cores is not None:
            body['executorCores'] = executor_cores
        if executor_memory is not None:
            body['executorMemory'] = executor_memory
        if instance_pool is not None:
            body['instancePool'] = instance_pool
        if runtime_version is not None:
            body['runtimeVersion'] = runtime_version
        if spark_properties is not None:
            body['sparkProperties'] = spark_properties

        respone_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                            error_message="Error updating staging settings", return_format="json")

        return respone_json


    # environmentSparkLibraries
    
    def cancel_publish(self, workspace_id, environment_id):
        """Cancel the publishing of the staging settings and libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/cancelPublish"

        resp_dict = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error canceling publish", return_format="json")
        return resp_dict
    
    def delete_staging_library(self, workspace_id, environment_id, library_to_delete):
        """Delete a library from the staging libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            library_to_delete (str): The library to delete
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries?libraryToDelete={library_to_delete}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], error_message="Error deleting staging library", return_format="response")

        return response
    
    def get_published_libraries(self, workspace_id, environment_id):
        """Get the published libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The published libraries
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/libraries"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting published libraries", return_format="json")
        return resp_json
    
    def get_staging_libraries(self, workspace_id, environment_id):
        """Get the staging libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The staging libraries
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting staging libraries", return_format="json")
        return resp_json
    
    def publish_environment(self, workspace_id, environment_id):
        """Publish the staging settings and libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/publish"

        resp_dict = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error publishing staging",
                                         return_format="json+operation_result")

        return resp_dict
    
    def upload_staging_library(self, workspace_id, environment_id, file_path):
        """Update staging libraries for an environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            file_path (str): The file path to upload
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"
        response = self.calling_routine(url, operation="POST", file_path=file_path, response_codes=[200, 429],
                                        error_message="Error uploading staging library", return_format="response")
        return response
    

    
    # eventhouses

    def create_eventhouse(self, workspace_id, display_name, description = None):
        """Create an eventhouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the eventhouse
            description (str): The description of the eventhouse
        Returns:
            Eventhouse: The created eventhouse
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "eventhouses",
                                definition = None,
                                description = description)

    def delete_eventhouse(self, workspace_id, eventhouse_id):
        """Delete an eventhouse from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            eventhouse_id (str): The ID of the eventhouse
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, eventhouse_id, type="eventhouses")
    
    def get_eventhouse(self, workspace_id, eventhouse_id = None, eventhouse_name = None):
        """Get an eventhouse from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            eventhouse_id (str): The ID of the eventhouse
            eventhouse_name (str): The name of the eventhouse
        Returns:
            Eventhouse: The eventhouse object
        """
        from msfabricpysdkcore.otheritems import Eventhouse
        if eventhouse_id is None and eventhouse_name is not None:
            ehs = self.list_eventhouses(workspace_id)
            ehs = [eh for eh in ehs if eh.display_name == eventhouse_name]
            if len(ehs) == 0:
                raise Exception(f"Eventhouse with name {eventhouse_name} not found")
            eventhouse_id = ehs[0].id
        if eventhouse_id is None:
            raise Exception("eventhouse_id or the eventhouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses/{eventhouse_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting eventhouse", return_format="json")
        return Eventhouse.from_dict(item_dict, core_client=self)
    
    def list_eventhouses(self, workspace_id, with_properties = False):
        """List eventhouses in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of eventhouses
        """
        return self.list_items(workspace_id=workspace_id, type="eventhouses", with_properties=with_properties)
    
    def update_eventhouse(self, workspace_id, eventhouse_id, display_name = None, description = None, return_item="Default"):
        """Update an eventhouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            eventhouse_id (str): The ID of the eventhouse
            display_name (str): The display name of the eventhouse
            description (str): The description of the eventhouse
        Returns:
            dict: The updated eventhouse
        """
        return self.update_item(workspace_id=workspace_id, item_id=eventhouse_id,
                                display_name=display_name, description=description, type="eventhouses", return_item=return_item)

    # eventstreams

    def create_eventstream(self, workspace_id, display_name, description = None):
        """Create an eventstream in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the eventstream
            description (str): The description of the eventstream
        Returns:
            dict: The created eventstream
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "eventstreams",
                                definition = None,
                                description = description)
    

    def get_eventstream(self, workspace_id, eventstream_id = None, eventstream_name = None):
        """Get an eventstream from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            eventstream_name (str): The name of the eventstream
        Returns:
            Eventstream: The eventstream object
        """
        from msfabricpysdkcore.otheritems import Eventstream
        if eventstream_id is None and eventstream_name is not None:
            evstreams = self.list_eventstreams(workspace_id)
            evstreams = [ev for ev in evstreams if ev.display_name == eventstream_name]
            if len(evstreams) == 0:
                raise Exception(f"Eventstream with name {eventstream_name} not found")
            eventstream_id = evstreams[0].id
        if eventstream_id is None:
            raise Exception("eventstream_id or the eventstream_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting eventstream", return_format="json")
        return Eventstream.from_dict(item_dict, core_client=self)
    
    def delete_eventstream(self, workspace_id, eventstream_id):
        """Delete an eventstream from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, eventstream_id, type="eventstreams")
    
    def list_eventstreams(self, workspace_id, with_properties = False):
        """List eventstreams in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of event
        """
        return self.list_items(workspace_id=workspace_id, type="eventstreams", with_properties=with_properties)

    def update_eventstream(self, workspace_id, eventstream_id, display_name = None, description = None, return_item="Default"):
        """Update an eventstream in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            display_name (str): The display name of the eventstream
            description (str): The description of the eventstream
        Returns:
            dict: The updated eventstream
        """
        return self.update_item(workspace_id, eventstream_id, display_name = display_name, description = description, 
                                type= "eventstreams", return_item=return_item)

    # kqlDatabases

    def create_kql_database(self, workspace_id, creation_payload, display_name, description = None):
        """Create a kql database in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            creation_payload (dict): The creation payload
            display_name (str): The display name of the kql database
            description (str): The description of the kql database
        Returns:
            dict: The created kql database
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "kqlDatabases",
                                description = description,
                                creation_payload = creation_payload)
    
    def delete_kql_database(self, workspace_id, kql_database_id):
        """Delete a kql database from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_database_id (str): The ID of the kql database
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, kql_database_id, type="kqlDatabases")
       
    def get_kql_database(self, workspace_id, kql_database_id = None, kql_database_name = None):
        """Get a kql database from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_database_id (str): The ID of the kql database
            kql_database_name (str): The name of the kql database
        Returns:
            KQLDatabase: The kql database object
        """
        from msfabricpysdkcore.otheritems import KQLDatabase
        if kql_database_id is None and kql_database_name is not None:
            kql_databases = self.list_kql_databases(workspace_id)
            kql_databases = [kd for kd in kql_databases if kd.display_name == kql_database_name]
            if len(kql_databases) == 0:
                raise Exception(f"Kql database with name {kql_database_name} not found")
            kql_database_id = kql_databases[0].id
        if kql_database_id is None:
            raise Exception("kql_database_id or the kql_database_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/kqlDatabases/{kql_database_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting kql database", return_format="json")
        return KQLDatabase.from_dict(item_dict, core_client=self)

    def list_kql_databases(self, workspace_id, with_properties = False):
        """List kql databases in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of kql databases"""
        return self.list_items(workspace_id=workspace_id, type="kqlDatabases", with_properties=with_properties)
    
    def update_kql_database(self, workspace_id, kql_database_id, display_name = None, description = None, return_item="Default"):
        """Update a kql database in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_database_id (str): The ID of the kql database
            display_name (str): The display name of the kql database
            description (str): The description of the kql database
        Returns:
            dict: The updated kql database
        """
        return self.update_item(workspace_id, kql_database_id, display_name = display_name,
                                description = description, type= "kqlDatabases", return_item=return_item)

    # kqlQuerysets

        
    def delete_kql_queryset(self, workspace_id, kql_queryset_id):
        """Delete a kql queryset from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_queryset_id (str): The ID of the kql queryset
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, kql_queryset_id, type="kqlQuerysets")
    
    def get_kql_queryset(self, workspace_id, kql_queryset_id = None, kql_queryset_name = None):
        """Get a kql queryset from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_queryset_id (str): The ID of the kql queryset
            kql_queryset_name (str): The name of the kql queryset
        Returns:
            KQLQueryset: The kql queryset object
        """
        from msfabricpysdkcore.otheritems import KQLQueryset
        if kql_queryset_id is None and kql_queryset_name is not None:
            kql_querysets = self.list_kql_querysets(workspace_id)
            kql_querysets = [kq for kq in kql_querysets if kq.display_name == kql_queryset_name]
            if len(kql_querysets) == 0:
                raise Exception(f"Kql queryset with name {kql_queryset_name} not found")
            kql_queryset_id = kql_querysets[0].id
        if kql_queryset_id is None:
            raise Exception("kql_queryset_id or the kql_queryset_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/kqlQuerysets/{kql_queryset_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting kql queryset", return_format="json")
        
        return KQLQueryset.from_dict(item_dict, core_client=self)

    def update_kql_queryset(self, workspace_id, kql_queryset_id, display_name = None, description = None, return_item="Default"):
        """Update a kql queryset in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_queryset_id (str): The ID of the kql queryset
            display_name (str): The display name of the kql queryset
            description (str): The description of the kql queryset
        Returns:
            dict: The updated kql queryset
        """
        return self.update_item(workspace_id, kql_queryset_id, display_name = display_name,
                                description = description, type= "kqlQuerysets", return_item=return_item)

    def list_kql_querysets(self, workspace_id, with_properties = False):
        """List kql querysets in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of kql querysets
        """
        return self.list_items(workspace_id=workspace_id, type="kqlQuerysets", with_properties=with_properties)


    # lakehouses

    def run_on_demand_table_maintenance(self, workspace_id, lakehouse_id, 
                                        execution_data = None,
                                        job_type = "TableMaintenance", wait_for_completion = False):
        """Run on demand table maintenance
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            execution_data (dict): The execution data
            job_type (str): The job type
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/instances?jobType={job_type}"

        body = {
                "executionData": execution_data
              }
        
        respone_operation_result = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 202, 429],
                                                        error_message="Error running on demand table maintenance",
                                                        return_format="response+operation_result", wait_for_completion=wait_for_completion)

        return respone_operation_result
    
    def create_lakehouse(self, workspace_id, display_name, description = None):
        """Create a lakehouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the lakehouse
            description (str): The description of the lakehouse
        Returns:
            dict: The created lakehouse
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "lakehouses",
                                description = description)
    
    def delete_lakehouse(self, workspace_id, lakehouse_id):
        """Delete a lakehouse from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, lakehouse_id, type="lakehouses")
    
    def get_lakehouse(self, workspace_id, lakehouse_id = None, lakehouse_name = None):
        """Get a lakehouse from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            lakehouse_name (str): The name of the lakehouse
        Returns:
            Lakehouse: The lakehouse object
        """
        from msfabricpysdkcore.lakehouse import Lakehouse
        if lakehouse_id is None and lakehouse_name is not None:
            lakehouses = self.list_lakehouses(workspace_id)
            lakehouses = [lh for lh in lakehouses if lh.display_name == lakehouse_name]
            if len(lakehouses) == 0:
                raise Exception(f"Lakehouse with name {lakehouse_name} not found")
            lakehouse_id = lakehouses[0].id
        if lakehouse_id is None:
            raise Exception("lakehouse_id or the lakehouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting lakehouse", return_format="json")
        return Lakehouse.from_dict(item_dict, core_client=self)
    
    def list_lakehouses(self, workspace_id, with_properties = False):
        """List lakehouses in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of lakehouses
        """
        return self.list_items(workspace_id, type="lakehouses", with_properties = with_properties)

    def update_lakehouse(self, workspace_id, lakehouse_id, display_name = None, description = None, return_item="Default"):
        """Update a lakehouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            display_name (str): The display name of the lakehouse
            description (str): The description of the lakehouse
        Returns:
            dict: The updated lakehouse
        """
        return self.update_item(workspace_id, item_id=lakehouse_id, display_name = display_name, description = description,
                                type="lakehouses", return_item=return_item)


    def list_tables(self, workspace_id, lakehouse_id):
        """List all tables in the lakehouse
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
        Returns:
            list: The list of tables
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                        error_message="Error listing tables", return_format="data", paging=True)

        return items
        
    def check_if_table_is_created(self, workspace_id, lakehouse_id, table_name):
        """Check if the table is created
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            table_name (str): The name of the table
        Returns:
            bool: Whether the table is created
        """
        for _ in range(60):
            table_names = [table["name"] for table in self.list_tables(workspace_id, lakehouse_id)]
            if table_name in table_names:
                return True
            sleep(3)
        return False
    
    def load_table(self, workspace_id, lakehouse_id, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        """Load a table in the lakehouse
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            table_name (str): The name of the table
            path_type (str): The path type
            relative_path (str): The relative path
            file_extension (str): The file extension
            format_options (dict): The format options
            mode (str): The mode
            recursive (bool): Whether to load recursively
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables/{table_name}/load"

        body = {
                "relativePath": relative_path,
                "pathType": path_type,
              }

        if file_extension:
            body["fileExtension"] = file_extension
        if format_options:
            body["formatOptions"] = format_options
        if mode:
            body["mode"] = mode
        if recursive:
            body["recursive"] = recursive

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[202, 429],
                                        error_message="Error loading table", return_format="response",
                                        wait_for_completion=False)

        if wait_for_completion:
            success = self.check_if_table_is_created(workspace_id = workspace_id,
                                                     lakehouse_id = lakehouse_id,
                                                     table_name = table_name)
        else:
            success = None

        if not success:
            self._logger.warning("Table not created after 3 minutes")
        else:
            self._logger.info("Table created")
        return response.status_code

    # mlExperiments


    def create_ml_experiment(self, workspace_id, display_name, description = None):
        """Create an ml experiment in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the ml experiment
            description (str): The description of the ml experiment
        Returns:
            dict: The created ml experiment
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "mlExperiments",
                                description = description)
    
    def delete_ml_experiment(self, workspace_id, ml_experiment_id):
        """Delete an ml experiment from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            ml_experiment_id (str): The ID of the ml experiment
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, ml_experiment_id, type="mlExperiments")
    
    def get_ml_experiment(self, workspace_id, ml_experiment_id = None, ml_experiment_name = None):
        """Get an ml experiment from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            ml_experiment_id (str): The ID of the ml experiment
            ml_experiment_name (str): The name of the ml experiment
        Returns:
            MLExperiment: The ml experiment object
        """
        from msfabricpysdkcore.otheritems import MLExperiment
        if ml_experiment_id is None and ml_experiment_name is not None:
            ml_experiments = self.list_ml_experiments(workspace_id)
            ml_experiments = [ml for ml in ml_experiments if ml.display_name == ml_experiment_name]
            if len(ml_experiments) == 0:
                raise Exception(f"ML experiment with name {ml_experiment_name} not found")
            ml_experiment_id = ml_experiments[0].id
        if ml_experiment_id is None:
            raise Exception("ml_experiment_id or the ml_experiment_name is required")
              
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlExperiments/{ml_experiment_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting ml experiment", return_format="json")
        return MLExperiment.from_dict(item_dict, core_client=self)
    
    def list_ml_experiments(self, workspace_id, with_properties = False):
        """List ml experiments in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of ml experiments
        """
        return self.list_items(workspace_id=workspace_id, type="mlExperiments", with_properties = with_properties)
    
    def update_ml_experiment(self, workspace_id, ml_experiment_id, display_name = None, description = None, return_item="Default"):
        """Update an ml experiment in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            ml_experiment_id (str): The ID of the ml experiment
            display_name (str): The display name of the ml experiment
            description (str): The description of the ml experiment
        Returns:
            dict: The updated ml experiment
        """
        return self.update_item(workspace_id, ml_experiment_id, display_name = display_name, description = description,
                                type="mlExperiments", return_item=return_item)
  
    # mlModels

    def create_ml_model(self, workspace_id, display_name, description = None):
        """Create an ml model in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the ml model
            description (str): The description of the ml model
        Returns:
            dict: The created ml model
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "mlModels", description = description,
                                wait_for_completion = True)
    
    def delete_ml_model(self, workspace_id, ml_model_id):
        """Delete an ml model from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            ml_model_id (str): The ID of the ml model
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, ml_model_id, type="mlModels")

    def get_ml_model(self, workspace_id, ml_model_id = None, ml_model_name = None):
        """Get an ml model from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            ml_model_id (str): The ID of the ml model
            ml_model_name (str): The name of the ml model
        Returns:
            MLModel: The ml model object
        """
        from msfabricpysdkcore.otheritems import MLModel
        if ml_model_id is None and ml_model_name is not None:
            ml_models = self.list_ml_models(workspace_id)
            ml_models = [ml for ml in ml_models if ml.display_name == ml_model_name]
            if len(ml_models) == 0:
                raise Exception(f"ML model with name {ml_model_name} not found")
            ml_model_id = ml_models[0].id
        if ml_model_id is None:
            raise Exception("ml_model_id or the ml_model_name is required")

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlModels/{ml_model_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting ml model", return_format="json")
        
        return MLModel.from_dict(item_dict, core_client=self)

    def list_ml_models(self, workspace_id, with_properties=False):
        """List ml models in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of ml models
        """
        return self.list_items(workspace_id=workspace_id, type="mlModels", with_properties = with_properties)
    
    def update_ml_model(self, workspace_id, ml_model_id, display_name = None, description = None, return_item="Default"):
        """Update an ml model in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            ml_model_id (str): The ID of the ml model
            display_name (str): The display name of the ml model
            description (str): The description of the ml model
        Returns:    
            dict: The updated ml model
        """
        return self.update_item(workspace_id, ml_model_id, display_name = display_name, description = description,
                                type="mlModels", return_item=return_item)
    
    # notebooks

    def create_notebook(self, workspace_id, display_name, definition = None, description = None):
        """Create a notebook in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the notebook
            definition (dict): The definition of the notebook
            description (str): The description of the notebook
        Returns:
            dict: The created notebook
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "notebooks", definition = definition, description = description)
    
    def get_notebook(self, workspace_id, notebook_id = None, notebook_name = None):
        """Get a notebook from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
            notebook_name (str): The name of the notebook
        Returns:
            Notebook: The notebook object"""
        from msfabricpysdkcore.otheritems import Notebook
        if notebook_id is None and notebook_name is not None:
            notebooks = self.list_notebooks(workspace_id)
            notebooks = [nb for nb in notebooks if nb.display_name == notebook_name]
            if len(notebooks) == 0:
                raise Exception(f"Notebook with name {notebook_name} not found")
            notebook_id = notebooks[0].id
        if notebook_id is None:
            raise Exception("notebook_id or the notebook_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks/{notebook_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting notebook", return_format="json")
        
        notebook = Notebook.from_dict(item_dict, core_client=self)
        notebook.get_definition()
        return notebook

    
    def get_notebook_definition(self, workspace_id, notebook_id, format = None):
        """Get the definition of a notebook
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
            format (str): The format of the definition
        Returns:
            dict: The definition of the notebook
        """
        return self.get_item_definition(workspace_id, notebook_id, type="notebooks", format=format)

    def delete_notebook(self, workspace_id, notebook_id):
        """Delete a notebook from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, notebook_id, type="notebooks")

    def list_notebooks(self, workspace_id, with_properties = False):
        """List notebooks in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of notebooks
        """
        return self.list_items(workspace_id = workspace_id, type = "notebooks", with_properties = with_properties)
    
    def update_notebook(self, workspace_id, notebook_id, display_name = None, description = None, return_item="Default"):
        """Update a notebook in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
            display_name (str): The display name of the notebook
            description (str): The description of the notebook
        Returns:
            dict: The updated notebook
        """
        return self.update_item(workspace_id, notebook_id, display_name = display_name, description = description,
                                type="notebooks", return_item=return_item)
    
    def update_notebook_definition(self, workspace_id, notebook_id, definition):
        """Update the definition of a notebook
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
            definition (dict): The definition of the notebook
        Returns:
            dict: The updated notebook
        """
        return self.update_item_definition(workspace_id, notebook_id, definition, type="notebooks")
    
    # reports

    def create_report(self, workspace_id, display_name, definition = None, description = None):
        """Create a report in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the report
            definition (dict): The definition of the report
            description (str): The description of the report
        Returns:
            dict: The created report
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "reports", definition = definition, description = description)
    
    def delete_report(self, workspace_id, report_id):
        """Delete a report from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            report_id (str): The ID of the report
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, report_id, type="reports")
    
    def get_report(self, workspace_id, report_id = None, report_name = None):
        """Get a report from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            report_id (str): The ID of the report
            report_name (str): The name of the report
        Returns:
            Report: The report object
        """
        from msfabricpysdkcore.otheritems import Report
        if report_id is None and report_name is not None:
            reports = self.list_reports(workspace_id)
            reports = [rp for rp in reports if rp.display_name == report_name]
            if len(reports) == 0:
                raise Exception(f"Report with name {report_name} not found")
            report_id = reports[0].id
        if report_id is None:
            raise Exception("report_id or the report_name is required")        

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/reports/{report_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting report", return_format="json")
        
        report = Report.from_dict(item_dict, core_client=self)
        report.get_definition()
        return report


    def get_report_definition(self, workspace_id, report_id, format = None):
        """Get the definition of a report
        Args:
            workspace_id (str): The ID of the workspace
            report_id (str): The ID of the report
            format (str): The format of the definition
        Returns:
            dict: The definition of the report
        """
        return self.get_item_definition(workspace_id, report_id, type="reports", format=format)
    
    def list_reports(self, workspace_id, with_properties = False):
        """List reports in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of reports
        """
        return self.list_items(workspace_id = workspace_id, type = "reports", with_properties = with_properties)

    def update_report_definition(self, workspace_id, report_id, definition):
        """Update the definition of a report
        Args:
            workspace_id (str): The ID of the workspace
            report_id (str): The ID of the report
            definition (dict): The definition of the report
        Returns:
            Report: The updated report
        """
        return self.update_item_definition(workspace_id, report_id, definition, type="reports")

    # semanticModels

    def list_semantic_models(self, workspace_id, with_properties = False):
        """List semantic models in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of semantic models
        """
        return self.list_items(workspace_id = workspace_id, type = "semanticModels", with_properties = with_properties)
    
    def create_semantic_model(self, workspace_id, display_name, definition = None, description = None):
        """Create a semantic model in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the semantic model
            definition (dict): The definition of the semantic model
            description (str): The description of the semantic model
        Returns:
            dict: The created semantic model
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "semanticModels", definition = definition, description = description)
    
    def get_semantic_model(self, workspace_id, semantic_model_id = None, semantic_model_name = None):
        """Get a semantic model from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
            semantic_model_name (str): The name of the semantic model
        Returns:
            SemanticModel: The semantic model object
        """
        from msfabricpysdkcore.otheritems import SemanticModel
        if semantic_model_id is None and semantic_model_name is not None:
            semantic_models = self.list_semantic_models(workspace_id)
            semantic_models = [sm for sm in semantic_models if sm.display_name == semantic_model_name]
            if len(semantic_models) == 0:
                raise Exception(f"Semantic model with name {semantic_model_name} not found")
            semantic_model_id = semantic_models[0].id
        if semantic_model_id is None:
            raise Exception("semantic_model_id or the semantic_model_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/semanticModels/{semantic_model_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting semantic model", return_format="json")
        semmodel = SemanticModel.from_dict(item_dict, core_client=self)
        semmodel.get_definition()

        return semmodel
    
    def delete_semantic_model(self, workspace_id, semantic_model_id):
        """Delete a semantic model from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, semantic_model_id, type="semanticModels")
    
    # def update_semantic_model(self, workspace_id, semantic_model_id, display_name = None, description = None):
    #     """Update a semantic model in a workspace"""
    #     ws = self.get_workspace_by_id(workspace_id)
    #     return ws.update_semantic_model(semantic_model_id, display_name = display_name, description = description)
    
    def get_semantic_model_definition(self, workspace_id, semantic_model_id, format = None):
        """Get the definition of a semantic model
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
            format (str): The format of the definition
        Returns:
            dict: The definition of the semantic model
        """
        return self.get_item_definition(workspace_id, semantic_model_id, type="semanticModels", format=format)

    def update_semantic_model_definition(self, workspace_id, semantic_model_id, definition):
        """Update the definition of a semantic model
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
            definition (dict): The definition of the semantic model
        Returns:
            dict: The updated semantic model
        """
        return self.update_item_definition(workspace_id, semantic_model_id, definition, type="semanticModels", wait_for_completion=False)
    # spark workspace custom pools

    def create_workspace_custom_pool(self, workspace_id, name, node_family, node_size, auto_scale, dynamic_executor_allocation):
        """Create a workspace custom pool
        Args:
            workspace_id (str): The ID of the workspace
            name (str): The name of the pool
            node_family (str): The node family
            node_size (str): The node size
            auto_scale (bool): Whether to auto scale
            dynamic_executor_allocation (bool): Whether to use dynamic executor allocation
        Returns:
            SparkCustomPool: The created custom pool
        """
        from msfabricpysdkcore.spark_custom_pool import SparkCustomPool
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools"

        body = {
            "name": name,
            "nodeFamily": node_family,
            "nodeSize": node_size,
            "autoScale": auto_scale,
            "dynamicExecutorAllocation": dynamic_executor_allocation
        }
        response_dict = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 201, 429],
                                            error_message="Error creating workspace custom pool", return_format="json")

        response_dict["workspaceId"] = workspace_id
        return SparkCustomPool.from_dict(response_dict, core_client=self)

    def get_workspace_custom_pool(self, workspace_id, pool_id):
        """Get a workspace custom pool
        Args:
            workspace_id (str): The ID of the workspace
            pool_id (str): The ID of the pool
        Returns:
            SparkCustomPool: The custom pool
        """
        from msfabricpysdkcore.spark_custom_pool import SparkCustomPool

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools/{pool_id}"
        response_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting workspace custom pool", return_format="json")
        response_dict["workspaceId"] = workspace_id
        return SparkCustomPool.from_dict(response_dict, core_client=self)
    
    def delete_workspace_custom_pool(self, workspace_id, pool_id):
        """Delete a workspace custom pool
        Args:
            workspace_id (str): The ID of the workspace
            pool_id (str): The ID of the pool
        Returns:
            int: The status code of the response
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools/{pool_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429],
                                        error_message="Error deleting workspace custom pool", return_format="response")

        return response.status_code
    
    def list_workspace_custom_pools(self, workspace_id):
        """List workspace custom pools
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            list: The list of custom pools
        """
        from msfabricpysdkcore.spark_custom_pool import SparkCustomPool

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools"
        
        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing workspace custom pools", return_format="json", paging=True)
        for item in items:
            item["workspaceId"] = workspace_id
        sppools = [SparkCustomPool.from_dict(item, core_client=self) for item in items]

        return sppools
    
    def update_workspace_custom_pool(self, workspace_id, pool_id, name = None, node_family = None, node_size = None, auto_scale = None, dynamic_executor_allocation = None,
                                     return_item = "Default"):
        """Update a workspace custom pool
        Args:
            workspace_id (str): The ID of the workspace
            pool_id (str): The ID of the pool
            name (str): The name of the pool
            node_family (str): The node family
            node_size (str): The node size
            auto_scale (bool): Whether to auto scale
            dynamic_executor_allocation (bool): Whether to use dynamic executor allocation
        Returns:
            int: The status code of the response
        """
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools/{pool_id}"
        body = {}

        if name is not None:
            body['name'] = name
        if node_family is not None:
            body['nodeFamily'] = node_family
        if node_size is not None:
            body['nodeSize'] = node_size
        if auto_scale is not None:
            body['autoScale'] = auto_scale
        if dynamic_executor_allocation is not None:
            body['dynamicExecutorAllocation'] = dynamic_executor_allocation

        if not body:
            return None

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating workspace custom pool", return_format="json")

        if return_item == "Default":
            warn(
                message="Warning: Updating an item currently will make invoke an additional API call to get the item "
                        "object. This default behaviour will change in newer versions of the SDK. To keep this "
                        "behaviour, set return_item=True in the function call.",
                category=FutureWarning,
                stacklevel=2
            )
        if return_item:
            return self.get_workspace_custom_pool(workspace_id, pool_id)
        return response_json

    # Spark workspace settings

    def get_spark_settings(self, workspace_id):
        """Get spark settings for a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The spark settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/settings"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting spark settings", return_format="json")

        return response_json
    
    def update_spark_settings(self, workspace_id, automatic_log = None, 
                              environment = None, high_concurrency = None, pool = None):
        """Update spark settings for a workspace
        Args:
            workspace_id (str): The ID of the workspace
            automatic_log (bool): Whether to automatically log
            environment (str): The environment
            high_concurrency (bool): Whether to use high concurrency
            pool (str): The pool
        Returns:
            dict: The updated spark settings
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/settings"

        body = {}

        if automatic_log:
            body["automaticLog"] = automatic_log
        if environment:
            body["environment"] = environment
        if high_concurrency:
            body["highConcurrency"] = high_concurrency
        if pool:
            body["pool"] = pool

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                            error_message="Error updating spark settings", return_format="json")

        return response_json

    # sparkJobDefinitions

    def create_spark_job_definition(self, workspace_id, display_name, definition = None, description = None):
        """Create a spark job definition in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the spark job definition
            definition (dict): The definition of the spark job definition
            description (str): The description of the spark job definition
        Returns:
            dict: The created spark job definition
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "sparkJobDefinitions", definition = definition, description = description)
    
    def delete_spark_job_definition(self, workspace_id, spark_job_definition_id):
        """Delete a spark job definition from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, spark_job_definition_id, type="sparkJobDefinitions")

    def get_spark_job_definition(self, workspace_id, spark_job_definition_id = None, spark_job_definition_name = None):
        """Get a spark job definition from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
            spark_job_definition_name (str): The name of the spark job definition
        Returns:
            SparkJobDefinition: The spark job definition object
        """
        from msfabricpysdkcore.otheritems import SparkJobDefinition
        if spark_job_definition_id is None and spark_job_definition_name is not None:
            spark_job_definitions = self.list_spark_job_definitions(workspace_id)
            spark_job_definitions = [sjd for sjd in spark_job_definitions if sjd.display_name == spark_job_definition_name]
            if len(spark_job_definitions) == 0:
                raise Exception(f"Spark job definition with name {spark_job_definition_name} not found")
            spark_job_definition_id = spark_job_definitions[0].id
        elif spark_job_definition_id is None:
            raise Exception("spark_job_definition_id or the spark_job_definition_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkjobdefinitions/{spark_job_definition_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting spark job definition", return_format="json")

        sjd_obj =  SparkJobDefinition.from_dict(item_dict, core_client=self)
        sjd_obj.get_definition()
        return sjd_obj
    
    def list_spark_job_definitions(self, workspace_id, with_properties = False):
        """List spark job definitions in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of spark job definitions
        """
        return self.list_items(workspace_id = workspace_id, type = "sparkJobDefinitions", with_properties = with_properties)
    
    def update_spark_job_definition(self, workspace_id, spark_job_definition_id, display_name = None, description = None, return_item="Default"):
        """Update a spark job definition in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
            display_name (str): The display name of the spark job definition
            description (str): The description of the spark job definition
        Returns:
            dict: The updated spark job definition
        """
        return self.update_item(workspace_id, spark_job_definition_id, display_name = display_name, description = description,
                                type="sparkJobDefinitions", return_item=return_item)
    
    def get_spark_job_definition_definition(self, workspace_id, spark_job_definition_id, format = None):
        """Get the definition of a spark job definition
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
            format (str): The format of the definition
        Returns:
            dict: The definition of the spark job definition
        """
        return self.get_item_definition(workspace_id, spark_job_definition_id, type="sparkJobDefinitions", format=format)

    def update_spark_job_definition_definition(self, workspace_id, spark_job_definition_id, definition):
        """Update the definition of a spark job definition
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
            definition (dict): The definition of the spark job definition
        Returns:
            dict: The updated spark job definition
        """
        return self.update_item_definition(workspace_id, spark_job_definition_id, definition, type="sparkJobDefinitions")
    
    def run_on_demand_spark_job_definition(self, workspace_id, spark_job_definition_id, job_type = "sparkjob"):
        """Run an on demand spark job definition
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
            job_type (str): The job type
        Returns:
            dict: The job instance
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}/jobs/instances?jobType={job_type}"

        response = self.calling_routine(url, operation="POST", response_codes=[202, 429], wait_for_completion = False,
                                        error_message="Error running on demand spark job definition", return_format="response")

        location = response.headers['Location']
        job_instance_id = location.split('/')[-1]

        return self.get_item_job_instance(workspace_id = workspace_id,
                                          item_id = spark_job_definition_id,
                                          job_instance_id = job_instance_id)

    
    # warehouses

    def create_warehouse(self, workspace_id, display_name, description = None):
        """Create a warehouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the warehouse
            description (str): The description of the warehouse
        Returns:
            dict: The created warehouse
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "warehouses", description = description)
    
    def delete_warehouse(self, workspace_id, warehouse_id):
        """Delete a warehouse from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, warehouse_id, type="warehouses")
    
    def get_warehouse(self, workspace_id, warehouse_id = None, warehouse_name = None):
        """Get a warehouse from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            warehouse_name (str): The name of the warehouse
        Returns:
            Warehouse: The warehouse object
        """
        from msfabricpysdkcore.otheritems import Warehouse
        if warehouse_id is None and warehouse_name is not None:
            warehouses = self.list_warehouses(workspace_id)
            warehouses = [wh for wh in warehouses if wh.display_name == warehouse_name]
            if len(warehouses) == 0:
                raise Exception(f"Warehouse with name {warehouse_name} not found")
            warehouse_id = warehouses[0].id
        if warehouse_id is None:
            raise Exception("warehouse_id or the warehouse_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting warehouse", return_format="json")
        
        return Warehouse.from_dict(item_dict, core_client=self)
        
    def list_warehouses(self, workspace_id, with_properties = False):
        """List warehouses in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of warehouses
        """
        return self.list_items(workspace_id = workspace_id, type = "warehouses", with_properties = with_properties)

    def update_warehouse(self, workspace_id, warehouse_id, display_name = None, description = None, return_item="Default"):
        """Update a warehouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            display_name (str): The display name of the warehouse
            description (str): The description of the warehouse
        Returns:
            dict: The updated warehouse
        """
        return self.update_item(workspace_id, warehouse_id, display_name = display_name, description = description, 
                                type="warehouses", return_item=return_item)

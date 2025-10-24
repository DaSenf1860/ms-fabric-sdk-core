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
    
    # Connections

    # POST https://api.fabric.microsoft.com/v1/connections/{connectionId}/roleAssignments

    def add_connection_role_assignment(self, connection_id, principal, role):
        """Add a role assignment to a connection
        Args:
            connection_id (str): The ID of the connection
            principal (str): The principal
            role (str): The role
        Returns:
            dict: The role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}/roleAssignments"

        body = {
            'principal': principal,
            'role': role
        }

        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429],
                                             error_message="Error adding connection role assignment", return_format="json")
        return response_json

    def create_connection(self, connection_request):
        """Create a connection
        Args:
            connection_request (dict): The connection request
        Returns:
            dict: The connection
        """
        url = "https://api.fabric.microsoft.com/v1/connections"

        response_json = self.calling_routine(url, operation="POST", body=connection_request, response_codes=[201, 429],
                                             error_message="Error creating connection", return_format="json")
        return response_json 

    def delete_connection(self, connection_id):
        """Delete a connection
        Args:
            connection_id (str): The ID of the connection
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting connection")
        return response.status_code
    
    def delete_connection_role_assignment(self, connection_id, connection_role_assignment_id):
        """Delete a role assignment for a connection
        Args:
            connection_id (str): The ID of the connection
            connection_role_assignment_id (str): The ID of the role assignment
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}/roleAssignments/{connection_role_assignment_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting connection role assignment")
        return response.status_code
                          

    def get_connection(self, connection_id = None, connection_name = None):
        """Get a connection
        Args:
            connection_id (str): The ID of the connection
        Returns:
            dict: The connection
        """
        if connection_id is None and connection_name is not None:
            connections = self.list_connections()
            for connection in connections:
                if connection["displayName"] == connection_name:
                    connection_id = connection["id"]
                    break
        if connection_id is None:
            raise Exception("Please provide either connection_id or connection_name")
    
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}"
        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting connection", return_format="json")
        return response_json
    
    # GET https://api.fabric.microsoft.com/v1/connections/{connectionId}/roleAssignments/{connectionRoleAssignmentId}
    def get_connection_role_assignment(self, connection_id, connection_role_assignment_id):
        """Get a role assignment for a connection
        Args:
            connection_id (str): The ID of the connection
            connection_role_assignment_id (str): The ID of the role assignment
        Returns:
            dict: The role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}/roleAssignments/{connection_role_assignment_id}"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting connection role assignment", return_format="json")
        return response_json
    
    def list_connection_role_assignments(self, connection_id):
        """List role assignments for a connection
        Args:
            connection_id (str): The ID of the connection
        Returns:
            list: The list of role assignments
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}/roleAssignments"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing connection role assignments", return_format="value_json", paging=True)
        return items
    
    def list_connections(self):
        """Returns a list of on-premises, virtual network and cloud connections the user has permission for.
        Returns:
            list: The list of connections
        """
        # GET https://api.fabric.microsoft.com/v1/connections

        url = "https://api.fabric.microsoft.com/v1/connections"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing connections", return_format="value_json", paging=True)
        
        return items
    
    def list_supported_connection_types(self, gateway_id = None, show_all_creation_methods = None):
        """List supported connection types
        Args:
            gateway_id (str): The ID of the gateway
            show_all_creation_methods (bool): Whether to show all creation methods
        Returns:
            list: The list of supported connection types
        """
        url = "https://api.fabric.microsoft.com/v1/connections/supportedConnectionTypes"

        if gateway_id:
            url += f"?gatewayId={gateway_id}"
        if show_all_creation_methods:
            if "?" in url:
                url += "&"
            else:
                url += "?"
            url += "showAllCreationMethods=" + str(show_all_creation_methods)
        
        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing supported connection types", return_format="value_json", paging=True)
        
        return items
    
    def update_connection(self, connection_id, connection_request):
        """Update a connection
        Args:
            connection_id (str): The ID of the connection
            connection_request (dict): The connection request
        Returns:
            dict: The updated connection
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}"

        response_json = self.calling_routine(url, operation="PATCH", body=connection_request, response_codes=[200, 429],
                                             error_message="Error updating connection", return_format="json")
        return response_json
    
    # PATCH https://api.fabric.microsoft.com/v1/connections/{connectionId}/roleAssignments/{connectionRoleAssignmentId}

    def update_connection_role_assignment(self, connection_id, connection_role_assignment_id, role):
        """Update a role assignment for a connection
        Args:
            connection_id (str): The ID of the connection
            connection_role_assignment_id (str): The ID of the role assignment
            role (str): The role
        Returns:
            dict: The role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/connections/{connection_id}/roleAssignments/{connection_role_assignment_id}"

        body = {
            'role': role
        }

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating connection role assignment", return_format="json")
        return response_json
        
    # Deployment Pipelines

    # POST https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/roleAssignments
    def add_deployment_pipeline_role_assignment(self, deployment_pipeline_id, principal, role):
        """Add a role assignment to a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            principal (str): The principal
            role (str): The role
        Returns:
            dict: The role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/roleAssignments"

        body = {
            'principal': principal,
            'role': role
        }

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                             error_message="Error adding deployment pipeline role assignment", return_format="response")
        return response.status_code
    
    # POST https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/stages/{stageId}/assignWorkspace
    def assign_workspace_to_stage(self, deployment_pipeline_id, stage_id, workspace_id):
        """Assign a workspace to a stage
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            stage_id (str): The ID of the stage
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The workspace assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages/{stage_id}/assignWorkspace"

        body = {
            'workspaceId': workspace_id
        }

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                             error_message="Error assigning workspace to stage", return_format="response")
        return response.status_code
    
    # POST https://api.fabric.microsoft.com/v1/deploymentPipelines
    def create_deployment_pipeline(self, display_name, stages, description = None):
        """Create a deployment pipeline
        Args:
            display_name (str): The display name of the deployment pipeline
            stages (list): The stages of the deployment pipeline
            description (str): The description of the deployment pipeline
        Returns:
            dict: The deployment pipeline
        """
        url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"

        body = {
            'displayName': display_name,
            'stages': stages
        }
        if description:
            body['description'] = description

        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429],
                                             error_message="Error creating deployment pipeline", return_format="json")
        
        from msfabricpysdkcore.deployment_pipeline import DeploymentPipeline
        deployment_pipeline = DeploymentPipeline.from_dict(response_json, self)
        return deployment_pipeline

    # DELETE https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}
    def delete_deployment_pipeline(self, deployment_pipeline_id):
        """Delete a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting deployment pipeline")
        return response.status_code

    # DELETE https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/roleAssignments/{principalId}
    def delete_deployment_pipeline_role_assignment(self, deployment_pipeline_id, principal_id):
        """Delete a role assignment for a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            principal_id (str): The ID of the principal
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/roleAssignments/{principal_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting deployment pipeline role assignment")
        return response.status_code

    def deploy_stage_content(self, deployment_pipeline_id, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, options = None, wait_for_completion = True):
        """Deploy stage content
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            source_stage_id (str): The ID of the source stage
            target_stage_id (str): The ID of the target stage
            created_workspace_details (list): A list of created workspace details
            items (list): A list of items
            note (str): A note
            options (dict): A dictionary of options
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
        if options:
            body["options"] = options
            
        json_operation_result = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 202, 429], error_message="Error deploying stage content", 
                                                     return_format="json+operation_result", wait_for_completion=wait_for_completion)

        return json_operation_result
    
    def get_deployment_pipeline(self, deployment_pipeline_id = None, deployment_pipeline_name = None, with_details = False):
        """Get a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
        Returns:
            DeploymentPipeline: The deployment pipeline
        """
        if deployment_pipeline_id is None and deployment_pipeline_name is not None:
            deployment_pipelines = self.list_deployment_pipelines()
            for deployment_pipeline in deployment_pipelines:
                if deployment_pipeline["displayName"] == deployment_pipeline_name:
                    deployment_pipeline_id = deployment_pipeline["id"]
                    break

            if deployment_pipeline_id is None:
                raise Exception("No deployment_pipeline_id given and deployment_pipeline_name is not found")
            

        from msfabricpysdkcore.deployment_pipeline import DeploymentPipeline
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}"

        result_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting deployment pipeline", return_format="json")

        deply = DeploymentPipeline.from_dict(result_json, self)
        
        if with_details:
            stages_ = []
            from msfabricpysdkcore.deployment_pipeline import DeploymentPipelineStage
            for stage in deply.stages:
                stage_items = self.list_deployment_pipeline_stage_items(deployment_pipeline_id, stage["id"])
                stage["items"] = stage_items
                stage["deploymentPipelineId"] = deployment_pipeline_id
                depl_pipe_stage = DeploymentPipelineStage.from_dict(stage, self)
                stages_.append(depl_pipe_stage)
            deply.stages = stages_
    
        return deply

    # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/operations/{operationId}
    def get_deployment_pipeline_operation(self, deployment_pipeline_id, operation_id):
        """Get a deployment pipeline operation
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            operation_id (str): The ID of the operation
        Returns:
            dict: The deployment pipeline operation
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/operations/{operation_id}"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting deployment pipeline operation", return_format="json")
        return response_json
    
    # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/stages/{stageId}
    def get_deployment_pipeline_stage(self, deployment_pipeline_id, stage_id, with_details = False):
        """Get a deployment pipeline stage
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            stage_id (str): The ID of the stage
        Returns:
            dict: The deployment pipeline stage
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages/{stage_id}"

        stage = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting deployment pipeline stage", return_format="json")
        
        if not with_details:
            stage["items"] = []
        else:
            stage_items = self.list_deployment_pipeline_stage_items(deployment_pipeline_id, stage["id"])
            stage["items"] = stage_items
        
        stage["deploymentPipelineId"] = deployment_pipeline_id
        from msfabricpysdkcore.deployment_pipeline import DeploymentPipelineStage

        depl_pipe_stage = DeploymentPipelineStage.from_dict(stage, self)
        return depl_pipe_stage


    # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/operations
    def list_deployment_pipeline_operations(self, deployment_pipeline_id):
        """List deployment pipeline operations
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: The list of deployment pipeline operations
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/operations"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing deployment pipeline operations", return_format="value_json", paging=True)
        
        return items
    
    # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/roleAssignments
    def list_deployment_pipeline_role_assignments(self, deployment_pipeline_id):
        """List role assignments for a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: The list of role assignments
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/roleAssignments"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing deployment pipeline role assignments", return_format="value_json", paging=True)
        
        return items
    


    def list_deployment_pipeline_stage_items(self, deployment_pipeline_id, stage_id = None, stage_name = None):
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
    
    def list_deployment_pipeline_stages(self, deployment_pipeline_id, with_details = False):
        """Get the stages of a deployment pipeline
        Args:
            pipeline_id (str): The ID of the deployment pipeline
        Returns:
            list: List of DeploymentPipelineStage objects
        """
        from msfabricpysdkcore.deployment_pipeline import DeploymentPipelineStage

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                      error_message="Error getting deployment pipeline stages", return_format="value_json", paging=True)

        for item in items:
            item["deploymentPipelineId"] = deployment_pipeline_id
            item["items"] = []
            if with_details:
                items = self.list_deployment_pipeline_stage_items(deployment_pipeline_id, item["id"])
                item["items"] = items
                
        stages = [DeploymentPipelineStage.from_dict(item, self) for item in items]
        
        
        return stages

    def list_deployment_pipelines(self, with_details = False):
        """List deployment pipelines
        Returns:
            list: List of DeploymentPipeline objects
        """

        url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing deployment pipelines", return_format="value_json", paging=True)

        if with_details:
            items = [self.get_deployment_pipeline(i["id"], with_details) for i in items]

        return items

    # POST https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/stages/{stageId}/unassignWorkspace
    def unassign_workspace_from_stage(self, deployment_pipeline_id, stage_id):
        """Unassign a workspace from a stage
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            stage_id (str): The ID of the stage
        Returns:
            dict: The workspace unassignment
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages/{stage_id}/unassignWorkspace"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 429],
                                             error_message="Error unassigning workspace from stage", return_format="response")
        return response.status_code

    # PATCH https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}
    def update_deployment_pipeline(self, deployment_pipeline_id, display_name = None, description = None):
        """Update a deployment pipeline
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            display_name (str): The display name of the deployment pipeline
            description (str): The description of the deployment pipeline
        Returns:
            dict: The updated deployment pipeline
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}"
        body = {}
        if display_name:
            body['displayName'] = display_name
        if description:
            body['description'] = description

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating deployment pipeline", return_format="json")
        
        from msfabricpysdkcore.deployment_pipeline import DeploymentPipeline
        deployment_pipeline = DeploymentPipeline.from_dict(response_json, self)
        return deployment_pipeline
    
    # PATCH https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/stages/{stageId}
    def update_deployment_pipeline_stage(self, deployment_pipeline_id, stage_id, display_name, description = None, is_public = None):
        """Update a deployment pipeline stage
        Args:
            deployment_pipeline_id (str): The ID of the deployment pipeline
            stage_id (str): The ID of the stage
            display_name (str): The display name of the stage
            description (str): The description of the stage
        Returns:
            dict: The updated deployment pipeline stage
        """
        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}/stages/{stage_id}"

        body = {}
        body['displayName'] = display_name
        if description:
            body['description'] = description
        if is_public is not None:
            body['isPublic'] = is_public

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating deployment pipeline stage", return_format="json")
        
        return response_json

    # External Data Shares Provider

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
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/externalDataShares/{externalDataShareId}
    def delete_external_data_share(self, workspace_id, item_id, external_data_share_id):
        """Delete an external data share in an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            external_data_share_id (str): The ID of the external data share
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/externalDataShares/{external_data_share_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting external data share")
        return response.status_code
    
    # External Data Shares Recipient

    # POST https://api.fabric.microsoft.com/v1/externalDataShares/invitations/{invitationId}/accept
    def accept_external_data_share_invitation(self, invitation_id, item_id, payload, provider_tenant_id, workspace_id):
        """Accept an external data share invitation
        Args:
            invitation_id (str): The ID of the invitation
            item_id (str): The ID of the item
            payload (dict): The payload of the invitation
            provider_tenant_id (str): The ID of the provider tenant
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The external data share invitation
        """
        url = f"https://api.fabric.microsoft.com/v1/externalDataShares/invitations/{invitation_id}/accept"

        body = {
            'itemId': item_id,
            'payload': payload,
            'providerTenantId': provider_tenant_id,
            'workspaceId': workspace_id
        }
        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                             error_message="Error accepting external data share invitation", return_format="value_json")
        return response_json
    
    # GET https://api.fabric.microsoft.com/v1/externalDataShares/invitations/{invitationId}?providerTenantId={providerTenantId}
    def get_external_data_share_invitation(self, invitation_id, provider_tenant_id):
        """Get an external data share invitation
        Args:
            invitation_id (str): The ID of the invitation
            provider_tenant_id (str): The ID of the provider tenant
        Returns:
            dict: The external data share invitation
        """
        url = f"https://api.fabric.microsoft.com/v1/externalDataShares/invitations/{invitation_id}?providerTenantId={provider_tenant_id}"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting external data share invitation", return_format="json")
        return response_json
    
    # Folders
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/folders
    def create_folder(self, workspace_id, display_name, parent_folder_id = None):
        """Create a folder
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the folder
            parent_folder_id (str): The ID of the parent folder
        Returns:
            dict: The folder
        """
        from msfabricpysdkcore.folder import Folder
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders"

        body = {
            'displayName': display_name
        }
        if parent_folder_id:
            body['parentFolderId'] = parent_folder_id

        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429],
                                             error_message="Error creating folder", return_format="json")
        
        folder = Folder.from_dict(response_json, self)
        return folder
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/folders/{folderId}
    def delete_folder(self, workspace_id, folder_id):
        """Delete a folder
        Args:
            workspace_id (str): The ID of the workspace
            folder_id (str): The ID of the folder
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting folder")
        return response.status_code
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/folders/{folderId}
    def get_folder(self, workspace_id, folder_id):
        """Get a folder
        Args:
            workspace_id (str): The ID of the workspace
            folder_id (str): The ID of the folder
        Returns:
            dict: The folder
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting folder", return_format="json")
        
        from msfabricpysdkcore.folder import Folder

        folder = Folder.from_dict(response_json, self)
        return folder
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/folders
    def list_folders(self, workspace_id):
        """List folders
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            list: The list of folders
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing folders", return_format="value_json", paging=True)
        
        from msfabricpysdkcore.folder import Folder

        folders = [Folder.from_dict(item, self) for item in items]
        return folders

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/folders/{folderId}/move
    def move_folder(self, workspace_id, folder_id, target_folder_id = None):
        """Move a folder
        Args:
            workspace_id (str): The ID of the workspace
            folder_id (str): The ID of the folder
            parent_folder_id (str): The ID of the parent folder
        Returns:
            dict: The moved folder
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}/move"

        body = {
        }
        if target_folder_id:
            body['targetFolderId'] = target_folder_id

        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                             error_message="Error moving folder", return_format="json")
        
        from msfabricpysdkcore.folder import Folder

        folder = Folder.from_dict(response_json, self)
        return folder
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/folders/{folderId}
    def update_folder(self, workspace_id, folder_id, display_name = None):
        """Update a folder
        Args:
            workspace_id (str): The ID of the workspace
            folder_id (str): The ID of the folder
            display_name (str): The display name of the folder
        Returns:
            dict: The updated folder
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}"

        body = {'displayName' : display_name}


        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating folder", return_format="json")
        from msfabricpysdkcore.folder import Folder

        folder = Folder.from_dict(response_json, self)
        return folder

    # Gateways

    def add_gateway_role_assignment(self, gateway_id, principal, role):
        """Add a role assignment to a gateway
        Args:
            gateway_id (str): The ID of the gateway
            principal (str): The principal
            role (str): The role
        Returns:
            dict: The role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/roleAssignments"

        body = {
            'principal': principal,
            'role': role
        }

        response_json = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429],
                                             error_message="Error adding gateway role assignment", return_format="json")
        return response_json

    def create_gateway(self, gateway_request):
        """Create a gateway
        Args:
            gateway_request (dict): The gateway request
        Returns:
            dict: The gateway
        """
        url = "https://api.fabric.microsoft.com/v1/gateways"

        response_json = self.calling_routine(url, operation="POST", body=gateway_request, response_codes=[200, 201, 429],
                                             error_message="Error creating gateway", return_format="json")
        return response_json
    
    def delete_gateway(self, gateway_id):
        """Delete a gateway
        Args:
            gateway_id (str): The ID of the gateway
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting gateway")
        return response.status_code
    
    def delete_gateway_member(self, gateway_id, gateway_member_id):
        """Delete a gateway member
        Args:
            gateway_id (str): The ID of the gateway
            gateway_member_id (str): The ID of the gateway member
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/members/{gateway_member_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting gateway member")
        return response.status_code

    def delete_gateway_role_assignment(self, gateway_id, gateway_role_assignment_id):
        """Delete a gateway role assignment
        Args:
            gateway_id (str): The ID of the gateway
            gateway_role_assignment_id (str): The ID of the gateway role assignment
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/roleAssignments/{gateway_role_assignment_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                        error_message="Error deleting gateway role assignment")
        return response.status_code
    
    def get_gateway(self, gateway_id = None, gateway_name = None):
        """Get a gateway
        Args:
            gateway_id (str): The ID of the gateway
            gateway_name (str): The name of the gateway
        Returns:
            dict: The gateway
        """
        if gateway_id is None and gateway_name is not None:
            gateways = self.list_gateways()
            for gateway in gateways:
                if gateway["displayName"] == gateway_name:
                    gateway_id = gateway["id"]
                    break
        if gateway_id is None:
            raise Exception("Please provide either gateway_id or gateway_name")
    
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}"
        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting gateway", return_format="json")
        return response_json

    def get_gateway_role_assignment(self, gateway_id, gateway_role_assignment_id):
        """Get a gateway role assignment
        Args:
            gateway_id (str): The
            gateway_role_assignment_id (str): The ID of the gateway role assignment
        Returns:
            dict: The gateway role assignment
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/roleAssignments/{gateway_role_assignment_id}"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting gateway role assignment", return_format="json")
        return response_json
    
    def list_gateway_members(self, gateway_id):
        """List gateway members
        Args:
            gateway_id (str): The ID of the gateway
        Returns:
            list: The list of gateway members
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/members"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing gateway members", return_format="value_json", paging=True)
        return items
    
    def list_gateway_role_assignments(self, gateway_id):
        """List gateway role assignments
        Args:
            gateway_id (str): The ID of the gateway
        Returns:
            list: The list of gateway role assignments
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/roleAssignments"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing gateway role assignments", return_format="value_json", paging=True)
        return items
    
    def list_gateways(self):
        """List gateways
        Returns:
            list: The list of gateways
        """
        url = "https://api.fabric.microsoft.com/v1/gateways"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing gateways", return_format="value_json", paging=True)
        return items
    
    def update_gateway(self, gateway_id, gateway_request):
        """Update a gateway
        Args:
            gateway_id (str): The ID of the gateway
            gateway_request (dict): The gateway request
        Returns:
            dict: The updated gateway
        """

        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}"

        response_json = self.calling_routine(url, operation="PATCH", body=gateway_request, response_codes=[200, 429],
                                             error_message="Error updating gateway", return_format="json")
        return response_json
    
    def update_gateway_member(self, gateway_id, gateway_member_id, display_name, enabled):
        """Update a gateway member
        Args:
            gateway_id (str): The ID of the gateway
            gateway_member_id (str): The ID of the gateway member
            display_name (str): The display name of the gateway member
            enabled (bool): Whether the gateway member is enabled
        Returns:
            dict: The updated gateway member
        """
        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/members/{gateway_member_id}"

        body = {
            'displayName': display_name,
            'enabled': enabled
        }

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating gateway member", return_format="json")
        return response_json

    def update_gateway_role_assignment(self, gateway_id, gateway_role_assignment_id, role):
        """Update a gateway role assignment
        Args:
            gateway_id (str): The ID of the gateway
            gateway_role_assignment_id (str): The ID of the gateway role assignment
            role (str): The role
        Returns:
            dict: The updated gateway role assignment
        """

        url = f"https://api.fabric.microsoft.com/v1/gateways/{gateway_id}/roleAssignments/{gateway_role_assignment_id}"

        body = {
            'role': role
        }

        response_json = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                             error_message="Error updating gateway role assignment", return_format="json")
        return response_json

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


    def git_connect(self, workspace_id, git_provider_details, my_git_credentials = None):
        """Connect git
        Args:
            workspace_id (str): The ID of the workspace
            git_provider_details (dict): The git provider details
            my_git_credentials (dict): The git credentials
        Returns:
            int: The status code of the response
        """
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/connect
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/connect"

        payload = {
            'gitProviderDetails': git_provider_details,
            
        }
        if my_git_credentials:
            payload['myGitCredentials'] = my_git_credentials

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
    
    def get_my_git_credentials(self, workspace_id):
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/myGitCredentials
        """Get my git credentials
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The git credentials
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/myGitCredentials"

        response_json = self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting git credentials", return_format="json")

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

        body = {'initializationStrategy':initialization_strategy}
        
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

    def update_my_git_credentials(self, workspace_id, source, connection_id = None):
        #PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/git/myGitCredentials
        """Update my git credentials
        Args:
            source (str): The git provider source
            connection_id (str): The connection ID
        Returns:
            dict: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/myGitCredentials"

        body = {"source": source}

        if connection_id:
            body['connectionId'] = connection_id

        response = self.calling_routine(url=url, operation="PATCH", body=body,
                                        response_codes=[200, 429],
                                        error_message="Error updating git credentials", return_format="json") 
        
        return response

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

        if item_dict["type"] == "AnomalyDetector":
            return self.get_anomaly_detector(workspace_id, item_dict["id"])
        if item_dict["type"] == "ApacheAirflowJob":
            return self.get_apache_airflow_job(workspace_id, item_dict["id"])
        if item_dict["type"] == "CopyJob":
            return self.get_copy_job(workspace_id, item_dict["id"])
        if item_dict["type"] == "VariableLibrary":
            return self.get_variable_library(workspace_id, item_dict["id"])
        if item_dict["type"] == "Dataflow":
            return self.get_dataflow(workspace_id, item_dict["id"])
        if item_dict["type"] == "DataPipeline":
            return self.get_data_pipeline(workspace_id, item_dict["id"])
        if item_dict["type"] == "DigitalTwinBuilder":
            return self.get_digital_twin_builder(workspace_id, item_dict["id"])
        if item_dict["type"] == "DigitalTwinBuilderFlow":
            return self.get_digital_twin_builder_flow(workspace_id, item_dict["id"])
        if item_dict["type"] == "Eventstream":
            return self.get_eventstream(workspace_id, item_dict["id"])
        if item_dict["type"] == "Eventhouse":
            return self.get_eventhouse(workspace_id, item_dict["id"])
        if item_dict["type"] == "KQLDashboard":
            return self.get_kql_dashboard(workspace_id, item_dict["id"])
        if item_dict["type"] == "KQLDatabase":
            return self.get_kql_database(workspace_id, item_dict["id"])
        if item_dict["type"] == "KQLQueryset":
            return self.get_kql_queryset(workspace_id, item_dict["id"])
        if item_dict["type"] == "Lakehouse":
            return self.get_lakehouse(workspace_id, item_dict["id"])
        if item_dict["type"] == "Map":
            return self.get_map(workspace_id, item_dict["id"])
        if item_dict["type"] == "MirroredAzureDatabricksCatalog":
            return self.get_mirrored_azure_databricks_catalog(workspace_id, item_dict["id"])
        if item_dict["type"] == "MirroredDatabase":
            return self.get_mirrored_database(workspace_id, item_dict["id"])
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
        if item_dict["type"] == "UserDataFunction":
            return self.get_user_data_function(workspace_id, item_dict["id"])
        if item_dict["type"] == "Warehouse":
            return self.get_warehouse(workspace_id, item_dict["id"])
        if item_dict["type"] == "WarehouseSnapshot":
            return self.get_warehouse_snapshot(workspace_id, item_dict["id"])
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
  
    def create_item(self, workspace_id, display_name, type, definition = None, description = None, wait_for_completion = True, creation_payload = None, folder_id = None, **kwargs):
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
                    
        if creation_payload:
            body["creationPayload"] = creation_payload

        if folder_id:
            body['folderId'] = folder_id

        if type in ["anomalydetectors",
                    "ApacheAirflowJobs",
                    "copyJobs",
                    "VariableLibraries",
                    "dataflows",
                    "dataPipelines",
                    "digitaltwinbuilders",
                    "DigitalTwinBuilderFlows",
                    "environments",
                    "eventhouses",
                    "eventstreams",
                    "GraphQLApis",
                    "kqlDatabases",
                    "kqlDashboards",
                    "kqlQuerysets",
                    "lakehouses",
                    "Maps",
                    "mirroredAzureDatabricksCatalogs",
                    "mirroredDatabases",
                    "mlExperiments", 
                    "mlModels",
                    "mountedDataFactories", 
                    "notebooks",
                    "reflexes", 
                    "reports", 
                    "semanticModels", 
                    "sparkJobDefinitions",
                    "SQLDatabases",
                    "UserDataFunctions",
                    "warehouses",
                    "warehousesnapshots"]:
                        

            if type == "kqlDatabases":
                if creation_payload is None:
                    raise Exception("creation_payload is required for KQLDatabase")
                body["creationPayload"] = creation_payload
            
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

            type_mapping = {"anomalydetectors": "AnomalyDetector",
                            "ApacheAirflowJobs": "ApacheAirflowJob",
                            "copyJobs": "CopyJob",
                            "VariableLibraries": "VariableLibrary",
                            "dataflows": "Dataflow",
                            "digitaltwinbuilders": "DigitalTwinBuilder",
                            "DigitalTwinBuilderFlows":"DigitalTwinBuilderFlow",
                            "dataPipelines": "DataPipeline",
                            "environments": "Environment",
                            "eventhouses": "Eventhouse",
                            "eventstreams": "Eventstream",
                            "GraphQLApis": "GraphQLApi",
                            "kqlDashboards": "KQLDashboard",
                            "kqlDatabases": "KQLDatabase",
                            "kqlQuerysets": "KQLQueryset",
                            "lakehouses": "Lakehouse",
                            "Maps": "Map",
                            "mirroredAzureDatabricksCatalogs": "MirroredAzureDatabricksCatalog",
                            "mirroredDatabases": "MirroredDatabase",
                            "mlExperiments": "MLExperiment",
                            "mlModels": "MLModel", 
                            "mountedDataFactories": "MountedDataFactory",
                            "notebooks": "Notebook",
                            "reflexes": "Reflex",
                            "reports": "Report", 
                            "semanticModels": "SemanticModel",
                            "sparkJobDefinitions": "SparkJobDefinition",
                            "SQLDatabases": "SQLDatabase",
                            "UserDataFunctions": "UserDataFunction",
                            "warehouses": "Warehouse",
                            "warehousesnapshots": "WarehouseSnapshot"
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

    def list_item_connections(self, workspace_id, item_id):
        """List item connections
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
        Returns:
            dict: The item connections
        """
        #GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/connections
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/connections"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error listing item connections", return_format="value_json", paging=True)

        return response_json
 
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
    
    
    def update_item(self, workspace_id, item_id, display_name = None, description = None, type = None, return_item=False, **kwargs):
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
        if "properties" in kwargs:
            payload['properties'] = kwargs["properties"]

        resp_dict = self.calling_routine(url, operation="PATCH", body=payload,
                                         response_codes=[200, 429], error_message="Error updating item",
                                         return_format="json")

        if return_item:
            return self.get_item_specific(workspace_id, resp_dict)
        return resp_dict

    def update_item_definition(self, workspace_id, item_id, definition, type = None, wait_for_completion=True, **kwargs):
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
       
        if "update_metadata" in kwargs and kwargs["update_metadata"]:
            url = f"{url}?updateMetadata={kwargs['update_metadata']}"
 
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
    
    def create_item_schedule(self, workspace_id, item_id, job_type, configuration, enabled):
        """Create a job schedule for the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_type (str): The type of the job
        Returns:
            dict: The job schedule
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/{job_type}/schedules"

        payload = {"configuration": configuration,
                   "enabled": enabled}

        return self.calling_routine(url=url, operation="POST", body=payload, response_codes=[201, 429],
                                    error_message="Error creating job schedule", return_format="json")
    
    def get_item_schedule(self, workspace_id, item_id, job_type, schedule_id):
        """Get the job schedule of the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_type (str): The type of the job
            schedule_id (str): The ID of the schedule
        Returns:
            dict: The job schedule
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/{job_type}/schedules/{schedule_id}"

        return self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                    error_message="Error getting job schedule", return_format="json")
    
    def list_item_job_instances(self, workspace_id, item_id):
        """List the job instances of the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_type (str): The type of the job
        Returns:
            list: The list of job instances
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/instances"

        return self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                    error_message="Error listing job instances", return_format="value_json", paging=True)
    
    def list_item_schedules(self, workspace_id, item_id, job_type):
        """List the job schedules of the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_type (str): The type of the job
        Returns:
            list: The list of job schedules
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/{job_type}/schedules"

        return self.calling_routine(url=url, operation="GET", response_codes=[200, 429],
                                    error_message="Error listing job schedules", return_format="value_json", paging=True)   

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
    
    def update_item_schedule(self, workspace_id, item_id, job_type, schedule_id, configuration, enabled):
        """Update the job schedule of the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            job_type (str): The type of the job
            schedule_id (str): The ID of the schedule
            configuration (dict): The configuration of the schedule
        Returns:
            dict: The updated job schedule
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/{job_type}/schedules/{schedule_id}"

        payload = {"configuration": configuration,
                     "enabled": enabled}

        return self.calling_routine(url=url, operation="PATCH", body=payload, response_codes=[200, 429],
                                    error_message="Error updating job schedule", return_format="json")
    
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

    # Managed Private Endpoints:

    def create_workspace_managed_private_endpoint(self, workspace_id, name, target_private_link_resource_id,
                                                  target_subresource_type, request_message = None):
        
        """Create a managed private endpoint in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            name (str): The name of the managed private endpoint
            target_private_link_resource_id (str): The target private link resource ID
            target_subresource_type (str): The target subresource type
            request_message (str): The request message
        Returns:
            dict: The created managed private endpoint
        """

        body = {
            "name": name,
            "targetPrivateLinkResourceId": target_private_link_resource_id,
            "targetSubresourceType": target_subresource_type
        }
        if request_message:
            body["requestMessage"] = request_message
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/managedPrivateEndpoints"

        response = self.calling_routine(url, operation="POST", body=body,
                                             response_codes=[201, 429], error_message="Error creating managed private endpoint",
                                             return_format="json")

        return response
    
    def delete_workspace_managed_private_endpoint(self, workspace_id, managed_private_endpoint_id):
        """Delete a managed private endpoint in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            managed_private_endpoint_id (str): The ID of the managed private endpoint
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/managedPrivateEndpoints/{managed_private_endpoint_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], return_format="response",
                                             error_message="Error deleting managed private endpoint")

        return response.status_code
    
    def get_workspace_managed_private_endpoint(self, workspace_id, managed_private_endpoint_id):
        """Get a managed private endpoint in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            managed_private_endpoint_id (str): The ID of the managed private endpoint
        Returns:
            dict: The managed private endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/managedPrivateEndpoints/{managed_private_endpoint_id}"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting managed private endpoint", return_format="json")

        return response_json
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/managedPrivateEndpoints/{managedPrivateEndpointId}/targetFQDNs
    def list_managed_private_endpoint_fqdns(self, workspace_id, managed_private_endpoint_id):
        """List FQDNs of a managed private endpoint in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            managed_private_endpoint_id (str): The ID of the managed private endpoint
        Returns:
            list: The list of FQDNs
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/managedPrivateEndpoints/{managed_private_endpoint_id}/targetFQDNs"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error listing FQDNs", return_format="value_json", paging=True)

        return response_json

    def list_workspace_managed_private_endpoints(self, workspace_id):
        """List managed private endpoints in a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            list: The list of managed private endpoints
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/managedPrivateEndpoints"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], paging=True,
                                             error_message="Error listing managed private endpoints", return_format="json")

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
    
    # one lake diagnostics

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/onelake/settings
    def get_onelake_settings(self, workspace_id):
        """Get OneLake settings for a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The OneLake settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/onelake/settings"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting OneLake settings", return_format="json")

        return response_json
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/onelake/settings/modifyDiagnostics
    def modify_onelake_settings(self, workspace_id, status, destination=None, wait_for_completion=False):
        """Modify OneLake settings for a workspace
        Args:
            workspace_id (str): The ID of the workspace
            status (str): The status of the diagnostics ("Enabled" or "Disabled")
            destination (str): The destination of the diagnostics
        Returns:
            Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/onelake/settings/modifyDiagnostics"

        body = {
            "status": status
        }
        if destination:
            body["destination"] = destination

        response = self.calling_routine(url, operation="POST", body=body,
                                             response_codes=[200, 202, 429], error_message="Error modifying OneLake settings",
                                             return_format="response+operation_result",
                                                wait_for_completion=wait_for_completion)
        return response

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
     

    def create_shortcuts_bulk(self, workspace_id, item_id, create_shortcut_requests):
        """
        Bulk create OneLake shortcuts.

        Args:
            workspace_id (str)
            item_id (str)
            create_shortcut_requests (list[dict]): Each dict must have:
                path, name, target (target has 'oneLake' OR 'adlsGen2' child object)

        Returns:
            dict: The results of the operation
        """
        if not isinstance(create_shortcut_requests, list) or len(create_shortcut_requests) == 0:
            raise Exception("create_shortcut_requests must be a non-empty list.")

        required_keys = {"path", "name", "target"}
        for idx, req in enumerate(create_shortcut_requests):
            if not isinstance(req, dict):
                raise Exception(f"Shortcut request at index {idx} is not a dict.")
            missing = required_keys - set(req.keys())
            if missing:
                raise Exception(f"Shortcut request at index {idx} missing keys: {missing}")

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/shortcuts/bulkCreate"
        body = {
            "createShortcutRequests": create_shortcut_requests
        }

        return self.calling_routine(
            url=url,
            operation="POST",
            body=body,
            response_codes=[200, 202, 429],
            error_message="Error creating shortcuts in bulk",
            return_format="value_json+operation_result",
            wait_for_completion=True
        )   

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
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/shortcuts

    def list_shortcuts(self, workspace_id, item_id, parent_path = None):
        """List the shortcuts in the item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            parent_path (str): The starting path from which to retrieve the shortcuts
        Returns:
            list: The list of shortcuts
        """
        from msfabricpysdkcore.onelakeshortcut import OneLakeShortcut

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/shortcuts"
        if parent_path:
            url += f"?parentPath={parent_path}"

        shortcuts = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error listing shortcuts", return_format="value_json", paging=True)

        for shortcut in shortcuts:
            shortcut['workspaceId'] = workspace_id
            shortcut['itemId'] = item_id
        return [OneLakeShortcut.from_dict(shortcut, core_client=self) for shortcut in shortcuts]
    

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/onelake/resetShortcutCache
    def reset_shortcut_cache(self, workspace_id, wait_for_completion = False):
        """Reset the shortcut cache

        Args:
            workspace_id (str): The ID of the workspace

        Returns:
            int: The status code of the response
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/onelake/resetShortcutCache"
        response = self.calling_routine(url=url, operation="POST", response_codes=[200, 202, 429], error_message="Error resetting shortcut cache",
                                        return_format="response", wait_for_completion = wait_for_completion)

        return response.status_code

    ### Tags
    # GET https://api.fabric.microsoft.com/v1/tags
    def list_tags(self):
        """List all tags
        Returns:
            list: The list of tags
        """
        url = "https://api.fabric.microsoft.com/v1/tags"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error listing tags", return_format="value_json", paging=True)

        return response_json
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/applyTags
    def apply_tags(self, workspace_id, item_id, tags):
        """Apply tags to an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            tags (list): The list of tags to apply
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/applyTags"

        payload = {
            'tags': tags
        }

        response = self.calling_routine(url, operation="POST", body=payload,
                                        response_codes=[200, 429], error_message="Error applying tags", return_format="response")

        return response.status_code
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/unapplyTags
    def unapply_tags(self, workspace_id, item_id, tags):
        """Unapply tags from an item
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            tags (list): The list of tags to unapply
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/unapplyTags"

        payload = {
            'tags': tags
        }

        response = self.calling_routine(url, operation="POST", body=payload,
                                        response_codes=[200, 429], error_message="Error unapplying tags", return_format="response")

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
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/networking/communicationPolicy
    def get_network_communication_policy(self, workspace_id):
        """Get the network communication policy for a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The network communication policy
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/networking/communicationPolicy"

        response_json = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                             error_message="Error getting network communication policy", return_format="json")

        return response_json

    def get_workspace(self, id = None, name = None, return_item=True):
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
            return self.get_workspace_by_id(id, return_item=return_item)
        if name:
            return self.get_workspace_by_name(name)
        raise ValueError("Either id or name must be provided")
    
    def get_workspace_by_id(self, id, return_item=True):
        """Get workspace by id
        Args:
            id (str): The ID of the workspace
        Returns:
            Workspace: The workspace object
        """
        from msfabricpysdkcore.workspace import Workspace

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{id}"

        ws_dict = self.calling_routine(url, operation="GET", response_codes=[200, 404], error_message="Error getting workspace", return_format="json")

        if return_item:
            return Workspace.from_dict(ws_dict, core_client=self)
        return ws_dict

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
            
        raise Exception(f"Workspace with name {name} not found")
            
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
    
    # PUT https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/networking/communicationPolicy
    def set_network_communication_policy(self, workspace_id, inbound, outbound, if_match = None):
        """Set the network communication policy for a workspace to allow all traffic
        Args:
            workspace_id (str): The ID of the workspace
            inbound (list): The list of inbound rules
            outbound (list): The list of outbound rules
            if_match (str): The ETag value to match
        Returns:
            dict: The updated network communication policy
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/networking/communicationPolicy"

        headers = self.auth.get_headers()
        if if_match:
            headers['If-Match'] = if_match

        body = {
            "inbound": inbound,
            "outbound": outbound,
        }

        response = self.calling_routine(url, operation="PUT", body=body, headers=headers,
                                             response_codes=[200, 429], error_message="Error setting network communication policy",
                                             return_format="response")

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

    def list_mirrored_warehouses(self, workspace_id):
        """List mirrored warehouses in a workspace"""
        return self.list_items(workspace_id, type="mirroredWarehouses")
    

    #airflowjob
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs
    def create_apache_airflow_job(self, workspace_id, display_name, definition = None, description = None, folder_id = None):
        """Create an Apache Airflow job in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the Apache Airflow job
            definition (dict): The definition of the Apache Airflow job
            description (str): The description of the Apache Airflow job
            folder_id (str): The ID of the folder to create the job in
        Returns:
            ApacheAirflowJob: The created Apache Airflow job object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "ApacheAirflowJobs",
                                definition = definition,
                                description = description, folder_id=folder_id)
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs/{ApacheAirflowJobId}
    def delete_apache_airflow_job(self, workspace_id, apache_airflow_job_id):
        """Delete an Apache Airflow job from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            apache_airflow_job_id (str): The ID of the Apache Airflow job
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=apache_airflow_job_id, type="ApacheAirflowJobs")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs/{ApacheAirflowJobId}
    def get_apache_airflow_job(self, workspace_id, apache_airflow_job_id = None, apache_airflow_job_name = None):
        """Get an Apache Airflow job from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            apache_airflow_job_id (str): The ID of the Apache Airflow job
            apache_airflow_job_name (str): The name of the Apache Airflow job
        Returns:
            ApacheAirflowJob: The Apache Airflow job object
        """
        from msfabricpysdkcore.otheritems import ApacheAirflowJob

        if apache_airflow_job_id is None and apache_airflow_job_name is not None:
            apache_airflow_jobs = self.list_apache_airflow_jobs(workspace_id)
            aajs = [aaj for aaj in apache_airflow_jobs if aaj.display_name == apache_airflow_job_name]
            if len(aajs) == 0:
                raise Exception(f"Apache Airflow job with name {apache_airflow_job_name} not found")
            apache_airflow_job_id = aajs[0].id
        elif apache_airflow_job_id is None:
            raise Exception("apache_airflow_job_id or the apache_airflow_job_name is required")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/ApacheAirflowJobs/{apache_airflow_job_id}"
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting Apache Airflow job", return_format="json")
        aaj = ApacheAirflowJob.from_dict(item_dict, core_client=self)
        aaj.get_definition()
        return aaj
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs/{ApacheAirflowJobId}/getDefinition
    def get_apache_airflow_job_definition(self, workspace_id, apache_airflow_job_id, format = None):
        """Get the definition of an Apache Airflow job
        Args:
            workspace_id (str): The ID of the workspace
            apache_airflow_job_id (str): The ID of the Apache Airflow job
            format (str): The format of the definition
        Returns:
            dict: The Apache Airflow job definition
        """
        return self.get_item_definition(workspace_id, apache_airflow_job_id, type="ApacheAirflowJobs", format=format)
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs
    def list_apache_airflow_jobs(self, workspace_id, with_properties = False):
        """List Apache Airflow jobs in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of Apache Airflow jobs
        """
        return self.list_items(workspace_id, type="ApacheAirflowJobs", with_properties=with_properties)
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs/{ApacheAirflowJobId}
    def update_apache_airflow_job(self, workspace_id, apache_airflow_job_id,
                                    display_name = None, description = None, return_item=False):
        """Update an Apache Airflow job in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            apache_airflow_job_id (str): The ID of the Apache Airflow job
            display_name (str): The display name of the Apache Airflow job
            description (str): The description of the Apache Airflow job
        Returns:
            dict: The updated Apache Airflow job or ApacheAirflowJob object if return_item is True
        """
        return self.update_item(workspace_id, item_id=apache_airflow_job_id, display_name=display_name, description=description, type="ApacheAirflowJobs",
                                return_item=return_item)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/ApacheAirflowJobs/{ApacheAirflowJobId}/updateDefinition
    def update_apache_airflow_job_definition(self, workspace_id, apache_airflow_job_id, definition, update_metadata = None):
        """Update the definition of an Apache Airflow job
        Args:
            workspace_id (str): The ID of the workspace
            apache_airflow_job_id (str): The ID of the Apache Airflow job
            definition (dict): The definition of the Apache Airflow job
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated Apache Airflow job definition
        """
        return self.update_item_definition(workspace_id, apache_airflow_job_id, type="ApacheAirflowJobs", definition=definition, update_metadata=update_metadata)

    # Anomaly Detectors
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors
    def create_anomaly_detector(self, workspace_id, display_name, definition = None, description = None, folder_id = None):
        """Create an anomaly detector in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the anomaly detector
            definition (dict): The definition of the anomaly detector
            description (str): The description of the anomaly detector
            folder_id (str): The ID of the folder to create the anomaly detector in
        Returns:
            AnomalyDetector: The created anomaly detector object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "anomalydetectors",
                                definition = definition,
                                description = description, folder_id=folder_id)
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors/{anomalyDetectorId}
    def delete_anomaly_detector(self, workspace_id, anomaly_detector_id):
        """Delete an anomaly detector from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            anomaly_detector_id (str): The ID of the anomaly detector
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=anomaly_detector_id, type="anomalydetectors")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors/{anomalyDetectorId}
    def get_anomaly_detector(self, workspace_id, anomaly_detector_id = None, anomaly_detector_name = None):
        """Get an anomaly detector from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            anomaly_detector_id (str): The ID of the anomaly detector
            anomaly_detector_name (str): The name of the anomaly detector
        Returns:
            AnomalyDetector: The anomaly detector object
        """
        from msfabricpysdkcore.otheritems import AnomalyDetector

        if anomaly_detector_id is None and anomaly_detector_name is not None:
            anomaly_detectors = self.list_anomaly_detectors(workspace_id)
            ads = [ad for ad in anomaly_detectors if ad.display_name == anomaly_detector_name]
            if len(ads) == 0:
                raise Exception(f"Anomaly detector with name {anomaly_detector_name} not found")
            anomaly_detector_id = ads[0].id
        elif anomaly_detector_id is None:
            raise Exception("anomaly_detector_id or the anomaly_detector_name is required")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/anomalydetectors/{anomaly_detector_id}"
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting anomaly detector", return_format="json")
        ad = AnomalyDetector.from_dict(item_dict, core_client=self)
        ad.get_definition()
        return ad
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors/{anomalyDetectorId}/getDefinition
    def get_anomaly_detector_definition(self, workspace_id, anomaly_detector_id, format = None):
        """Get the definition of an anomaly detector
        Args:
            workspace_id (str): The ID of the workspace
            anomaly_detector_id (str): The ID of the anomaly detector
            format (str): The format of the definition
        Returns:
            dict: The anomaly detector definition
        """
        return self.get_item_definition(workspace_id, anomaly_detector_id, type="anomalydetectors", format=format)
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors
    def list_anomaly_detectors(self, workspace_id, with_properties = False):
        """List anomaly detectors in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of anomaly detectors
        """
        return self.list_items(workspace_id, type="anomalydetectors", with_properties=with_properties)
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors/{anomalyDetectorId}
    def update_anomaly_detector(self, workspace_id, anomaly_detector_id,
                                    display_name = None, description = None, return_item=False):
        """Update an anomaly detector in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            anomaly_detector_id (str): The ID of the anomaly detector
            display_name (str): The display name of the anomaly detector
            description (str): The description of the anomaly detector
            return_item (bool): Whether to return the item object
        Returns:
            dict: The updated anomaly detector or AnomalyDetector object if return_item is True
        """
        return self.update_item(workspace_id, item_id=anomaly_detector_id, display_name=display_name, description=description, type="anomalydetectors",
                                return_item=return_item)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/anomalydetectors/{anomalyDetectorId}/updateDefinition
    def update_anomaly_detector_definition(self, workspace_id, anomaly_detector_id, definition, update_metadata = None):
        """Update the definition of an anomaly detector
        Args:
            workspace_id (str): The ID of the workspace
            anomaly_detector_id (str): The ID of the anomaly detector
            definition (dict): The definition of the anomaly detector
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated anomaly detector definition
        """
        return self.update_item_definition(workspace_id, anomaly_detector_id, type="anomalydetectors", definition=definition, update_metadata=update_metadata)

    # copyJobs
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/copyJobs
    def create_copy_job(self, workspace_id, display_name, definition = None, description = None):
        """Create a copy job in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the copy job
            definition (dict): The definition of the copy job
            description (str): The description of the copy job
        Returns:
            CopyJob: The copy job object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "copyJobs",
                                definition = definition,
                                description = description)
    
    def delete_copy_job(self, workspace_id, copy_job_id):
        """Delete a copy job from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            copy_job_id (str): The ID of the copy job
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=copy_job_id, type="copyJobs")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/copyJobs/{copyJobId}
    def get_copy_job(self, workspace_id, copy_job_id = None, copy_job_name = None):
        """Get a copy job from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            copy_job_id (str): The ID of the copy job
            copy_job_name (str): The name of the copy job
        Returns:
            CopyJob: The copy job object
        """
        from msfabricpysdkcore.otheritems import CopyJob

        if copy_job_id is None and copy_job_name is not None:
            copy_jobs = self.list_copy_jobs(workspace_id)
            cjs = [cj for cj in copy_jobs if cj.display_name == copy_job_name]
            if len(cjs) == 0:
                raise Exception(f"Copy job with name {copy_job_name} not found")
            copy_job_id = cjs[0].id
        elif copy_job_id is None:
            raise Exception("copy_job_id or the copy_job_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/copyJobs/{copy_job_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting copy job", return_format="json")

        cj = CopyJob.from_dict(item_dict, core_client=self)
        cj.get_definition()
        return cj
    
    def get_copy_job_definition(self, workspace_id, copy_job_id, format = None):
        """Get the definition of an copy job
        Args:
            workspace_id (str): The ID of the workspace
            copy_job_id (str): The ID of the copy job
            format (str): The format of the definition
        Returns:
            dict: The copy job definition
        """
        return self.get_item_definition(workspace_id, copy_job_id, type="copyJobs", format=format)

    def list_copy_jobs(self, workspace_id, with_properties = False):
        """List copy jobs in a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            list: The list of copy jobs
        """
        return self.list_items(workspace_id, type="copyJobs", with_properties=with_properties)

    def update_copy_job(self, workspace_id, copy_job_id, display_name = None, description = None, return_item=False):
        """Update a copy job in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            copy_job_id (str): The ID of the copy job
            display_name (str): The display name of the copy job
            description (str): The description of the copy job
        Returns:
            dict: The updated copy job or CopyJob object if return_item is True
        """
        return self.update_item(workspace_id, item_id=copy_job_id, display_name=display_name, description=description, type="copyJobs",
                                return_item=return_item)
    
    def update_copy_job_definition(self, workspace_id, copy_job_id, definition, update_metadata = None):
        """Update the definition of an copy job
        Args:
            workspace_id (str): The ID of the workspace
            copy_job_id (str): The ID of the copy job
            definition (dict): The definition of the copy job
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated copy job definition
        """
        return self.update_item_definition(workspace_id, copy_job_id, type="copyJobs", definition=definition, update_metadata=update_metadata)


    # user data functions
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions
    def create_user_data_function(self, workspace_id, display_name, definition = None, description = None):
        """Create a user data function in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the user data function
            definition (dict): The definition of the user data function
            description (str): The description of the user data function
        Returns:
            UserDataFunction: The created user data function object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "UserDataFunctions",
                                definition = definition,
                                description = description)
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions/{UserDataFunctionId}
    def delete_user_data_function(self, workspace_id, user_data_function_id):
        """Delete a user data function from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            user_data_function_id (str): The ID of the user data function
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=user_data_function_id, type="UserDataFunctions")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions/{UserDataFunctionId}
    def get_user_data_function(self, workspace_id, user_data_function_id = None, user_data_function_name = None):
        """Get a user data function from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            user_data_function_id (str): The ID of the user data function
            user_data_function_name (str): The name of the user data function
        Returns:
            UserDataFunction: The user data function object
        """
        from msfabricpysdkcore.otheritems import UserDataFunction

        if user_data_function_id is None and user_data_function_name is not None:
            user_data_functions = self.list_user_data_functions(workspace_id)
            udfs = [udf for udf in user_data_functions if udf.display_name == user_data_function_name]
            if len(udfs) == 0:
                raise Exception(f"User data function with name {user_data_function_name} not found")
            user_data_function_id = udfs[0].id
        elif user_data_function_id is None:
            raise Exception("user_data_function_id or the user_data_function_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/UserDataFunctions/{user_data_function_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting user data function", return_format="json")

        udf = UserDataFunction.from_dict(item_dict, core_client=self)
        udf.get_definition()
        return udf

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions/{UserDataFunctionId}/getDefinition
    def get_user_data_function_definition(self, workspace_id, user_data_function_id, format = None):
        """Get the definition of an user data function
        Args:
            workspace_id (str): The ID of the workspace
            user_data_function_id (str): The ID of the user data function
            format (str): The format of the definition
        Returns:
            dict: The user data function definition
        """
        return self.get_item_definition(workspace_id, user_data_function_id, type="UserDataFunctions", format=format)
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions
    def list_user_data_functions(self, workspace_id, with_properties = False):
        """List user data functions in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of user data functions
        """
        return self.list_items(workspace_id, type="UserDataFunctions", with_properties=with_properties)
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions/{UserDataFunctionId}
    def update_user_data_function(self, workspace_id, user_data_function_id, display_name = None, description = None):
        """Update a user data function in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            user_data_function_id (str): The ID of the user data function
            display_name (str): The display name of the user data function
            description (str): The description of the user data function
        Returns:
            dict: The updated user data function
        """
        return self.update_item(workspace_id, item_id=user_data_function_id, display_name=display_name, description=description, type="UserDataFunctions")
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/UserDataFunctions/{UserDataFunctionId}/updateDefinition?updateMetadata={updateMetadata}
    def update_user_data_function_definition(self, workspace_id, user_data_function_id, definition,
                                             update_metadata = None):
        """Update the definition of an user data function
        Args:
            workspace_id (str): The ID of the workspace
            user_data_function_id (str): The ID of the user data function
            definition (dict): The definition of the user data function
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated user data function definition
        """
        return self.update_item_definition(workspace_id, user_data_function_id, type="UserDataFunctions", definition=definition, update_metadata=update_metadata)



    # variable libary
    def create_variable_library(self, workspace_id, display_name, definition = None, description = None):
        """Create a copy job in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the copy job
            definition (dict): The definition of the copy job
            description (str): The description of the copy job
        Returns:
            VariableLibrary: The created variable library
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name=display_name,
                                type="VariableLibraries",
                                definition=definition,
                                description=description)

    def delete_variable_library(self, workspace_id, variable_library_id):
        """Delete a variable library from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            variable_library_id (str): The ID of the variable library
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=variable_library_id, type="VariableLibraries")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/VariableLibraries/{variableLibraryId}
    def get_variable_library(self, workspace_id, variable_library_id = None, variable_library_name = None):
        """Get a variable library from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            variable_library_id (str): The ID of the variable library
            variable_library_name (str): The name of the variable library
        Returns:
            VariableLibrary: The variable library object
        """
        from msfabricpysdkcore.otheritems import VariableLibrary

        if variable_library_id is None and variable_library_name is not None:
            variable_librarys = self.list_variable_librarys(workspace_id)
            cjs = [cj for cj in variable_librarys if cj.display_name == variable_library_name]
            if len(cjs) == 0:
                raise Exception(f"Variable library with name {variable_library_name} not found")
            variable_library_id = cjs[0].id
        elif variable_library_id is None:
            raise Exception("variable_library_id or the variable_library_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/VariableLibraries/{variable_library_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting variable library", return_format="json")

        vl = VariableLibrary.from_dict(item_dict, core_client=self)
        vl.get_definition()
        return vl

    def get_variable_library_definition(self, workspace_id, variable_library_id, format = None):
        """Get the definition of an variable library
        Args:
            workspace_id (str): The ID of the workspace
            variable_library_id (str): The ID of the variable library
            format (str): The format of the definition
        Returns:
            dict: The variable library definition
        """
        return self.get_item_definition(workspace_id, variable_library_id, type="VariableLibraries", format=format)

    def list_variable_libraries(self, workspace_id, with_properties = False):
        """List variable libraries in a workspace
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            list: The list of variable libraries
        """
        return self.list_items(workspace_id, type="VariableLibraries", with_properties=with_properties)

    def update_variable_library(self, workspace_id, variable_library_id, display_name = None, description = None, return_item=False):
        """Update a variable library in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            variable_library_id (str): The ID of the variable library
            display_name (str): The display name of the variable library
            description (str): The description of the variable library
        Returns:
            dict: The updated variable library or VariableLibrary object if return_item is True
        """
        return self.update_item(workspace_id, item_id=variable_library_id, display_name=display_name, description=description, type="VariableLibraries",
                                return_item=return_item)
    
    def update_variable_library_definition(self, workspace_id, variable_library_id, definition, update_metadata = None):
        """Update the definition of an variable library
        Args:
            workspace_id (str): The ID of the workspace
            variable_library_id (str): The ID of the variable library
            definition (dict): The definition of the variable library
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated variable library definition
        """
        return self.update_item_definition(workspace_id, variable_library_id, type="VariableLibraries", definition=definition, update_metadata=update_metadata)


    # data flow
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows
    def create_dataflow(self, workspace_id, display_name, definition = None, description = None):
        """Create a dataflow in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the dataflow
            definition (dict): The definition of the dataflow
            description (str): The description of the dataflow
        Returns:
            dict: The created dataflow
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "dataflows",
                                definition = definition,
                                description = description)
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}
    def delete_dataflow(self, workspace_id, dataflow_id):
        """Delete a dataflow from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=dataflow_id, type="dataflows")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/parameters?continuationToken={continuationToken}
    def discover_dataflow_parameters(self, workspace_id, dataflow_id):
        """List parameters for a dataflow in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
        Returns:
            list: The list of dataflow parameters
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataflows/{dataflow_id}/parameters"

        parameters = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                                error_message="Error listing dataflow parameters", return_format = "value_json",
                                                paging = True)

        return parameters


    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}
    def get_dataflow(self, workspace_id, dataflow_id = None, dataflow_name = None):
        """Get a dataflow from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            dataflow_name (str): The name of the dataflow
        Returns:
            Dataflow: The dataflow object
        """
        from msfabricpysdkcore.otheritems import Dataflow

        if dataflow_id is None and dataflow_name is not None:
            dataflows = self.list_dataflows(workspace_id)
            dfs = [df for df in dataflows if df.display_name == dataflow_name]
            if len(dfs) == 0:
                raise Exception(f"Dataflow with name {dataflow_name} not found")
            dataflow_id = dfs[0].id
        elif dataflow_id is None:
            raise Exception("dataflow_id or the dataflow_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataflows/{dataflow_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting data flow", return_format="json")

        df = Dataflow.from_dict(item_dict, core_client=self)
        df.get_definition()
        return df
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/getDefinition
    def get_dataflow_definition(self, workspace_id, dataflow_id, format = None):
        """Get the definition of a dataflow
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            format (str): The format of the definition
        Returns:
            dict: The dataflow definition
        """
        return self.get_item_definition(workspace_id, dataflow_id, type="dataflows", format=format)
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows
    def list_dataflows(self, workspace_id, with_properties = False):
        """List dataflows in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of dataflows
        """
        return self.list_items(workspace_id, type="dataflows", with_properties=with_properties)
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}
    def update_dataflow(self, workspace_id, dataflow_id, display_name = None, description = None, return_item=False):
        """Update a dataflow in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            display_name (str): The display name of the dataflow
            description (str): The description of the dataflow
        Returns:
            dict: The updated dataflow
        """
        return self.update_item(workspace_id, item_id=dataflow_id, display_name=display_name, description=description, type="dataflows",
                                return_item=return_item)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/updateDefinition
    def update_dataflow_definition(self, workspace_id, dataflow_id, definition, update_metadata = None):
        """Update the definition of a dataflow
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            definition (dict): The definition of the dataflow
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated dataflow definition
        """
        return self.update_item_definition(workspace_id, dataflow_id, type="dataflows", definition=definition, update_metadata=update_metadata)

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/jobs/instances?jobType={jobType}
    def run_on_demand_apply_changes(self, workspace_id, dataflow_id, job_type = "ApplyChanges", wait_for_completion = True):
        """Run an on-demand apply changes job for a dataflow
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            job_type (str): The type of the job, default is "ApplyChanges"
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataflows/{dataflow_id}/jobs/instances?jobType={job_type}"

        response = self.calling_routine(url, operation="POST", response_codes=[202, 429], error_message="Error running on-demand apply changes",
                                        return_format="response", wait_for_completion=wait_for_completion)

        return response
    
    def run_on_demand_execute(self, workspace_id, dataflow_id, job_type = "Execute", wait_for_completion = True):
        """Run an on-demand execute job for a dataflow
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            job_type (str): The type of the job, default is "Execute"
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataflows/{dataflow_id}/jobs/instances?jobType={job_type}"

        response = self.calling_routine(url, operation="POST", response_codes=[202, 429], error_message="Error running on-demand execute",
                                        return_format="response", wait_for_completion=wait_for_completion)

        return response

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/jobs/ApplyChanges/schedules
    def schedule_apply_changes(self, workspace_id, dataflow_id, configuration, enabled):
        """Schedule an apply changes job for a dataflow
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            configuration (dict): The configuration of the schedule
            enabled (bool): Whether the schedule is enabled
        Returns:
            dict: The schedule object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataflows/{dataflow_id}/jobs/ApplyChanges/schedules"

        body = {
            "configuration": configuration,
            "enabled": enabled
        }

        response_dict = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429], error_message="Error scheduling apply changes",
                                        return_format="json")

        return response_dict
    
    def schedule_execute(self, workspace_id, dataflow_id, configuration, enabled):
        """Schedule an execute job for a dataflow
        Args:
            workspace_id (str): The ID of the workspace
            dataflow_id (str): The ID of the dataflow
            configuration (dict): The configuration of the schedule
            enabled (bool): Whether the schedule is enabled
        Returns:
            dict: The schedule object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataflows/{dataflow_id}/jobs/Execute/schedules"

        body = {
            "configuration": configuration,
            "enabled": enabled
        }

        response_dict = self.calling_routine(url, operation="POST", body=body, response_codes=[201, 429], error_message="Error scheduling execute",
                                        return_format="json")

        return response_dict



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
    
    def get_data_pipeline_definition(self, workspace_id, data_pipeline_id, format = None):
        """Get the definition of a data pipeline
        Args:
            workspace_id (str): The ID of the workspace
            data_pipeline_id (str): The ID of the data pipeline
            format (str): The format of the definition
        Returns:
            dict: The data pipeline definition
        """
        return self.get_item_definition(workspace_id, data_pipeline_id, type="dataPipelines", format=format)

    
    def list_data_pipelines(self, workspace_id, with_properties = False):
        """List data pipelines in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of data pipelines
        """
        return self.list_items(workspace_id, type="dataPipelines", with_properties=with_properties)
    
    def update_data_pipeline(self, workspace_id, data_pipeline_id, display_name = None, description = None, return_item=False):
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
    
    def update_data_pipeline_definition(self, workspace_id, data_pipeline_id, definition, update_metadata = None):
        """Update the definition of a data pipeline
        Args:
            workspace_id (str): The ID of the workspace
            data_pipeline_id (str): The ID of the data pipeline
            definition (dict): The definition of the data pipeline
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated data pipeline definition
        """
        return self.update_item_definition(workspace_id, data_pipeline_id, type="dataPipelines", definition=definition, update_metadata=update_metadata)
    
    # digitaltwinbuilder
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/digitaltwinbuilders
    def create_digital_twin_builder(self, workspace_id, display_name, definition = None, description = None, folder_id = None):
        """Create a digital twin builder in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the digital twin builder
            definition (dict): The definition of the digital twin builder
            description (str): The description of the digital twin builder
            folder_id (str): The ID of the folder to create the digital twin builder in
        Returns:
            DigitalTwinBuilder: The created digital twin builder object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "digitaltwinbuilders",
                                definition = definition,
                                description = description, folder_id=folder_id)
    
    def delete_digital_twin_builder(self, workspace_id, digital_twin_builder_id):
        """Delete a digital twin builder from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_id (str): The ID of the digital twin builder
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=digital_twin_builder_id, type="digitaltwinbuilders")
    
    def get_digital_twin_builder(self, workspace_id, digital_twin_builder_id = None, digital_twin_builder_name = None):
        """Get a digital twin builder from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_id (str): The ID of the digital twin builder
            digital_twin_builder_name (str): The name of the digital twin builder
        Returns:
            DigitalTwinBuilder: The digital twin builder object
        """
        from msfabricpysdkcore.otheritems import DigitalTwinBuilder

        if digital_twin_builder_id is None and digital_twin_builder_name is not None:
            digital_twin_builders = self.list_digital_twin_builders(workspace_id)
            dtbs = [dtb for dtb in digital_twin_builders if dtb.display_name == digital_twin_builder_name]
            if len(dtbs) == 0:
                raise Exception(f"Digital twin builder with name {digital_twin_builder_name} not found")
            digital_twin_builder_id = dtbs[0].id
        elif digital_twin_builder_id is None:
            raise Exception("digital_twin_builder_id or the digital_twin_builder_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/digitaltwinbuilders/{digital_twin_builder_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting digital twin builder", return_format="json")

        dtb = DigitalTwinBuilder.from_dict(item_dict, core_client=self)
        dtb.get_definition()
        return dtb
    
    def get_digital_twin_builder_definition(self, workspace_id, digital_twin_builder_id, format = None):
        """Get the definition of a digital twin builder
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_id (str): The ID of the digital twin builder
            format (str): The format of the definition
        Returns:
            dict: The digital twin builder definition
        """
        return self.get_item_definition(workspace_id, digital_twin_builder_id, type="digitaltwinbuilders", format=format)
    
    def list_digital_twin_builders(self, workspace_id, with_properties = False):
        """List digital twin builders in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of digital twin builders
        """
        return self.list_items(workspace_id, type="digitaltwinbuilders", with_properties=with_properties)
    
    def update_digital_twin_builder(self, workspace_id, digital_twin_builder_id, display_name = None, description = None, return_item=False):
        """Update a digital twin builder in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_id (str): The ID of the digital twin builder
            display_name (str): The display name of the digital twin builder
            description (str): The description of the digital twin builder
        Returns:
            dict: The updated digital twin builder or DigitalTwinBuilder object if return_item is True
        """
        return self.update_item(workspace_id, item_id=digital_twin_builder_id, display_name=display_name, description=description, type="digitaltwinbuilders",
                                return_item=return_item)
    
    def update_digital_twin_builder_definition(self, workspace_id, digital_twin_builder_id, definition, update_metadata = None):
        """Update the definition of a digital twin builder
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_id (str): The ID of the digital twin builder
            definition (dict): The definition of the digital twin builder
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated digital twin builder definition
        """
        return self.update_item_definition(workspace_id, digital_twin_builder_id, type="digitaltwinbuilders", definition=definition, update_metadata=update_metadata)

    # digital twin builder flows
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/DigitalTwinBuilderFlows
    def create_digital_twin_builder_flow(self, workspace_id, display_name, creation_payload, definition = None, description = None):
        """Create a digital twin builder flow in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the digital twin builder flow
            creation_payload (dict): The creation payload for the digital twin builder flow
            definition (dict): The definition of the digital twin builder flow
            description (str): The description of the digital twin builder flow
        Returns:
            DigitalTwinBuilderFlow: The created digital twin builder flow object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "DigitalTwinBuilderFlows",
                                definition = definition,
                                description = description, creation_payload=creation_payload)
    
    def delete_digital_twin_builder_flow(self, workspace_id, digital_twin_builder_flow_id):
        """Delete a digital twin builder flow from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_flow_id (str): The ID of the digital twin builder flow
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=digital_twin_builder_flow_id, type="DigitalTwinBuilderFlows")

    def get_digital_twin_builder_flow(self, workspace_id, digital_twin_builder_flow_id = None, digital_twin_builder_flow_name = None):
        """Get a digital twin builder flow from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_flow_id (str): The ID of the digital twin builder flow
            digital_twin_builder_flow_name (str): The name of the digital twin builder flow
        Returns:
            DigitalTwinBuilderFlow: The digital twin builder flow object
        """
        from msfabricpysdkcore.otheritems import DigitalTwinBuilderFlow

        if digital_twin_builder_flow_id is None and digital_twin_builder_flow_name is not None:
            digital_twin_builder_flows = self.list_digital_twin_builder_flows(workspace_id)
            dtbfs = [dtbf for dtbf in digital_twin_builder_flows if dtbf.display_name == digital_twin_builder_flow_name]
            if len(dtbfs) == 0:
                raise Exception(f"Digital twin builder flow with name {digital_twin_builder_flow_name} not found")
            digital_twin_builder_flow_id = dtbfs[0].id
        elif digital_twin_builder_flow_id is None:
            raise Exception("digital_twin_builder_flow_id or the digital_twin_builder_flow_name is required")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/DigitalTwinBuilderFlows/{digital_twin_builder_flow_id}"
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting digital twin builder flow", return_format="json")
        dtbf = DigitalTwinBuilderFlow.from_dict(item_dict, core_client=self)
        dtbf.get_definition()
        return dtbf
    
    def get_digital_twin_builder_flow_definition(self, workspace_id, digital_twin_builder_flow_id, format = None):
        """Get the definition of a digital twin builder flow
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_flow_id (str): The ID of the digital twin builder flow
            format (str): The format of the definition
        Returns:
            dict: The digital twin builder flow definition
        """
        return self.get_item_definition(workspace_id, digital_twin_builder_flow_id, type="DigitalTwinBuilderFlows", format=format)
    
    def list_digital_twin_builder_flows(self, workspace_id, with_properties = False):
        """List digital twin builder flows in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of digital twin builder flows
        """
        return self.list_items(workspace_id, type="DigitalTwinBuilderFlows", with_properties=with_properties)
    
    def update_digital_twin_builder_flow(self, workspace_id, digital_twin_builder_flow_id, display_name = None, description = None, return_item=False):
        """Update a digital twin builder flow in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_flow_id (str): The ID of the digital twin builder flow
            display_name (str): The display name of the digital twin builder flow
            description (str): The description of the digital twin builder flow
        Returns:
            dict: The updated digital twin builder flow or DigitalTwinBuilderFlow object if return_item is True
        """
        return self.update_item(workspace_id, item_id=digital_twin_builder_flow_id, display_name=display_name, description=description, type="DigitalTwinBuilderFlows",
                                return_item=return_item)
    
    def update_digital_twin_builder_flow_definition(self, workspace_id, digital_twin_builder_flow_id, definition, update_metadata = None):
        """Update the definition of a digital twin builder flow
        Args:
            workspace_id (str): The ID of the workspace
            digital_twin_builder_flow_id (str): The ID of the digital twin builder flow
            definition (dict): The definition of the digital twin builder flow
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated digital twin builder flow definition
        """
        return self.update_item_definition(workspace_id, digital_twin_builder_flow_id, type="DigitalTwinBuilderFlows", definition=definition, update_metadata=update_metadata)

    # environments
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/cancelPublish
    def cancel_publish(self, workspace_id, environment_id):
        logger.warning("cancel_publish is deprecated. Use cancel_publish_environment instead.")
        print("WARNING: cancel_publish is deprecated. Use cancel_publish_environment instead.")
        self.cancel_publish_environment(workspace_id, environment_id)

    def cancel_publish_environment(self, workspace_id, environment_id):
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
    
    def create_environment(self, workspace_id, display_name, definition = None, description = None, folder_id = None):
        """Create an environment in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the environment
            definition (dict): The definition of the environment
            description (str): The description of the environment
        Returns:
            dict: The created environment
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "environments",
                                definition = definition,
                                description = description,
                                folder_id = folder_id)
    
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
        env.get_definition()
        return env

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/getDefinition
    def get_environment_definition(self, workspace_id, environment_id, format = None):
        """Get the definition of an environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            format (str): The format of the definition
        Returns:
            dict: The environment definition
        """
        return self.get_item_definition(workspace_id, environment_id, type="environments", format=format)

    def list_environments(self, workspace_id, with_properties = False):
        """List environments in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of environments
        """
        return self.list_items(workspace_id, type="environments", with_properties=with_properties)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/publish?preview={preview}
    def publish_environment(self, workspace_id, environment_id, preview="false"):
        """Publish the staging settings and libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            preview (bool): Whether to publish as a preview
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/publish?preview={preview}"

        resp_dict = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error publishing staging",
                                         return_format="json+operation_result")

        return resp_dict
    
    def update_environment(self, workspace_id, environment_id, display_name = None, description = None, return_item=False):
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

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/updateDefinition?updateMetadata={updateMetadata}
    def update_environment_definition(self, workspace_id, environment_id, definition, update_metadata = None):
        """Update the definition of an environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            definition (dict): The definition of the environment
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated environment definition
        """
        return self.update_item_definition(workspace_id, environment_id, type="environments",
                                           definition=definition, update_metadata=update_metadata)

    # Published

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/libraries/exportExternalLibraries
    def export_published_external_libraries(self, workspace_id, environment_id):
        """Export the external libraries of the published environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The exported external libraries
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/libraries/exportExternalLibraries"

        headers = self.auth.get_headers()
        headers["Content-Type"] = "application/octet-stream"
        response = self.calling_routine(url, headers=headers, operation="GET", response_codes=[200, 429],
                                         error_message="Error exporting external libraries", return_format="response")
        return response
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/sparkcompute?preview={preview}
    def get_published_spark_compute(self, workspace_id, environment_id, preview = "false"):
        """Get the spark compute settings of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            preview (str): Whether to get the preview settings
        Returns:
            dict: The spark compute settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/sparkcompute?preview={preview}"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting spark compute settings", return_format="json")     
        return resp_json
    
    def get_published_settings(self, workspace_id, environment_id, preview = "false"):
        logger.warning("get_published_settings is deprecated. Use get_spark_compute with preview='false' instead.")
        print("WARNING: get_published_settings is deprecated. Use get_spark_compute with preview='false' instead.")
        return self.get_published_spark_compute(workspace_id, environment_id, preview=preview)

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/libraries?preview={preview}
    def list_published_libraries(self, workspace_id, environment_id, preview="false"):
        """List the libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            preview (str): Whether to get the preview libraries
        Returns:
            dict: The libraries
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/libraries?preview={preview}"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error listing libraries", return_format="json")
        return resp_json
    
    def get_published_libraries(self, workspace_id, environment_id, preview="false"):
        logger.warning("get_published_libraries is deprecated. Use list_libraries with preview='false' instead.")
        print("WARNING: get_published_libraries is deprecated. Use list_libraries with preview='false' instead.")
        return self.list_published_libraries(workspace_id, environment_id, preview=preview)
    
    

    # Staging
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries/{libraryName}
    def delete_custom_library(self, workspace_id, environment_id, library_name):
        """Delete a custom library from the published libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            library_name (str): The name of the library to delete
            preview (str): Whether to delete from the preview libraries
        Returns:
            requests.Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries/{library_name}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429],
                                        error_message="Error deleting staging library", return_format="response")

        return response


    def delete_staging_library(self, workspace_id, environment_id, library_to_delete):
        """Delete a library from the staging libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            library_to_delete (str): The library to delete
        Returns:
            requests.Response: The response object
        """
        logger.warning("delete_staging_library is deprecated. Use delete_custom_library instead.")
        print("WARNING: delete_staging_library is deprecated. Use delete_custom_library instead.")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries?libraryToDelete={library_to_delete}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429], error_message="Error deleting staging library", return_format="response")

        return response
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries/exportExternalLibraries
    def export_staging_external_libraries(self, workspace_id, environment_id):
        """Export the external libraries of the staging environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
        Returns:
            dict: The exported external libraries
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries/exportExternalLibraries"

        headers = self.auth.get_headers()
        headers["Content-Type"] = "application/octet-stream"
        response = self.calling_routine(url, headers=headers, operation="GET", response_codes=[200, 429],
                                         error_message="Error exporting staging external libraries", return_format="response")
        return response

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/sparkcompute?preview={preview}
    def get_staging_spark_compute(self, workspace_id, environment_id, preview="false"):
        """Get the spark compute settings of the staging environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            preview (str): Whether to get the preview settings
        Returns:
            dict: The spark compute settings
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/sparkcompute?preview={preview}"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], error_message="Error getting staging spark compute settings", return_format="json")       
        return resp_json
    
    def get_staging_settings(self, workspace_id, environment_id, preview="false"):
        logger.warning("get_staging_settings is deprecated. Use get_staging_spark_compute with preview='false' instead.")
        print("WARNING: get_staging_settings is deprecated. Use get_staging_spark_compute with preview='false' instead.")
        return self.get_staging_spark_compute(workspace_id, environment_id, preview=preview)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries/importExternalLibraries
    def import_external_libraries_to_staging(self, workspace_id, environment_id, file_path):
        """Import external libraries to the staging environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            file_path (str): The file path to import
        Returns:
            requests.Response: The response object
        """
        headers = self.auth.get_headers()
        headers["Content-Type"] = "application/octet-stream"
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries/importExternalLibraries"
        response = self.calling_routine(url, headers=headers, operation="POST", file_path=file_path, response_codes=[200, 429],
                                        error_message="Error importing external libraries to staging", return_format="response")
        return response
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries?preview={preview}&continuationToken={continuationToken}
    def list_staging_libraries(self, workspace_id, environment_id, preview="false"):
        """List the staging libraries of the environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            preview (str): Whether to get the preview libraries
        Returns:
            dict: The staging libraries
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries?preview={preview}"

        resp_json = self.calling_routine(url, operation="GET", response_codes=[200, 429], paging=True,
                                         error_message="Error listing staging libraries", return_format="libraries")
        return resp_json
    
    def get_staging_libraries(self, workspace_id, environment_id, preview="false"):
        logger.warning("get_staging_libraries is deprecated. Use list_staging_libraries instead.")
        print("WARNING: get_staging_libraries is deprecated. Use list_staging_libraries instead.")
        return self.list_staging_libraries(workspace_id, environment_id, preview=preview)
    

    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries/removeExternalLibrary

    def remove_external_library(self, workspace_id, environment_id, name, version):
        """Remove an external library from the staging environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            name (str): The name of the library
            version (str): The version of the library
        Returns:
            Response: The response object
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries/removeExternalLibrary"
        body = {
            "name": name,
            "version": version
        }
        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                        error_message="Error removing external library from staging", return_format="response")
        return response


    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/sparkcompute?preview={preview}
    def update_staging_spark_compute(self, workspace_id, environment_id,
                                       driver_cores=None, driver_memory=None, dynamic_executor_allocation=None,
                                       executor_cores=None, executor_memory=None, instance_pool=None,
                                       runtime_version=None, spark_properties=None, preview="false"):
        """Update the staging spark compute settings of the environment"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/sparkcompute?preview={preview}"
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
                                            error_message="Error updating staging spark compute settings", return_format="json")

        return respone_json

    def update_staging_settings(self, workspace_id, environment_id,
                                driver_cores = None, driver_memory = None, dynamic_executor_allocation = None,
                                executor_cores = None, executor_memory = None, instance_pool = None,
                                runtime_version = None, spark_properties = None, preview="false"):
        logger.warning("update_staging_settings is deprecated. Use update_staging_spark_compute instead.")
        print("WARNING: update_staging_settings is deprecated. Use update_staging_spark_compute instead.")
        return self.update_staging_spark_compute(workspace_id, environment_id,
                                                 driver_cores=driver_cores, driver_memory=driver_memory,
                                                    dynamic_executor_allocation=dynamic_executor_allocation,
                                                    executor_cores=executor_cores, executor_memory=executor_memory,
                                                    instance_pool=instance_pool, runtime_version=runtime_version,
                                                    spark_properties=spark_properties, preview=preview)

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/libraries/{libraryName}
    def upload_custom_library(self, workspace_id, environment_id, library_name, file_path):
        """Upload a custom library to the staging environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            library_name (str): The name of the library to upload
            file_path (str): The file path to upload
        Returns:
            requests.Response: The response object
        """
        headers = self.auth.get_headers()
        headers["Content-Type"] = "application/octet-stream"
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries/{library_name}"
        response = self.calling_routine(url, headers=headers, operation="POST", file_path=file_path, response_codes=[200, 429],
                                        error_message="Error uploading custom library", return_format="response")
        return response

    def upload_staging_library(self, workspace_id, environment_id, file_path):
        """Update staging libraries for an environment
        Args:
            workspace_id (str): The ID of the workspace
            environment_id (str): The ID of the environment
            file_path (str): The file path to upload
        Returns:
            requests.Response: The response object
        """
        logger.warning("upload_staging_library is deprecated. Use upload_custom_library instead.")
        print("WARNING: upload_staging_library is deprecated. Use upload_custom_library instead.")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"
        response = self.calling_routine(url, operation="POST", file_path=file_path, response_codes=[200, 429],
                                        error_message="Error uploading staging library", return_format="response")
        return response
    

    
    # eventhouses

    def create_eventhouse(self, workspace_id, display_name, definition = None, creation_payload = None, description = None):
        """Create an eventhouse in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the eventhouse
            definition (str): The definition of the eventhouse
            creation_payload (dict): The creation payload for the eventhouse
            description (str): The description of the eventhouse
        Returns:
            Eventhouse: The created eventhouse
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "eventhouses",
                                definition = definition,
                                creation_payload = creation_payload,
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
        ev = Eventhouse.from_dict(item_dict, core_client=self)
        ev.get_definition()
        return ev
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventhouses/{eventhouseId}/getDefinition

    def get_eventhouse_definition(self, workspace_id, eventhouse_id, format = None):
        """Get the definition of an eventhouse
        Args:
            workspace_id (str): The ID of the workspace
            eventhouse_id (str): The ID of the eventhouse
            format (str): The format of the definition
        Returns:
            dict: The eventhouse definition
        """
        return self.get_item_definition(workspace_id, eventhouse_id, type="eventhouses", format=format)

    def list_eventhouses(self, workspace_id, with_properties = False):
        """List eventhouses in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of eventhouses
        """
        return self.list_items(workspace_id=workspace_id, type="eventhouses", with_properties=with_properties)
    
    def update_eventhouse(self, workspace_id, eventhouse_id, display_name = None, description = None, return_item=False):
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

    def update_eventhouse_definition(self, workspace_id, eventhouse_id, definition, update_metadata = None):
        """Update the definition of an eventhouse
        Args:
            workspace_id (str): The ID of the workspace
            eventhouse_id (str): The ID of the eventhouse
            definition (dict): The definition of the eventhouse
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated eventhouse definition
        """
        return self.update_item_definition(workspace_id, eventhouse_id, type="eventhouses", definition=definition, update_metadata=update_metadata)


    # eventstreams

    def create_eventstream(self, workspace_id, display_name, description = None, definition = None, creation_payload = None):
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
                                definition = definition,
                                creation_payload= creation_payload,
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
        from msfabricpysdkcore.eventstream import Eventstream
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
        es = Eventstream.from_dict(item_dict, core_client=self)
        es.get_definition()
        return es
    
    def get_eventstream_definition(self, workspace_id, eventstream_id, format = None):
        """Get the definition of an eventstream

        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            format (str): The format of the definition
        Returns:
            dict: The eventstream definition
        """

        return self.get_item_definition(workspace_id, eventstream_id, type="eventstreams", format=format)


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

    def update_eventstream(self, workspace_id, eventstream_id, display_name = None, description = None, return_item=False):
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
    
    def update_eventstream_definition(self, workspace_id, eventstream_id, definition, update_metadata = None):
        """Update the definition of an eventstream
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            definition (dict): The definition of the eventstream
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated definition of the eventstream
        """
        return self.update_item_definition(workspace_id, eventstream_id, type="eventstreams", definition=definition, update_metadata=update_metadata)

    # eventstream topology

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/destinations/{destinationId}
    def get_eventstream_destination(self, workspace_id, eventstream_id, destination_id):
        """Get the destination of an eventstream
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            destination_id (str): The ID of the destination
        Returns:
            dict: The eventstream destination
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/destinations/{destination_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting eventstream destination", return_format="json")
        return item_dict
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/destinations/{destinationId}/connection
    def get_eventstream_destination_connection(self, workspace_id, eventstream_id, destination_id):
        """Get the connection of an eventstream destination
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            destination_id (str): The ID of the destination
        Returns:
            dict: The eventstream destination connection
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/destinations/{destination_id}/connection"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting eventstream destination connection", return_format="json")
        return item_dict

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/sources/{sourceId}
    def get_eventstream_source(self, workspace_id, eventstream_id, source_id):
        """Get the source of an eventstream
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            source_id (str): The ID of the source
        Returns:
            dict: The eventstream source
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/sources/{source_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting eventstream source", return_format="json")
        return item_dict
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/sources/{sourceId}/connection
    def get_eventstream_source_connection(self, workspace_id, eventstream_id, source_id):
        """Get the connection of an eventstream source
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            source_id (str): The ID of the source
        Returns:
            dict: The eventstream source connection
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/sources/{source_id}/connection"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting eventstream source connection", return_format="json")
        return item_dict


    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/topology
    def get_eventstream_topology(self, workspace_id, eventstream_id):
        """Get the topology of an eventstream
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
        Returns:
            dict: The eventstream topology
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/topology"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting eventstream topology", return_format="json")
        return item_dict
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/pause
    def pause_eventstream(self, workspace_id, eventstream_id):
        """Pause an eventstream
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/pause"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error pausing eventstream",
                                         return_format="response")

        return response.status_code
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/destinations/{destinationId}/pause
    def pause_eventstream_destination(self, workspace_id, eventstream_id, destination_id):
        """Pause an eventstream destination
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            destination_id (str): The ID of the destination
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/destinations/{destination_id}/pause"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error pausing eventstream destination",
                                         return_format="response")

        return response.status_code
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/sources/{sourceId}/pause
    def pause_eventstream_source(self, workspace_id, eventstream_id, source_id):
        """Pause an eventstream source
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            source_id (str): The ID of the source
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/sources/{source_id}/pause"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 429], error_message="Error pausing eventstream source",
                                         return_format="response")

        return response.status_code

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/resume
    def resume_eventstream(self, workspace_id, eventstream_id, start_type, custom_start_date_time = None):
        """Resume an eventstream
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            start_type (str): The start type of the eventstream
            custom_start_date_time (str): The custom start date time of the eventstream
        Returns:
            dict: The operation result or response value
        """

        body = {
            "startType": start_type
        }

        if custom_start_date_time is not None:
            body["customStartDateTime"] = custom_start_date_time

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/resume"

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429], error_message="Error resuming eventstream",
                                         return_format="response")

        return response.status_code

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/destinations/{destinationId}/resume
    def resume_eventstream_destination(self, workspace_id, eventstream_id, destination_id, start_type, custom_start_date_time = None):
        """Resume an eventstream destination
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            destination_id (str): The ID of the destination
            start_type (str): The start type of the eventstream destination
            custom_start_date_time (str): The custom start date time of the eventstream destination
        Returns:
            dict: The operation result or response value
        """
        body = {
            "startType": start_type
        }

        if custom_start_date_time is not None:
            body["customStartDateTime"] = custom_start_date_time

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/destinations/{destination_id}/resume"

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429], error_message="Error resuming eventstream destination",
                                         return_format="response")

        return response.status_code

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/sources/{sourceId}/resume
    def resume_eventstream_source(self, workspace_id, eventstream_id, source_id, start_type, custom_start_date_time = None):
        """Resume an eventstream source
        Args:
            workspace_id (str): The ID of the workspace
            eventstream_id (str): The ID of the eventstream
            source_id (str): The ID of the source
            start_type (str): The start type of the eventstream source
            custom_start_date_time (str): The custom start date time of the eventstream source
        Returns:
            dict: The operation result or response value
        """
        body = {
            "startType": start_type
        }

        if custom_start_date_time is not None:
            body["customStartDateTime"] = custom_start_date_time

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventstreams/{eventstream_id}/sources/{source_id}/resume"

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429], error_message="Error resuming eventstream source",
                                         return_format="response")

        return response.status_code

    # graphqlapis

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/GraphQLApis
    def create_graphql_api(self, workspace_id, display_name, description = None):
        """Create a graphql api in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the graphql api
            description (str): The description of the graphql api
        Returns:
            dict: The created graphql api
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "GraphQLApis",
                                description = description)
    
    def delete_graphql_api(self, workspace_id, graphql_api_id):
        """Delete a graphql api from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            graphql_api_id (str): The ID of the graphql api
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, graphql_api_id, type="GraphQLApis")
    
    def get_graphql_api(self, workspace_id, graphql_api_id = None, graphql_api_name = None):
        """Get a graphql api from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            graphql_api_id (str): The ID of the graphql api
            graphql_api_name (str): The name of the graphql api
        Returns:
            dict: The graphql api
        """
        from msfabricpysdkcore.otheritems import GraphQLApi
        if graphql_api_id is None and graphql_api_name is not None:
            graphql_apis = self.list_graphql_apis(workspace_id)
            graphql_apis = [ga for ga in graphql_apis if ga.display_name == graphql_api_name]
            if len(graphql_apis) == 0:
                raise Exception(f"Graphql api with name {graphql_api_name} not found")
            graphql_api_id = graphql_apis[0].id
        if graphql_api_id is None:
            raise Exception("graphql_api_id or the graphql_api_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/GraphQLApis/{graphql_api_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting graphql api", return_format="json")
        graphql = GraphQLApi.from_dict(item_dict, core_client=self)
        return graphql
    
    def list_graphql_apis(self, workspace_id, with_properties = False):
        """List graphql apis in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of graphql apis
        """
        return self.list_items(workspace_id=workspace_id, type="GraphQLApis", with_properties=with_properties)

    def update_graphql_api(self, workspace_id, graphql_api_id, display_name = None, description = None, return_item=False):
        """Update a graphql api in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            graphql_api_id (str): The ID of the graphql api
            display_name (str): The display name of the graphql api
            description (str): The description of the graphql api
        Returns:
            dict: The updated graphql api
        """
        return self.update_item(workspace_id, graphql_api_id, display_name = display_name, description = description, 
                                type= "GraphQLApis", return_item=return_item)

    # kqlDashboard
    def create_kql_dashboard(self, workspace_id, display_name, description = None):
        """Create a kql dashboard in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the kql dashboard
            description (str): The description of the kql dashboard
        Returns:
            dict: The created kql dashboard
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "kqlDashboards",
                                description = description)
    
    def delete_kql_dashboard(self, workspace_id, kql_dashboard_id):
        """Delete a kql dashboard from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_dashboard_id (str): The ID of the kql dashboard
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, kql_dashboard_id, type="kqlDashboards")
    
    def get_kql_dashboard(self, workspace_id, kql_dashboard_id = None, kql_dashboard_name = None):
        """Get a kql dashboard from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_dashboard_id (str): The ID of the kql dashboard
            kql_dashboard_name (str): The name of the kql dashboard
        Returns:
            KQLDashboard: The kql dashboard object
        """
        
        from msfabricpysdkcore.otheritems import KQLDashboard
        if kql_dashboard_id is None and kql_dashboard_name is not None:
            kql_dashboards = self.list_kql_dashboards(workspace_id)
            kql_dashboards = [kd for kd in kql_dashboards if kd.display_name == kql_dashboard_name]
            if len(kql_dashboards) == 0:
                raise Exception(f"Kql dashboard with name {kql_dashboard_name} not found")
            kql_dashboard_id = kql_dashboards[0].id
        if kql_dashboard_id is None:
            raise Exception("kql_dashboard_id or the kql_dashboard_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/kqlDashboards/{kql_dashboard_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting kql dashboard", return_format="json")
        kqldashboard = KQLDashboard.from_dict(item_dict, core_client=self)
        kqldashboard.get_definition()
        return kqldashboard

    def get_kql_dashboard_definition(self, workspace_id, kql_dashboard_id, format=None):
        """Get the definition of a kql dashboard
        Args:
            workspace_id (str): The ID of the workspace
            kql_dashboard_id (str): The ID of the kql dashboard
        Returns:
            dict: The definition of the kql dashboard
        """
        return self.get_item_definition(workspace_id, kql_dashboard_id, type="kqlDashboards", format=format)


    def list_kql_dashboards(self, workspace_id, with_properties = False):
        """List kql dashboards in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of kql dashboards
        """
        return self.list_items(workspace_id=workspace_id, type="kqlDashboards", with_properties=with_properties)
    
    def update_kql_dashboard(self, workspace_id, kql_dashboard_id, display_name = None, description = None, return_item=False):
        """Update a kql dashboard in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            kql_dashboard_id (str): The ID of the kql dashboard
            display_name (str): The display name of the kql dashboard
            description (str): The description of the kql dashboard
        Returns:
            dict: The updated kql dashboard
        """
        return self.update_item(workspace_id, kql_dashboard_id, display_name = display_name,
                                description = description, type= "kqlDashboards", return_item=return_item)
    
    def update_kql_dashboard_definition(self, workspace_id, kql_dashboard_id, definition, update_metadata = None):
        """Update the definition of a kql dashboard
        Args:
            workspace_id (str): The ID of the workspace
            kql_dashboard_id (str): The ID of the kql dashboard
            definition (dict): The definition of the kql dashboard
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated definition of the kql dashboard
        """
        return self.update_item_definition(workspace_id, kql_dashboard_id,
                                           type="kqlDashboards", definition=definition, update_metadata=update_metadata)

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
        kqldb = KQLDatabase.from_dict(item_dict, core_client=self)
        kqldb.get_definition()
        return kqldb
    
    def get_kql_database_definition(self, workspace_id, kql_database_id, format=None):
        """Get the definition of a kql database
        Args:
            workspace_id (str): The ID of the workspace
            kql_database_id (str): The ID of the kql database
            format (str): The format of the definition
        Returns:
            dict: The definition of the kql database
        """
        return self.get_item_definition(workspace_id, kql_database_id, type="kqlDatabases", format=format)

    def list_kql_databases(self, workspace_id, with_properties = False):
        """List kql databases in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of kql databases"""
        return self.list_items(workspace_id=workspace_id, type="kqlDatabases", with_properties=with_properties)
    
    def update_kql_database(self, workspace_id, kql_database_id, display_name = None, description = None, return_item=False):
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

    def update_kql_database_definition(self, workspace_id, kql_database_id, definition, update_metadata = None):
        """Update the definition of a kql database
        Args:
            workspace_id (str): The ID of the workspace
            kql_database_id (str): The ID of the kql database
            definition (dict): The definition of the kql database
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated definition of the kql database
        """
        return self.update_item_definition(workspace_id, kql_database_id,
                                           type="kqlDatabases", definition=definition, update_metadata=update_metadata)

    # kqlQuerysets

    def create_kql_queryset(self, workspace_id, display_name, description = None, definition = None):
        """Create a kql queryset in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the kql queryset
            description (str): The description of the kql queryset
            definition (dict): The definition of the kql queryset
        Returns:
            dict: The created kql queryset
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "kqlQuerysets",
                                description = description,
                                definition = definition)


        
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
        
        kql =  KQLQueryset.from_dict(item_dict, core_client=self)
        kql.get_definition()
        return kql
    
    def get_kql_queryset_definition(self, workspace_id, kql_queryset_id, format=None):
        """Get the definition of a kql queryset
        Args:
            workspace_id (str): The ID of the workspace
            kql_queryset_id (str): The ID of the kql queryset
        Returns:
            dict: The definition of the kql queryset
        """
        return self.get_item_definition(workspace_id, kql_queryset_id, type="kqlQuerysets", format=format)

    def list_kql_querysets(self, workspace_id, with_properties = False):
        """List kql querysets in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of kql querysets
        """
        return self.list_items(workspace_id=workspace_id, type="kqlQuerysets", with_properties=with_properties)
    
    def update_kql_queryset(self, workspace_id, kql_queryset_id, display_name = None, description = None, return_item=False):
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

    def update_kql_queryset_definition(self, workspace_id, kql_queryset_id, definition, update_metadata = None):
        """Update the definition of a kql queryset
        Args:
            workspace_id (str): The ID of the workspace
            kql_queryset_id (str): The ID of the kql queryset
            definition (dict): The definition of the kql queryset
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated definition of the kql queryset
        """
        return self.update_item_definition(workspace_id, kql_queryset_id,
                                           type="kqlQuerysets", definition=definition, update_metadata=update_metadata)


    # mirrored azure databricks catalog
    def create_mirrored_azure_databricks_catalog(self, workspace_id, display_name, description = None, definition = None,creation_payload = None, folder_id = None):
        """Create a mirrored azure databricks catalog in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the mirrored azure databricks catalog
            description (str): The description of the mirrored azure databricks catalog
            creation_payload (dict): The creation payload
            folder_id (str): The folder ID to create the item in
        Returns:
            dict: The created mirrored azure databricks catalog
        """
        if creation_payload is None and definition is None:
            raise Exception("Either creation_payload or definition must be provided")
        if creation_payload is not None and definition is not None:
            raise Exception("Only one of creation_payload or definition can be provided")
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "mirroredAzureDatabricksCatalogs",
                                description = description,
                                definition = definition,
                                creation_payload = creation_payload,
                                folder_id = folder_id)
    
    def delete_mirrored_azure_databricks_catalog(self, workspace_id, mirrored_azure_databricks_catalog_id):
        """Delete a mirrored azure databricks catalog from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_azure_databricks_catalog_id (str): The ID of the mirrored azure databricks catalog
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, mirrored_azure_databricks_catalog_id, type="mirroredAzureDatabricksCatalogs")
    
    def get_mirrored_azure_databricks_catalog(self, workspace_id, mirrored_azure_databricks_catalog_id = None,
                                                  mirrored_azure_databricks_catalog_name = None):
        """Get a mirrored azure databricks catalog from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_azure_databricks_catalog_id (str): The ID of the mirrored azure dat
            mirrored_azure_databricks_catalog_name (str): The name of the mirrored azure databricks catalog
        Returns:
            MirroredAzureDatabricksCatalog: The mirrored azure databricks catalog object
        """
        from msfabricpysdkcore.otheritems import MirroredAzureDatabricksCatalog
        if mirrored_azure_databricks_catalog_id is None and mirrored_azure_databricks_catalog_name is not None:
            mirrored_azure_databricks_catalogs = self.list_mirrored_azure_databricks_catalogs(workspace_id)
            mirrored_azure_databricks_catalogs = [madc for madc in mirrored_azure_databricks_catalogs if madc.display_name == mirrored_azure_databricks_catalog_name]
            if len(mirrored_azure_databricks_catalogs) == 0:
                raise Exception(f"Mirrored azure databricks catalog with name {mirrored_azure_databricks_catalog_name} not found")
            mirrored_azure_databricks_catalog_id = mirrored_azure_databricks_catalogs[0].id
        if mirrored_azure_databricks_catalog_id is None:
            raise Exception("mirrored_azure_databricks_catalog_id or the mirrored_azure_databricks_catalog_name is required")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredAzureDatabricksCatalogs/{mirrored_azure_databricks_catalog_id}"
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting mirrored azure databricks catalog", return_format="json")
        madc = MirroredAzureDatabricksCatalog.from_dict(item_dict, core_client=self)
        madc.get_definition()
        return madc

    def get_mirrored_azure_databricks_catalog_definition(self, workspace_id, mirrored_azure_databricks_catalog_id, format=None):
        """Get the definition of a mirrored azure databricks catalog
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_azure_databricks_catalog_id (str): The ID of the mirrored azure databricks catalog
            format (str): The format of the definition
        Returns:
            dict: The definition of the mirrored azure databricks catalog
        """
        return self.get_item_definition(workspace_id, mirrored_azure_databricks_catalog_id, type="mirroredAzureDatabricksCatalogs", format=format)
    
    def list_mirrored_azure_databricks_catalogs(self, workspace_id, with_properties = False):
        """List mirrored azure databricks catalogs in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of mirrored azure databricks catalogs
        """
        return self.list_items(workspace_id=workspace_id, type="mirroredAzureDatabricksCatalogs", with_properties=with_properties)
    
    def update_mirrored_azure_databricks_catalog(self, workspace_id, mirrored_azure_databricks_catalog_id, display_name = None, description = None, return_item=False):
        """Update a mirrored azure databricks catalog in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_azure_databricks_catalog_id (str): The ID of the mirrored azure databricks catalog
            display_name (str): The display name of the mirrored azure databricks catalog
            description (str): The description of the mirrored azure databricks catalog
        Returns:
            dict: The updated mirrored azure databricks catalog
        """
        return self.update_item(workspace_id, mirrored_azure_databricks_catalog_id, display_name = display_name,
                                description = description, type= "mirroredAzureDatabricksCatalogs", return_item=return_item)
    
    def update_mirrored_azure_databricks_catalog_definition(self, workspace_id, mirrored_azure_databricks_catalog_id, definition, update_metadata = None):
        """Update the definition of a mirrored azure databricks catalog
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_azure_databricks_catalog_id (str): The ID of the mirrored azure databricks catalog
            definition (dict): The definition of the mirrored azure databricks catalog
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated definition of the mirrored azure databricks catalog
        """
        return self.update_item_definition(workspace_id, mirrored_azure_databricks_catalog_id,
                                           type="mirroredAzureDatabricksCatalogs", definition=definition, update_metadata=update_metadata)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mirroredAzureDatabricksCatalogs/{mirroredAzureDatabricksCatalogId}/refreshCatalogMetadata
    def refresh_mirrored_azure_databricks_catalog_metadata(self, workspace_id, mirrored_azure_databricks_catalog_id, wait_for_completion = False):
        """Refresh the metadata of a mirrored azure databricks catalog
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_azure_databricks_catalog_id (str): The ID of the mirrored azure databricks catalog
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredAzureDatabricksCatalogs/{mirrored_azure_databricks_catalog_id}/refreshCatalogMetadata"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                         error_message="Error refreshing mirrored azure databricks catalog metadata",
                                         return_format="response", wait_for_completion=wait_for_completion)

        return response.status_code
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/azuredatabricks/catalogs?databricksWorkspaceConnectionId={databricksWorkspaceConnectionId}
    def discover_mirrored_azure_databricks_catalogs(self, workspace_id, databricks_workspace_connection_id, max_results = None):
        """List mirrored azure databricks catalogs by connection
        Args:
            workspace_id (str): The ID of the workspace
            databricks_workspace_connection_id (str): The ID of the databricks workspace connection
            max_results (int): The maximum number of results to return
        Returns:
            list: The list of mirrored azure databricks catalogs
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/azuredatabricks/catalogs?databricksWorkspaceConnectionId={databricks_workspace_connection_id}"
        
        if max_results is not None:
            url += f"&maxResults={max_results}"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                        error_message="Error listing mirrored azure databricks catalogs by connection", return_format="value_json", paging=True)

        return items
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/azuredatabricks/catalogs/{catalogName}/schemas?databricksWorkspaceConnectionId={databricksWorkspaceConnectionId}
    def discover_mirrored_azure_databricks_catalog_schemas(self, workspace_id, catalog_name, databricks_workspace_connection_id, max_results = None):
        """List mirrored azure databricks catalog schemas by connection
        Args:
            workspace_id (str): The ID of the workspace
            catalog_name (str): The name of the catalog
            databricks_workspace_connection_id (str): The ID of the databricks workspace connection
            max_results (int): The maximum number of results to return
        Returns:
            list: The list of mirrored azure databricks catalog schemas
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/azuredatabricks/catalogs/{catalog_name}/schemas?databricksWorkspaceConnectionId={databricks_workspace_connection_id}"
        
        if max_results is not None:
            url += f"&maxResults={max_results}"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                        error_message="Error listing mirrored azure databricks catalog schemas by connection",
                                          return_format="value_json", paging=True)

        return items
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/azuredatabricks/catalogs/{catalogName}/schemas/{schemaName}/tables?databricksWorkspaceConnectionId={databricksWorkspaceConnectionId}
    def discover_mirrored_azure_databricks_catalog_tables(self, workspace_id, catalog_name, schema_name, databricks_workspace_connection_id, max_results = None):
        """List mirrored azure databricks catalog tables by connection
        Args:
            workspace_id (str): The ID of the workspace
            catalog_name (str): The name of the catalog
            schema_name (str): The name of the schema
            databricks_workspace_connection_id (str): The ID of the databricks workspace connection
            max_results (int): The maximum number of results to return
        Returns:
            list: The list of mirrored azure databricks catalog tables
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/azuredatabricks/catalogs/{catalog_name}/schemas/{schema_name}/tables?databricksWorkspaceConnectionId={databricks_workspace_connection_id}"
        
        if max_results is not None:
            url += f"&maxResults={max_results}"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                        error_message="Error listing mirrored azure databricks catalog tables by connection", 
                                        return_format="value_json", paging=True)

        return items

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
    
    def create_lakehouse(self, workspace_id, display_name, description = None, creation_payload = None):
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
                                description = description,
                                creation_payload = creation_payload)
    
    
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

    def update_lakehouse(self, workspace_id, lakehouse_id, display_name = None, description = None, return_item=False):
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
    
    # lakehouse livy sessions

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livySessions
    def list_lakehouse_livy_sessions(self, workspace_id, lakehouse_id):
        """List all livy sessions for a lakehouse
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
        Returns:
            list: The list of livy sessions
        """
        return self.list_livy_sessions(workspace_id=workspace_id, item_id=lakehouse_id, item_type="lakehouses")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livySessions/{livyId}
    def get_lakehouse_livy_session(self, workspace_id, lakehouse_id, livy_id):
        """Get a livy session for a lakehouse
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            livy_id (str): The ID of the livy session
        Returns:
            dict: The livy session
        """
        return self.get_livy_session(workspace_id=workspace_id,
                                     item_id=lakehouse_id, item_type="lakehouses", livy_id=livy_id)

    # Livy sessions
    
    
    def get_livy_session(self, workspace_id, item_id, item_type = None, livy_id = None):
        """Get a livy session for a lakehouse
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            item_type (str): The type of the item
            livy_id (str): The ID of the livy session
        Returns:
            dict: The livy session
        """

        if "lakehouse" in item_type.lower():
            item_type = "lakehouses"
        elif "notebook" in item_type.lower():
            item_type = "notebooks"
        elif "sparkjobdef" in item_type.lower() or "sjd" in item_type.lower():
            item_type = "sparkJobDefinitions"

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{item_type}/{item_id}/livySessions/{livy_id}"
        
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting livy session", return_format="json")
        return item_dict

    def list_livy_sessions(self, workspace_id, item_id = None, item_type = None):
        """List all livy sessions for a lakehouse
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            item_type (str): The type of the item
        Returns:
            list: The list of livy sessions
        """
        if item_id is None:
            item_type = "spark"
        elif "lakehouse" in item_type.lower():
            item_type = "lakehouses"
        elif "notebook" in item_type.lower():
            item_type = "notebooks"
        elif "sparkjobdef" in item_type.lower() or "sjd" in item_type.lower():
            item_type = "sparkJobDefinitions"
        
        if item_id is None:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/livySessions"
        else:
            url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/{item_type}/{item_id}/livySessions"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                      error_message="Error listing livy sessions", return_format="value_json", paging=True)

        return items

    # Materialized view

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/jobs/RefreshMaterializedLakeViews/schedules
    def create_refresh_materialized_lake_view_schedule(self, workspace_id, lakehouse_id, enabled, configuration):
        """Create a refresh materialized lake view schedule
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            enabled (bool): Whether the schedule is enabled
            configuration (dict): The configuration of the schedule
        Returns:
            dict: The created schedule
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/RefreshMaterializedLakeViews/schedules"

        body = {
                "enabled": enabled,
                "configuration": configuration
              }
        
        item_dict = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 201, 429],
                                         error_message="Error creating refresh materialized lake view schedule", return_format="json")

        return item_dict
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/jobs/RefreshMaterializedLakeViews/schedules/{scheduleId}
    def delete_refresh_materialized_lake_view_schedule(self, workspace_id, lakehouse_id, schedule_id):
        """Delete a refresh materialized lake view schedule
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            schedule_id (str): The ID of the schedule
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/RefreshMaterializedLakeViews/schedules/{schedule_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 204, 429],
                                        error_message="Error deleting refresh materialized lake view schedule", return_format="response")

        return response.status_code

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/jobs/instances?jobType={jobType}
    def run_on_demand_refresh_materialized_lake_view(self, workspace_id, lakehouse_id, job_type="RefreshMaterializedLakeViews"):
        """Run refresh materialized lake view
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            job_type (str): The job type
        Returns:
            dict: The operation result or response value
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/instances?jobType={job_type}"

    
        response = self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                                        error_message="Error running refresh materialized lake view",
                                                        return_format="response")

        return response

    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/jobs/RefreshMaterializedLakeViews/schedules/{scheduleId}
    def update_refresh_materialized_lake_view_schedule(self, workspace_id, lakehouse_id, schedule_id, enabled, configuration):
        """Update a refresh materialized lake view schedule
        Args:
            workspace_id (str): The ID of the workspace
            lakehouse_id (str): The ID of the lakehouse
            schedule_id (str): The ID of the schedule
            enabled (bool): Whether the schedule is enabled
            configuration (dict): The configuration of the schedule
        Returns:
            dict: The updated schedule
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/RefreshMaterializedLakeViews/schedules/{schedule_id}"

        body = {}
        body["enabled"] = enabled
        body["configuration"] = configuration

        item_dict = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                         error_message="Error updating refresh materialized lake view schedule", return_format="json")

        return item_dict

    # mirrored_database

    def create_mirrored_database(self, workspace_id, display_name, description = None, definition = None):
        """Create a mirrored database in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the mirrored database
            description (str): The description of the mirrored database
        Returns:
            dict: The created mirrored database
        """
        return self.create_item(workspace_id = workspace_id,
                                display_name = display_name,
                                type = "mirroredDatabases",
                                description = description,
                                definition=definition)
    
    def delete_mirrored_database(self, workspace_id, mirrored_database_id):
        """Delete a mirrored database from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, mirrored_database_id, type="mirroredDatabases")
    
    def get_mirrored_database(self, workspace_id, mirrored_database_id = None, mirrored_database_name = None):
        """Get a mirrored database from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
            mirrored_database_name (str): The name of the mirrored database
        Returns:
            MirroredDatabase: The mirrored database object
        """
        from msfabricpysdkcore.otheritems import MirroredDatabase

        if mirrored_database_id is None and mirrored_database_name is not None:
            mirrored_databases = self.list_mirrored_databases(workspace_id)
            mirrored_databases = [md for md in mirrored_databases if md.display_name == mirrored_database_name]
            if len(mirrored_databases) == 0:
                raise Exception(f"Mirrored database with name {mirrored_database_name} not found")
            mirrored_database_id = mirrored_databases[0].id
        
        if mirrored_database_id is None:
            raise Exception("mirrored_database_id or the mirrored_database_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredDatabases/{mirrored_database_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting mirrored database", return_format="json")
        mirrored_db = MirroredDatabase.from_dict(item_dict, core_client=self)
        return mirrored_db

    def get_mirrored_database_definition(self, workspace_id, mirrored_database_id):
        """Get the definition of a mirrored database
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
        Returns:
            dict: The definition of the mirrored database
        """
        return self.get_item_definition(workspace_id, mirrored_database_id, type="mirroredDatabases")

    def list_mirrored_databases(self, workspace_id, with_properties = False):
        """List mirrored databases in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of mirrored databases
        """
        return self.list_items(workspace_id=workspace_id, type="mirroredDatabases", with_properties=with_properties)
    
    def update_mirrored_database(self, workspace_id, mirrored_database_id, display_name = None, description = None, return_item=False): 
        """Update a mirrored database in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
            display_name (str): The display name of the mirrored database
            description (str): The description of the mirrored database
        Returns:
            dict: The updated mirrored database
        """
        return self.update_item(workspace_id, mirrored_database_id, display_name = display_name, description = description,
                                type="mirroredDatabases", return_item=return_item)
    
    def update_mirrored_database_definition(self, workspace_id, mirrored_database_id, definition):
        """Update the definition of a mirrored database
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
            definition (dict): The definition of the mirrored database
        Returns:
            dict: The updated definition of the mirrored database
        """
        return self.update_item_definition(workspace_id, mirrored_database_id,
                                           type="mirroredDatabases", definition=definition)
    
    
    def get_mirroring_status(self, workspace_id, mirrored_database_id):
        """Get the mirroring status of a mirrored database
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
        Returns:
            dict: The mirroring status of the mirrored database
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredDatabases/{mirrored_database_id}/getMirroringStatus"

        return self.calling_routine(url, operation="POST", response_codes=[200, 429],
                                    error_message="Error getting mirroring status", return_format="json")

    def get_tables_mirroring_status(self, workspace_id, mirrored_database_id):
        """Get the tables mirroring status of a mirrored database
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
        Returns:
            dict: The tables mirroring status of the mirrored database
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredDatabases/{mirrored_database_id}/getTablesMirroringStatus"

        return self.calling_routine(url, operation="POST", response_codes=[200, 429],
                                    error_message="Error getting tables mirroring status", return_format="json")

    def start_mirroring(self, workspace_id, mirrored_database_id):
        """Start mirroring of a mirrored database
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
        Returns:
            dict: The operation result
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredDatabases/{mirrored_database_id}/startMirroring"

        return self.calling_routine(url, operation="POST", response_codes=[200, 429],
                                    error_message="Error starting mirroring", return_format="response")
    
    def stop_mirroring(self, workspace_id, mirrored_database_id):
        """Stop mirroring of a mirrored database
        Args:
            workspace_id (str): The ID of the workspace
            mirrored_database_id (str): The ID of the mirrored database
        Returns:
            dict: The operation result
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mirroredDatabases/{mirrored_database_id}/stopMirroring"

        return self.calling_routine(url, operation="POST", response_codes=[200, 429],
                                    error_message="Error stopping mirroring", return_format="response")


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
    
    def update_ml_experiment(self, workspace_id, ml_experiment_id, display_name = None, description = None, return_item=False):
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
    
    def update_ml_model(self, workspace_id, ml_model_id, display_name = None, description = None, return_item=False):
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

    # MLmodel endpoint

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions/{name}/activate
    def activate_ml_model_endpoint_version(self, workspace_id, model_id, name, wait_for_completion = False):
        """Activate an ml model endpoint version
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            name (str): The name of the endpoint version    
        Returns:
            dict: The activated endpoint version
        """

        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions/{name}/activate"
        return self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                     error_message="Error activating ml model endpoint version", return_format="json", wait_for_completion=wait_for_completion)

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions/deactivateAll
    def deactivate_all_ml_model_endpoint_versions(self, workspace_id, model_id, wait_for_completion = False):
        """Deactivate all ml model endpoint versions
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
        Returns:
            Response: The operation result
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions/deactivateAll"
        return self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                     error_message="Error deactivating all ml model endpoint versions", return_format="response", wait_for_completion=wait_for_completion)

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions/{name}/deactivate
    def deactivate_ml_model_endpoint_version(self, workspace_id, model_id, name, wait_for_completion = False):
        """Deactivate an ml model endpoint version
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            name (str): The name of the endpoint version    
        Returns:
            Response: The operation result
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions/{name}/deactivate"
        return self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                     error_message="Error deactivating ml model endpoint version", return_format="response", wait_for_completion=wait_for_completion)
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint
    def get_ml_model_endpoint(self, workspace_id, model_id):
        """Get the ml model endpoint
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
        Returns:
            dict: The ml model endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint"
        return self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error getting ml model endpoint", return_format="json")

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions/{name}
    def get_ml_model_endpoint_version(self, workspace_id, model_id, name):
        """Get an ml model endpoint version
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            name (str): The name of the endpoint version    
        Returns:
            dict: The ml model endpoint version
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions/{name}"
        return self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error getting ml model endpoint version", return_format="json")

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions?continuationToken={continuationToken}
    def list_ml_model_endpoint_versions(self, workspace_id, model_id):
        """List all ml model endpoint versions
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
        Returns:
            list: The list of ml model endpoint versions
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions"
        return self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing ml model endpoint versions", return_format="value_json", paging=True)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlModels/{modelId}/endpoint/score
    def score_ml_model_endpoint(self, workspace_id, model_id, inputs, format_type = None, orientation = None):
        """Score an ml model endpoint
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            inputs (list): The inputs to score
            format_type (str): The format type
            orientation (str): The orientation
        Returns:
            dict: The scoring result
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlModels/{model_id}/endpoint/score"

        body = {
                "inputs": inputs
              }

        if format_type:
            body["formatType"] = format_type
        if orientation:
            body["orientation"] = orientation

        return self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                     error_message="Error scoring ml model endpoint", return_format="json")

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions/{name}/score
    def score_ml_model_endpoint_version(self, workspace_id, model_id, name, inputs, format_type = None, orientation = None):
        """Score an ml model endpoint version
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            name (str): The name of the endpoint version    
            inputs (list): The inputs to score
            format_type (str): The format type
            orientation (str): The orientation
        Returns:
            dict: The scoring result
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions/{name}/score"

        body = {
                "inputs": inputs
              }

        if format_type:
            body["formatType"] = format_type
        if orientation:
            body["orientation"] = orientation

        return self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                     error_message="Error scoring ml model endpoint version", return_format="json")                                    

    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint
    def update_ml_model_endpoint(self, workspace_id, model_id, default_version_assignment_behavior, default_version_name):
        """Update an ml model endpoint
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            default_version_assignment_behavior (str): The default version assignment behavior
            default_version_name (str): The default version name
        Returns:
            dict: The updated endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint"

        body = {
                "defaultVersionAssignmentBehavior": default_version_assignment_behavior,
                "defaultVersionName": default_version_name
              }

        return self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                     error_message="Error updating ml model endpoint", return_format="json")


    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mlmodels/{modelId}/endpoint/versions/{name}
    def update_ml_model_endpoint_version(self, workspace_id, model_id, name, scale_rule):
        """Update an ml model endpoint version
        Args:
            workspace_id (str): The ID of the workspace
            model_id (str): The ID of the ml model
            name (str): The name of the endpoint version    
            scale_rule (str): The scale rule
        Returns:
            dict: The updated endpoint version
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mlmodels/{model_id}/endpoint/versions/{name}"

        body = {
                "scaleRule": scale_rule
              }

        return self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                     error_message="Error updating ml model endpoint version", return_format="json")



    # Maps
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps
    def create_map(self, workspace_id, display_name, definition = None, description = None, folder_id = None):
        """Create a map in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the map
            definition (dict): The definition of the map
            description (str): The description of the map
            folder_id (str): The ID of the folder to create the map in
        Returns:
            Map: The created map object
        """
        return self.create_item(workspace_id=workspace_id,
                                display_name = display_name,
                                type = "Maps",
                                definition = definition,
                                description = description, folder_id=folder_id)
    
    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps/{MapId}
    def delete_map(self, workspace_id, map_id):
        """Delete a map from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            map_id (str): The ID of the map
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, item_id=map_id, type="Maps")
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps/{MapId}
    def get_map(self, workspace_id, map_id = None, map_name = None):
        """Get a map from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            map_id (str): The ID of the map
            map_name (str): The name of the map
        Returns:
            Map: The map object
        """
        from msfabricpysdkcore.otheritems import Map

        if map_id is None and map_name is not None:
            maps = self.list_maps(workspace_id)
            maps_filtered = [m for m in maps if m.display_name == map_name]
            if len(maps_filtered) == 0:
                raise Exception(f"Map with name {map_name} not found")
            map_id = maps_filtered[0].id
        elif map_id is None:
            raise Exception("map_id or the map_name is required")
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/Maps/{map_id}"
        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting map", return_format="json")
        map_obj = Map.from_dict(item_dict, core_client=self)
        map_obj.get_definition()
        return map_obj
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps/{MapId}/getDefinition
    def get_map_definition(self, workspace_id, map_id, format = None):
        """Get the definition of a map
        Args:
            workspace_id (str): The ID of the workspace
            map_id (str): The ID of the map
            format (str): The format of the definition
        Returns:
            dict: The map definition
        """
        return self.get_item_definition(workspace_id, map_id, type="Maps", format=format)
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps
    def list_maps(self, workspace_id, with_properties = False):
        """List maps in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of maps
        """
        return self.list_items(workspace_id, type="Maps", with_properties=with_properties)
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps/{MapId}
    def update_map(self, workspace_id, map_id, display_name = None, description = None, return_item=False):
        """Update a map in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            map_id (str): The ID of the map
            display_name (str): The display name of the map
            description (str): The description of the map
            return_item (bool): Whether to return the item object
        Returns:
            dict: The updated map or Map object if return_item is True
        """
        return self.update_item(workspace_id, item_id=map_id, display_name=display_name, description=description, type="Maps",
                                return_item=return_item)
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Maps/{MapId}/updateDefinition
    def update_map_definition(self, workspace_id, map_id, definition, update_metadata = None):
        """Update the definition of a map
        Args:
            workspace_id (str): The ID of the workspace
            map_id (str): The ID of the map
            definition (dict): The definition of the map
            update_metadata (bool): Whether to update the metadata
        Returns:
            dict: The updated map definition
        """
        return self.update_item_definition(workspace_id, map_id, type="Maps", definition=definition, update_metadata=update_metadata)

    # mounted data factory
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mountedDataFactories

    def create_mounted_data_factory(self, workspace_id, display_name, description = None, definition = None):
        """Create a mounted data factory in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the mounted data factory
            description (str): The description of the mounted data factory
            definition (dict): The definition of the mounted data factory
        Returns:
            dict: The created mounted data factory
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "mountedDataFactories",
                                description = description, definition = definition)
    
    def delete_mounted_data_factory(self, workspace_id, mounted_data_factory_id):
        """Delete a mounted data factory from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mounted_data_factory_id (str): The ID of the mounted data factory
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, mounted_data_factory_id, type="mountedDataFactories")

    def get_mounted_data_factory(self, workspace_id, mounted_data_factory_id = None, mounted_data_factory_name = None):
        """Get a mounted data factory from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mounted_data_factory_id (str): The ID of the mounted data factory
            mounted_data_factory_name (str): The name of the mounted data factory
        Returns:
            MountedDataFactory: The mounted data factory object
        """
        from msfabricpysdkcore.otheritems import MountedDataFactory
        if mounted_data_factory_id is None and mounted_data_factory_name is not None:
            mounted_data_factories = self.list_mounted_data_factories(workspace_id)
            mounted_data_factories = [mdf for mdf in mounted_data_factories if mdf.display_name == mounted_data_factory_name]
            if len(mounted_data_factories) == 0:
                raise Exception(f"Mounted data factory with name {mounted_data_factory_name} not found")
            mounted_data_factory_id = mounted_data_factories[0].id
        if mounted_data_factory_id is None:
            raise Exception("mounted_data_factory_id or the mounted_data_factory_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/mountedDataFactories/{mounted_data_factory_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting mounted data factory", return_format="json")
        
        mdf = MountedDataFactory.from_dict(item_dict, core_client=self)
        mdf.get_definition()
        return mdf
    
    def get_mounted_data_factory_definition(self, workspace_id, mounted_data_factory_id, format = None):
        """Get the definition of a mounted data factory
        Args:
            workspace_id (str): The ID of the workspace
            mounted_data_factory_id (str): The ID of the mounted data factory
            format (str): The format of the definition
        Returns:
            dict: The definition of the mounted data factory
        """
        return self.get_item_definition(workspace_id, mounted_data_factory_id, type="mountedDataFactories", format=format)

    def list_mounted_data_factories(self, workspace_id, with_properties = False):
        """List mounted data factories in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of mounted data factories
        """
        return self.list_items(workspace_id=workspace_id, type="mountedDataFactories", with_properties = with_properties)
    
    def update_mounted_data_factory(self, workspace_id, mounted_data_factory_id, display_name = None, description = None, return_item=False):
        """Update a mounted data factory in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            mounted_data_factory_id (str): The ID of the mounted data factory
            display_name (str): The display name of the mounted data factory
            description (str): The description of the mounted data factory
        Returns:
            dict: The updated mounted data factory
        """
        return self.update_item(workspace_id, mounted_data_factory_id, display_name = display_name, description = description,
                                type="mountedDataFactories", return_item=return_item)

    def update_mounted_data_factory_definition(self, workspace_id, mounted_data_factory_id, definition, update_metadata = None):
        """Update the definition of a mounted data factory
        Args:
            workspace_id (str): The ID of the workspace
            mounted_data_factory_id (str): The ID of the mounted data factory
            definition (dict): The definition of the mounted data factory
        Returns:
            dict: The updated definition of the mounted data factory
        """
        return self.update_item_definition(workspace_id, mounted_data_factory_id, definition, type="mountedDataFactories", update_metadata=update_metadata)

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
    
    def update_notebook(self, workspace_id, notebook_id, display_name = None, description = None, return_item=False):
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

    def get_notebook_livy_session(self, workspace_id, notebook_id, livy_id):
        """Get a livy session for a notebook
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
            livy_id (str): The ID of the livy session
        Returns:
            dict: The livy session
        """
        return self.get_livy_session(workspace_id=workspace_id, item_id=notebook_id, item_type="notebooks", livy_id=livy_id)
    
    def list_notebook_livy_sessions(self, workspace_id, notebook_id):
        """List all livy sessions for a notebook
        Args:
            workspace_id (str): The ID of the workspace
            notebook_id (str): The ID of the notebook
        Returns:
            list: The list of livy sessions
        """

        return self.list_livy_sessions(workspace_id=workspace_id, item_id=notebook_id, item_type="notebooks")

    # paginatedReports

    def list_paginated_reports(self, workspace_id):
        """List paginated reports in a workspace"""
        return self.list_items(workspace_id, type="paginatedReports")
    
    def update_paginated_report(self, workspace_id, paginated_report_id, display_name = None, description = None, return_item=False):
        """Update a paginated report in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            paginated_report_id (str): The ID of the paginated report
            display_name (str): The display name of the paginated report
            description (str): The description of the paginated report
        Returns:
            dict: The updated paginated report
        """
        return self.update_item(workspace_id, paginated_report_id, display_name = display_name, description = description,
                                type="paginatedReports", return_item=return_item)

    # reflex

    def create_reflex(self, workspace_id, display_name, description = None, definition = None):
        """Create a reflex in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the reflex
            description (str): The description of the reflex
            definition (dict): The definition of the reflex
        Returns:
            dict: The created reflex
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "reflexes", description = description, definition = definition)

    def delete_reflex(self, workspace_id, reflex_id):
        """Delete a reflex from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            reflex_id (str): The ID of the reflex
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, reflex_id, type="reflexes")
    
    def get_reflex(self, workspace_id, reflex_id = None, reflex_name = None):
        """Get a reflex from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            reflex_id (str): The ID of the reflex
            reflex_name (str): The name of the reflex
        Returns:
            Reflex: The reflex object
        """
        from msfabricpysdkcore.otheritems import Reflex
        if reflex_id is None and reflex_name is not None:
            reflexes = self.list_reflexes(workspace_id)
            reflexes = [rf for rf in reflexes if rf.display_name == reflex_name]
            if len(reflexes) == 0:
                raise Exception(f"Reflex with name {reflex_name} not found")
            reflex_id = reflexes[0].id
        if reflex_id is None:
            raise Exception("reflex_id or the reflex_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/reflexes/{reflex_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting reflex", return_format="json")
        
        refl = Reflex.from_dict(item_dict, core_client=self)
        refl.get_definition()
        return refl
    
    def get_reflex_definition(self, workspace_id, reflex_id, format = None):
        """Get the definition of a reflex
        Args:
            workspace_id (str): The ID of the workspace
            reflex_id (str): The ID of the reflex
            format (str): The format of the definition
        Returns:
            dict: The definition of the reflex
        """
        return self.get_item_definition(workspace_id, reflex_id, type="reflexes", format=format)

    def list_reflexes(self, workspace_id, with_properties = False):
        """List reflexes in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of reflexes
        """
        return self.list_items(workspace_id = workspace_id, type = "reflexes", with_properties = with_properties)
    
    def update_reflex(self, workspace_id, reflex_id, display_name = None, description = None, return_item=False):
        """Update a reflex in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            reflex_id (str): The ID of the reflex
            display_name (str): The display name of the reflex
            description (str): The description of the reflex
        Returns:
            dict: The updated reflex
        """
        return self.update_item(workspace_id, reflex_id, display_name = display_name, description = description,
                                type="reflexes", return_item=return_item)
    
    def update_reflex_definition(self, workspace_id, reflex_id, definition, update_metadata = None):
        """Update the definition of a reflex
        Args:
            workspace_id (str): The ID of the workspace
            reflex_id (str): The ID of the reflex
            definition (dict): The definition of the reflex
        Returns:
            dict: The updated reflex
        """
        return self.update_item_definition(workspace_id, reflex_id, definition, type="reflexes", update_metadata=update_metadata)
    
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

    def update_report(self, workspace_id, report_id, display_name = None, description = None, return_item=False):
        """Update a report in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            report_id (str): The ID of the report
            display_name (str): The display name of the report
            description (str): The description of the report
        Returns:
            dict: The updated report
        """
        return self.update_item(workspace_id, report_id, display_name = display_name, description = description,
                                type="reports", return_item=return_item)

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

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/semanticModels/{semanticModelId}/bindConnection
    def bind_semantic_model_connection(self, workspace_id, semantic_model_id, connection_binding):
        """Bind a connection to a semantic model
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
            connection_binding (dict): The connection binding
        Returns:
            dict: The updated semantic model
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/semanticModels/{semantic_model_id}/bindConnection"

        body = {
                "connectionBinding": connection_binding
              }

        return self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                     error_message="Error binding connection to semantic model", return_format="response")

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

    def delete_semantic_model(self, workspace_id, semantic_model_id):
        """Delete a semantic model from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, semantic_model_id, type="semanticModels")
    
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
    
    def list_semantic_models(self, workspace_id, with_properties = False):
        """List semantic models in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of semantic models
        """
        return self.list_items(workspace_id = workspace_id, type = "semanticModels", with_properties = with_properties)
    
    def update_semantic_model(self, workspace_id, semantic_model_id, display_name = None, description = None, return_item=False):
        """Update a semantic model in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            semantic_model_id (str): The ID of the semantic model
            display_name (str): The display name of the semantic model
            description (str): The description of the semantic model
        Returns:
            dict: The updated semantic model
        """
        return self.update_item(workspace_id, semantic_model_id, display_name = display_name, description = description,
                                type="semanticModels", return_item=return_item)

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
                                     return_item = False):
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
    
    def update_spark_job_definition(self, workspace_id, spark_job_definition_id, display_name = None, description = None, return_item=False):
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
    
    def list_spark_job_definition_livy_sessions(self, workspace_id, spark_job_definition_id):
        """List all livy sessions for a spark job definition
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
        Returns:
            list: The list of livy sessions
        """
        return self.list_livy_sessions(workspace_id=workspace_id, item_id=spark_job_definition_id, item_type="sparkJobDefinitions")
    
    def get_spark_job_definition_livy_session(self, workspace_id, spark_job_definition_id, livy_id):
        """Get a livy session for a spark job definition
        Args:
            workspace_id (str): The ID of the workspace
            spark_job_definition_id (str): The ID of the spark job definition
            livy_id (str): The ID of the livy session
        Returns:
            dict: The livy session
        """
        return self.get_livy_session(workspace_id=workspace_id, item_id=spark_job_definition_id, item_type="sparkJobDefinitions", livy_id=livy_id)

    # sql database

    def create_sql_database(self, workspace_id, display_name, description = None, definition = None):
        """Create a SQL database in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the SQL database
            description (str): The description of the SQL database
            definition (dict): The definition of the SQL database
        Returns:
            dict: The created SQL database
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "SQLDatabases", definition = definition, description = description)
    
    def delete_sql_database(self, workspace_id, sql_database_id):
        """Delete a SQL database from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            sql_database_id (str): The ID of the SQL database
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, sql_database_id, type="SQLDatabases")
    
    def get_sql_database(self, workspace_id, sql_database_id = None, sql_database_name = None):
        """Get a SQL database from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            sql_database_id (str): The ID of the SQL database
            sql_database_name (str): The name of the SQL database
        Returns:
            SQLDatabase: The SQL database object
        """
        from msfabricpysdkcore.otheritems import SQLDatabase
        if sql_database_id is None and sql_database_name is not None:
            sql_databases = self.list_sql_databases(workspace_id)
            sql_databases = [sd for sd in sql_databases if sd.display_name == sql_database_name]
            if len(sql_databases) == 0:
                raise Exception(f"SQL database with name {sql_database_name} not found")
            sql_database_id = sql_databases[0].id
        elif sql_database_id is None:
            raise Exception("sql_database_id or the sql_database_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/SQLDatabases/{sql_database_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting SQL database", return_format="json")
        
        return SQLDatabase.from_dict(item_dict, core_client=self)
    
    def list_sql_databases(self, workspace_id, with_properties = False):
        """List SQL databases in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of SQL databases
        """
        return self.list_items(workspace_id = workspace_id, type = "SQLDatabases", with_properties = with_properties)
    
    def update_sql_database(self, workspace_id, sql_database_id, display_name = None, description = None, return_item=False):
        """Update a SQL database in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            sql_database_id (str): The ID of the SQL database
            display_name (str): The display name of the SQL database
            description (str): The description of the SQL database
        Returns:
            dict: The updated SQL database
        """
        return self.update_item(workspace_id, sql_database_id, display_name = display_name, description = description,
                                type="SQLDatabases", return_item=return_item)
    
    # SQL endpoints
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlEndpoints/{sqlEndpointId}/connectionString?guestTenantId={guestTenantId}&privateLinkType={privateLinkType}
    def get_sql_endpoint_connection_string(self, workspace_id, sql_endpoint_id, guest_tenant_id = None, private_link_type = None):
        """Get the connection string of a SQL endpoint
        Args:
            workspace_id (str): The ID of the workspace
            sql_endpoint_id (str): The ID of the SQL endpoint
            guest_tenant_id (str): The guest tenant ID
            private_link_type (str): The private link type
        Returns:
            dict: The connection string of the SQL endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sqlEndpoints/{sql_endpoint_id}/connectionString"
        params = ""
        if guest_tenant_id is not None:
            params += f"?guestTenantId={guest_tenant_id}"
        if private_link_type is not None:
            if params:
                params += f"&privateLinkType={private_link_type}"
            else:
                params += f"?privateLinkType={private_link_type}"

        response_dict = self.calling_routine(url, operation="GET", params=params, response_codes=[200, 429],
                                            error_message="Error getting SQL endpoint connection string", return_format="json")

        return response_dict

    def list_sql_endpoints(self, workspace_id):
        """List sql endpoints in a workspace"""
        return self.list_items(workspace_id, type="sqlEndpoints")

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlEndpoints/{sqlEndpointId}/refreshMetadata?preview={preview}
    def refresh_sql_endpoint_metadata(self, workspace_id, sql_endpoint_id, preview = True, timeout = None, wait_for_completion = False):
        """Refresh the metadata of a SQL endpoint
        Args:
            workspace_id (str): The ID of the workspace
            sql_endpoint_id (str): The ID of the SQL endpoint
            preview (bool): Whether to preview the refresh
            timeout (int): The timeout for the request
        Returns:
            response: The response of the refresh operation
        """
        body = {}
        if timeout is not None:
            body["timeout"] = timeout
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sqlEndpoints/{sql_endpoint_id}/refreshMetadata?preview={preview}"
        
        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 202, 429],
                                             error_message="Error refreshing SQL endpoint metadata", return_format="response",
                                             wait_for_completion=wait_for_completion)
        
        return response

    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlEndpoints/{itemId}/settings/sqlAudit
    def get_sql_endpoint_audit_settings(self, workspace_id, sql_endpoint_id):
        """Get the audit settings of a SQL endpoint
        Args:
            workspace_id (str): The ID of the workspace
            sql_endpoint_id (str): The ID of the SQL endpoint
        Returns:
            dict: The audit settings of the SQL endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sqlEndpoints/{sql_endpoint_id}/settings/sqlAudit"

        response_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting SQL endpoint audit settings", return_format="json")

        return response_dict
    
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlEndpoints/{itemId}/settings/sqlAudit/setAuditActionsAndGroups
    def set_sql_endpoint_audit_actions_and_groups(self, workspace_id, sql_endpoint_id, set_audit_actions_and_groups_request):
        """Set the audit actions and groups of a SQL endpoint
        Args:
            workspace_id (str): The ID of the workspace
            sql_endpoint_id (str): The ID of the SQL endpoint
            set_audit_actions_and_groups_request (list): The list of audit actions and groups
        Returns:
            dict: The updated audit settings of the SQL endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sqlEndpoints/{sql_endpoint_id}/settings/sqlAudit/setAuditActionsAndGroups"

        body = set_audit_actions_and_groups_request

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[200, 429],
                                            error_message="Error setting SQL endpoint audit actions and groups", return_format="response")

        return response

    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlEndpoints/{itemId}/settings/sqlAudit
    def update_sql_endpoint_audit_settings(self, workspace_id, sql_endpoint_id, retention_days, state):
        """Update the audit settings of a SQL endpoint
        Args:
            workspace_id (str): The ID of the workspace
            sql_endpoint_id (str): The ID of the SQL endpoint
            retention_days (int): The number of days to retain the audit logs
            state (str): The state of the audit settings
        Returns:
            dict: The updated audit settings of the SQL endpoint
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sqlEndpoints/{sql_endpoint_id}/settings/sqlAudit"

        body = {
            "retentionDays": retention_days,
            "state": state
        }

        response = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                            error_message="Error updating SQL endpoint audit settings", return_format="response")

        return response

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
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/connectionString?guestTenantId={guestTenantId}&privateLinkType={privateLinkType}
    def get_warehouse_connection_string(self, workspace_id, warehouse_id, guest_tenant_id=None, private_link_type=None):
        """Get the connection string of a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            guest_tenant_id (str): The guest tenant ID
            private_link_type (str): The private link type
        Returns:
            dict: The connection string of the warehouse
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/connectionString"
        params = ""
        if guest_tenant_id is not None:
            params += f"?guestTenantId={guest_tenant_id}"
        if private_link_type is not None:
            if params:
                params += f"&privateLinkType={private_link_type}"
            else:
                params += f"?privateLinkType={private_link_type}"
        
        url += params

        response_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting warehouse connection string", return_format="json")

        return response_dict
    
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

    def update_warehouse(self, workspace_id, warehouse_id, display_name = None, description = None, return_item=False):
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
    
    # warehouse restore points
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/restorePoints
    def create_warehouse_restore_point(self, workspace_id, warehouse_id, display_name = None, description = None, wait_for_completion = False):
        """Create a restore point for a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            display_name (str): The display name of the restore point
            description (str): The description of the restore point
            wait_for_completion (bool): Whether to wait for the restore point creation to complete
        Returns:
            dict: The created restore point
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/restorePoints"

        body = {}
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        response = self.calling_routine(url, operation="POST", body=body, response_codes=[201,202, 429],
                                         error_message="Error creating warehouse restore point", return_format="json"
                                         , wait_for_completion=wait_for_completion)

        return response

    # DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/restorePoints/{restorePointId}
    def delete_warehouse_restore_point(self, workspace_id, warehouse_id, restore_point_id):
        """Delete a restore point for a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            restore_point_id (str): The ID of the restore point
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/restorePoints/{restore_point_id}"

        response = self.calling_routine(url, operation="DELETE", response_codes=[200, 429],
                                        error_message="Error deleting warehouse restore point", return_format="response")

        return response.status_code
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/restorePoints/{restorePointId}
    def get_warehouse_restore_point(self, workspace_id, warehouse_id, restore_point_id):
        """Get a restore point for a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            restore_point_id (str): The ID of the restore point
        Returns:
            dict: The restore point
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/restorePoints/{restore_point_id}"

        response_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                            error_message="Error getting warehouse restore point", return_format="json")

        return response_dict
    
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/restorePoints?continuationToken={continuationToken}
    def list_warehouse_restore_points(self, workspace_id, warehouse_id):
        """List restore points for a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
        Returns:
            list: The list of restore points
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/restorePoints"

        items = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                     error_message="Error listing warehouse restore points", return_format="value_json", paging=True)
        
        return items

    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/restorePoints/{restorePointId}/restore
    def restore_warehouse_to_restore_point(self, workspace_id, warehouse_id, restore_point_id, wait_for_completion = False):
        """Restore a warehouse to a restore point
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            restore_point_id (str): The ID of the restore point
            wait_for_completion (bool): Whether to wait for the restore operation to complete
        Returns:
            response: The response of the restore operation
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/restorePoints/{restore_point_id}/restore"

        response = self.calling_routine(url, operation="POST", response_codes=[200, 202, 429],
                                        error_message="Error restoring warehouse to restore point", return_format="response",
                                        wait_for_completion=wait_for_completion)

        return response
    
    # PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{warehouseId}/restorePoints/{restorePointId}
    def update_warehouse_restore_point(self, workspace_id, warehouse_id, restore_point_id, display_name = None, description = None):
        """Update a restore point for a warehouse
        Args:
            workspace_id (str): The ID of the workspace 
            warehouse_id (str): The ID of the warehouse
            restore_point_id (str): The ID of the restore point
            display_name (str): The display name of the restore point
            description (str): The description of the restore point
        Returns:
            dict: The updated restore point
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/restorePoints/{restore_point_id}"

        body = {}
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        if not body:
            return None

        response_dict = self.calling_routine(url, operation="PATCH", body=body, response_codes=[200, 429],
                                            error_message="Error updating warehouse restore point", return_format="json")

        return response_dict

    # warehouse sql audit settings
    # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehouses/{itemId}/settings/sqlAudit
    def get_warehouse_sql_audit_settings(self, workspace_id, warehouse_id):
        """Get the audit settings of a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
        Returns:
            dict: The audit settings of the warehouse
        """

        return self.get_sql_endpoint_audit_settings(workspace_id, warehouse_id)
    
    def set_warehouse_audit_actions_and_groups(self, workspace_id, warehouse_id, set_audit_actions_and_groups_request):
        """Set the audit actions and groups of a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            set_audit_actions_and_groups_request (list): The list of audit actions and groups
        Returns:
            dict: The updated audit settings of the warehouse
        """
        return self.set_sql_endpoint_audit_actions_and_groups(workspace_id, warehouse_id, set_audit_actions_and_groups_request)

    def update_warehouse_sql_audit_settings(self, workspace_id, warehouse_id, retention_days, state):
        """Update the audit settings of a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_id (str): The ID of the warehouse
            retention_days (int): The number of days to retain the audit logs
            state (str): The state of the audit settings
        Returns:
            dict: The updated audit settings of the warehouse
        """
        return self.update_sql_endpoint_audit_settings(workspace_id, warehouse_id, retention_days, state)


    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/warehousesnapshots
    def create_warehouse_snapshot(self, workspace_id, display_name, creation_payload, description = None, folder_id = None):
        """Create a snapshot of a warehouse
        Args:
            workspace_id (str): The ID of the workspace
            display_name (str): The display name of the snapshot
            creation_payload (dict): The payload for creating the snapshot
            description (str): The description of the snapshot
            folder_id (str): The ID of the folder to create the snapshot in
        Returns:
            dict: The created snapshot
        """
        return self.create_item(workspace_id = workspace_id, display_name = display_name, type = "warehousesnapshots", 
                                creation_payload = creation_payload, description = description, folder_id = folder_id)
    
    def delete_warehouse_snapshot(self, workspace_id, warehouse_snapshot_id):
        """Delete a warehouse snapshot from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_snapshot_id (str): The ID of the warehouse snapshot
        Returns:
            int: The status code of the response
        """
        return self.delete_item(workspace_id, warehouse_snapshot_id, type="warehousesnapshots")
    
    def get_warehouse_snapshot(self, workspace_id, warehouse_snapshot_id = None, warehouse_snapshot_name = None):
        """Get a warehouse snapshot from a workspace
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_snapshot_id (str): The ID of the warehouse snapshot
            warehouse_snapshot_name (str): The name of the warehouse snapshot
        Returns:
            WarehouseSnapshot: The warehouse snapshot object
        """
        from msfabricpysdkcore.otheritems import WarehouseSnapshot
        if warehouse_snapshot_id is None and warehouse_snapshot_name is not None:
            warehouse_snapshots = self.list_warehouse_snapshots(workspace_id)
            warehouse_snapshots = [ws for ws in warehouse_snapshots if ws.display_name == warehouse_snapshot_name]
            if len(warehouse_snapshots) == 0:
                raise Exception(f"Warehouse snapshot with name {warehouse_snapshot_name} not found")
            warehouse_snapshot_id = warehouse_snapshots[0].id
        if warehouse_snapshot_id is None:
            raise Exception("warehouse_snapshot_id or the warehouse_snapshot_name is required")
        
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehousesnapshots/{warehouse_snapshot_id}"

        item_dict = self.calling_routine(url, operation="GET", response_codes=[200, 429],
                                         error_message="Error getting warehouse snapshot", return_format="json")
        
        return WarehouseSnapshot.from_dict(item_dict, core_client=self)
    
    def list_warehouse_snapshots(self, workspace_id, with_properties = False):
        """List warehouse snapshots in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            with_properties (bool): Whether to get the item object with properties
        Returns:
            list: The list of warehouse snapshots
        """
        return self.list_items(workspace_id = workspace_id, type = "warehousesnapshots", with_properties = with_properties)
    
    def update_warehouse_snapshot(self, workspace_id, warehouse_snapshot_id, display_name = None, description = None, return_item=False, properties = None):
        """Update a warehouse snapshot in a workspace
        Args:
            workspace_id (str): The ID of the workspace
            warehouse_snapshot_id (str): The ID of the warehouse snapshot
            display_name (str): The display name of the warehouse snapshot
            description (str): The description of the warehouse snapshot
        Returns:
            dict: The updated warehouse snapshot
        """
        return self.update_item(workspace_id, warehouse_snapshot_id, display_name = display_name, description = description,
                                type="warehousesnapshots", return_item=return_item, properties=properties)
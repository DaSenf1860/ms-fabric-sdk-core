import json
from warnings import warn

from msfabricpysdkcore.coreapi import FabricClientCore

class DeploymentPipeline:
    """Class to represent a deployment pipeline in Microsoft Fabric"""

    def __init__(self, id, display_name, description, stages, core_client: FabricClientCore) -> None:
        self.id = id
        self.display_name = display_name
        self.description = description
        self.stages = stages
        self.core_client = core_client

    
    def from_dict(dict,  core_client):
        """Create a Workspace object from a dictionary"""
        if dict["displayName"] == None:
            dict["displayName"] = dict["display_name"]

        depl_pipe = DeploymentPipeline(
            id=dict["id"],
            display_name=dict["displayName"],
            description=dict["description"],
            stages=[],
            core_client=core_client
        )

        if "stages" in dict:
            depl_pipe.stages = dict["stages"]
        else:
            dict["stages"] = depl_pipe.List_stages()

        return depl_pipe

    
    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {"id": self.id, "display_name": self.display_name, "description": self.description, "stages": self.stages}

        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()

    def add_role_assignment(self, principal, role):
        """Add a role assignment to the deployment pipeline"""
        return self.core_client.add_deployment_pipeline_role_assignment(deployment_pipeline_id=self.id, principal=principal, role=role)
    
    def assign_workspace_to_stage(self, stage_id, workspace_id):
        """Assign a workspace to a stage in the deployment pipeline"""
        return self.core_client.assign_workspace_to_stage(deployment_pipeline_id=self.id, stage_id=stage_id, workspace_id=workspace_id)

    def delete(self):
        """Delete the deployment pipeline"""
        return self.core_client.delete_deployment_pipeline(deployment_pipeline_id=self.id)

    def delete_role_assignment(self, principal_id):
        """Delete a role assignment from the deployment pipeline"""
        return self.core_client.delete_deployment_pipeline_role_assignment(deployment_pipeline_id=self.id, principal_id=principal_id)
    
    def deploy_stage_content(self, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, options = None, wait_for_completion = True):
        """Deploy the content of a stage to another stage in the deployment pipeline"""
        return self.core_client.deploy_stage_content(deployment_pipeline_id=self.id, source_stage_id=source_stage_id,
                                                     target_stage_id=target_stage_id, created_workspace_details=created_workspace_details,
                                                     items=items, note=note, options=options, wait_for_completion=wait_for_completion)
  
    def deploy(self, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, options = None, wait_for_completion = True):
        return self.deploy_stage_content(deployment_pipelinesource_stage_id=source_stage_id,
                                         target_stage_id=target_stage_id, created_workspace_details=created_workspace_details,
                                         items=items, note=note, options=options, wait_for_completion=wait_for_completion)
    
    def get(self):
        """Get the deployment pipeline"""
        return self.core_client.get_deployment_pipeline(deployment_pipeline_id=self.id)

    def get_operation(self, operation_id):
        """Get the deployment pipeline operation"""
        return self.core_client.get_deployment_pipeline_operation(deployment_pipeline_id=self.id, operation_id=operation_id)

    def get_stage(self, stage_id):
        """Get the deployment pipeline stage"""
        return self.core_client.get_deployment_pipeline_stage(deployment_pipeline_id=self.id, stage_id=stage_id)

    def list_operations(self):
        """List the deployment pipeline operations"""
        return self.core_client.list_deployment_pipeline_operations(deployment_pipeline_id=self.id)
    
    def list_role_assignments(self):
        """List the role assignments of the deployment pipeline"""
        return self.core_client.list_deployment_pipeline_role_assignments(deployment_pipeline_id=self.id)

    def list_stage_items(self, stage_id = None, stage_name = None):
        """List the items in the deployment pipeline stage"""
        return self.core_client.list_deployment_pipeline_stage_items(deployment_pipeline_id=self.id, stage_id=stage_id, stage_name=stage_name)

    def list_stages(self):
        """List the stages in the deployment pipeline"""
        return self.core_client.list_deployment_pipeline_stages(deployment_pipeline_id=self.id)

    def unassign_workspace_from_stage(self, stage_id):
        """Unassign a workspace from a stage in the deployment pipeline"""
        return self.core_client.unassign_workspace_from_stage(deployment_pipeline_id=self.id, stage_id=stage_id)
    
    def update(self, display_name = None, description = None):
        """Update the deployment pipeline"""
        return self.core_client.update_deployment_pipeline(deployment_pipeline_id=self.id, display_name=display_name, description=description)

    def update_stage(self, stage_id, display_name, description = None, is_public = None):
        """Update the deployment pipeline stage"""
        return self.core_client.update_deployment_pipeline_stage(deployment_pipeline_id=self.id, stage_id=stage_id, display_name=display_name, description=description, is_public=is_public)

        

class DeploymentPipelineStage():

    """Class to represent a deployment pipeline stage in Microsoft Fabric"""

    def __init__(self, id, order, display_name, description, workspace_id, workspace_name, is_public,
                 deployment_pipeline_id, core_client: FabricClientCore, items = None) -> None:
        self.id = id
        self.order = order
        self.display_name = display_name
        self.description = description
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.is_public = is_public
        self.items = items
        self.deployment_pipeline_id = deployment_pipeline_id
        self.core_client = core_client

    
    def from_dict(dict,  core_client):
        """Create a Workspace object from a dictionary"""
        if dict["displayName"] is None:
            dict["displayName"] = dict["display_name"]

        if dict.get("workspaceId", None) is None:
            dict["workspaceId"] = dict.get("workspace_id", None)
        
        if dict.get("workspaceName", None)  is None:
            dict["workspaceName"] = dict.get("workspace_name", None)
        
        if dict["deploymentPipelineId"] is None:
            dict["deploymentPipelineId"] = dict["deployment_pipeline_id"]

        if dict["isPublic"] is None:
            dict["isPublic"] = dict["is_public"]

        
        return DeploymentPipelineStage(id=dict["id"],
                                         order=dict["order"],
                                         display_name=dict["displayName"],
                                         description=dict["description"],
                                         workspace_id=dict["workspaceId"],
                                         workspace_name=dict["workspaceName"],
                                         is_public=dict["isPublic"],
                                         items = dict.get("items", None),
                                         deployment_pipeline_id=dict["deploymentPipelineId"],
                                         core_client=core_client
                                        )
    
    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {"id": self.id, "order": self.order, "display_name": self.display_name, 
                 "description": self.description, "workspace_id": self.workspace_id, 
                 "workspace_name": self.workspace_name, 
                 "deployment_pipeline_id": self.deployment_pipeline_id,
                 "is_public": self.is_public}

        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def assign_workspace_to_stage(self, workspace_id):
        """Assign a workspace to the stage"""
        resp = self.core_client.assign_workspace_to_stage(deployment_pipeline_id=self.deployment_pipeline_id, stage_id=self.id, workspace_id=workspace_id)
        self.workspace_id = workspace_id
        ws = self.core_client.get_workspace(workspace_id=workspace_id)
        self.workspace_name = ws.display_name
        return resp

    def get(self):
        """Get the deployment pipeline stage"""
        return self.core_client.get_deployment_pipeline_stage(deployment_pipeline_id=self.deployment_pipeline_id, stage_id=self.id)

    def list_items(self):
        return self.core_client.list_deployment_pipeline_stage_items(deployment_pipeline_id=self.deployment_pipeline_id, stage_id=self.id)
    
    def unassign_workspacee(self):
        """Unassign the workspace from the stage"""
        resp = self.core_client.unassign_workspace_from_stage(deployment_pipeline_id=self.deployment_pipeline_id, stage_id=self.id)
        self.workspace_id = None
        self.workspace_name = None
        return resp
    
    def update(self, display_name = None, description = None, is_public = None):
        """Update the deployment pipeline stage"""
        return self.core_client.update_deployment_pipeline_stage(deployment_pipeline_id=self.deployment_pipeline_id, stage_id=self.id, display_name=display_name, description=description, is_public=is_public)
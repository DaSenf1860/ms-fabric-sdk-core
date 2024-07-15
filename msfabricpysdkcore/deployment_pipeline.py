import json

from msfabricpysdkcore.coreapi import FabricClientCore

class DeploymentPipeline:
    """Class to represent a deployment pipeline in Microsoft Fabric"""

    def __init__(self, id, display_name, description, core_client: FabricClientCore) -> None:
        self.id = id
        self.display_name = display_name
        self.description = description
        self.core_client = core_client

    
    def from_dict(dict,  core_client):
        """Create a Workspace object from a dictionary"""
        if dict["displayName"] == None:
            dict["displayName"] = dict["display_name"]

        
        return DeploymentPipeline(
            id=dict["id"],
            display_name=dict["displayName"],
            description=dict["description"],
            core_client=core_client
        )

    
    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {"id": self.id, "display_name": self.display_name, "description": self.description}

        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()

    def deploy(self, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, wait_for_completion = True):
        return self.core_client.deploy_stage_content(deployment_pipeline_id=self.id, source_stage_id=source_stage_id,
                                                     target_stage_id=target_stage_id, created_workspace_details=created_workspace_details,
                                                     items=items, note=note, wait_for_completion=wait_for_completion)
    
    def get_pipeline(deployment_pipeline_id, core_client: FabricClientCore):
        return core_client.get_deployment_pipeline(deployment_pipeline_id=deployment_pipeline_id)   


    def get_stages(self):
        print("DEPRECATED: Use list_stages() instead")
        return self.list_stages(self)
    
    def list_stages(self):
        return self.core_client.list_deployment_pipeline_stages(deployment_pipeline_id=self.id)


    def get_deployment_pipeline_stages_items(self, stage_id = None, stage_name = None):
        print("DEPRECATED: Use list_deployment_pipeline_stages_items() instead")
        return self.list_deployment_pipeline_stages_items(stage_id=stage_id, stage_name=stage_name)


    def list_deployment_pipeline_stages_items(self, stage_id = None, stage_name = None):
        return self.core_client.list_deployment_pipeline_stages_items(deployment_pipeline_id=self.id, stage_id=stage_id, stage_name=stage_name)

class Deployment_Pipeline_Stage():

    """Class to represent a deployment pipeline stage in Microsoft Fabric"""

    def __init__(self, id, order, display_name, description, workspace_id, workspace_name, is_public, deployment_pipeline_id, core_client: FabricClientCore) -> None:
        self.id = id
        self.order = order
        self.display_name = display_name
        self.description = description
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.is_public = is_public
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

        
        return Deployment_Pipeline_Stage(id=dict["id"],
                                         order=dict["order"],
                                         display_name=dict["displayName"],
                                         description=dict["description"],
                                         workspace_id=dict["workspaceId"],
                                         workspace_name=dict["workspaceName"],
                                         is_public=dict["isPublic"],
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
    
    def get_items(self):
        print("DEPRECATED: Use list_items() instead")
        return self.list_items()
    
    def list_items(self):
        return self.core_client.list_deployment_pipeline_stages_items(deployment_pipeline_id=self.deployment_pipeline_id, stage_id=self.id)
        
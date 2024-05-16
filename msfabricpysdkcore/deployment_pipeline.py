import json
from time import sleep

import requests 
from msfabricpysdkcore.long_running_operation import check_long_running_operation


class DeploymentPipeline:
    """Class to represent a deployment pipeline in Microsoft Fabric"""

    def __init__(self, id, display_name, description, auth) -> None:
        self.id = id
        self.display_name = display_name
        self.description = description
        self.auth = auth

    
    def from_dict(dict,  auth):
        """Create a Workspace object from a dictionary"""
        if dict["displayName"] == None:
            dict["displayName"] = dict["display_name"]

        
        return DeploymentPipeline(
            id=dict["id"],
            display_name=dict["displayName"],
            description=dict["description"],
            auth=auth
        )

    
    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {"id": self.id, "display_name": self.display_name, "description": self.description}

        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_pipeline(deployment_pipeline_id, auth):
        """Get a deployment pipeline"""
        # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{deployment_pipeline_id}"

        for _ in range(10):
            response = requests.get(url=url, headers=auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting item: {response.text}")
            break
        
        item_dict = json.loads(response.text)
        return DeploymentPipeline.from_dict(item_dict, auth)
    
    def get_stages(self, continuationToken = None):
        """Get stages in a deployment pipeline"""
        # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/stages

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{self.id}/stages"

        if continuationToken:
            url += f"?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting stages: {response.text}")
            break
        
        resp_dict = json.loads(response.text)
        items = resp_dict["value"]
        for item in items:
            item["deploymentPipelineId"] = self.id
        stages = [Deployment_Pipeline_Stage.from_dict(item, self.auth) for item in items]

        if "continuationToken" in resp_dict:
            stages_next = self.get_stages(continuationToken=resp_dict["continuationToken"])
            stages.extend(stages_next)
        
        return stages
    

    def deploy(self, source_stage_id, target_stage_id, created_workspace_details = None,
               items = None, note = None, wait_for_completion = True):
        # POST https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/deploy

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{self.id}/deploy"

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
            

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202 and wait_for_completion:
                print("successfully started the operation")
                try:
                    operation_result = check_long_running_operation( response.headers, self.auth)
                    return operation_result
                except Exception as e:
                    print("Problem waiting for long running operation. Returning initial response.")
                    print(e)
                    return response
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error deploying: {response.text}")
            break

        return response.json()



    def get_deployment_pipeline_stages_items(self, stage_id = None, stage_name = None):
        """Get items in a deployment pipeline stage"""

        if stage_id == None and stage_name == None:
            raise Exception("Please provide either stage_id or stage_name")
        stages = self.get_stages()
        if stage_id is None:
            dep_pip_stages = [stage for stage in stages if stage.display_name == stage_name]
            if len(dep_pip_stages) == 0:
                raise Exception(f"Stage with name {stage_name} not found")
        else:
            dep_pip_stages = [stage for stage in stages if stage.id == stage_id]
            if len(dep_pip_stages) == 0:
                raise Exception(f"Stage with id {stage_id} not found")
        dep_pip_stage = dep_pip_stages[0]
        return dep_pip_stage.get_items()

class Deployment_Pipeline_Stage():

    """Class to represent a deployment pipeline stage in Microsoft Fabric"""

    def __init__(self, id, order, display_name, description, workspace_id, workspace_name, is_public, deployment_pipeline_id, auth) -> None:
        self.id = id
        self.order = order
        self.display_name = display_name
        self.description = description
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.is_public = is_public
        self.deployment_pipeline_id = deployment_pipeline_id
        self.auth = auth

    
    def from_dict(dict,  auth):
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
                                         auth=auth
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
    

    def get_items(self, continuationToken = None):
        """Get items in a deployment pipeline stage"""
        # GET https://api.fabric.microsoft.com/v1/deploymentPipelines/{deploymentPipelineId}/stages/{stageId}/items

        url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{self.deployment_pipeline_id}/stages/{self.id}/items"
        if continuationToken is not None:
            url += f"?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting items: {response.text}")
            break

        resp_dict = json.loads(response.text)
        items = resp_dict["value"]
        return items

        
import json 
from msfabricpysdkcore.coreapi import FabricClientCore

class JobInstance:
    """Class to represent a job instance in Microsoft Fabric"""

    def __init__(self, id, item_id, workspace_id, core_client: FabricClientCore, job_type, invoke_type, status, root_activity_id,
                 start_time_utc, end_time_utc, failureReason):

        self.id = id
        self.item_id = item_id
        self.workspace_id = workspace_id
        self.job_type = job_type
        self.invoke_type = invoke_type
        self.status = status
        self.root_activity_id = root_activity_id
        self.start_time_utc = start_time_utc
        self.end_time_utc = end_time_utc
        self.failureReason = failureReason
        
        self.core_client = core_client


    def __str__(self) -> str:
        """Return a string representation of the workspace object"""
        dict_ = {
            'id': self.id,
            'item_id': self.item_id,
            'workspace_id': self.workspace_id,
            'job_type': self.job_type,
            'invoke_type': self.invoke_type,
            'status': self.status,
            'root_activity_id': self.root_activity_id,
            'start_time_utc': self.start_time_utc,
            'end_time_utc': self.end_time_utc,
            'failureReason': self.failureReason
        }
        return json.dumps(dict_, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def from_dict(job_dict, core_client):
        """Create JobInstance object from dictionary"""
        return JobInstance(id=job_dict['id'], item_id=job_dict['itemId'], workspace_id=job_dict['workspaceId'],
                           job_type=job_dict['jobType'], invoke_type=job_dict['invokeType'], status=job_dict['status'],
                           root_activity_id=job_dict['rootActivityId'], start_time_utc=job_dict['startTimeUtc'],
                           end_time_utc=job_dict['endTimeUtc'], failureReason=job_dict['failureReason'], core_client=core_client)
    
    def cancel(self):
        """Cancel the job instance"""
        return self.core_client.cancel_item_job_instance(workspace_id=self.workspace_id,
                                                         item_id=self.item_id,
                                                         job_instance_id=self.id)
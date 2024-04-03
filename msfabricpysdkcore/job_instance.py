import json 
import requests
from time import sleep
from msfabricpysdkcore.long_running_operation import check_long_running_operation

class JobInstance:
    """Class to represent a job instance in Microsoft Fabric"""

    def __init__(self, id, item_id, workspace_id, auth, job_type, invoke_type, status, root_activity_id,
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
        
        self.auth = auth


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
    
    def from_dict(job_dict, auth):
        """Create JobInstance object from dictionary"""
        return JobInstance(id=job_dict['id'], item_id=job_dict['itemId'], workspace_id=job_dict['workspaceId'],
                           job_type=job_dict['jobType'], invoke_type=job_dict['invokeType'], status=job_dict['status'],
                           root_activity_id=job_dict['rootActivityId'], start_time_utc=job_dict['startTimeUtc'],
                           end_time_utc=job_dict['endTimeUtc'], failureReason=job_dict['failureReason'], auth=auth)
    
    def cancel(self):
        """Cancel the job instance"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/items/{self.item_id}/jobs/instances/{self.id}/cancel"
        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue

            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error running on demand job: {response.text}")
            break

        return response.status_code
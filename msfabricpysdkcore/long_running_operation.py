import json 
import requests
from time import sleep

class LongRunningOperation:
    """Class to represent a workspace in Microsoft Fabric"""

    def __init__(self, operation_id, auth) -> None:
        self.operation_id = operation_id
        self.auth = auth

        self.state = self.get_operation_state()["status"]


    def get_operation_results(self):
        """Get the results of an operation"""
        url = f"https://api.fabric.microsoft.com/v1/operations/{self.operation_id}/result"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 400:
                return None
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting operation results: {response.text}")
            break

        return json.loads(response.text)
    
    def get_operation_state(self):
        """Get the state of an operation"""
        url = f"https://api.fabric.microsoft.com/v1/operations/{self.operation_id}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting operation state: {response.text}")
            break

        return json.loads(response.text)    
    
    def wait_for_completion(self):
        """Wait for the operation to complete"""
        max_iter = 20
        while self.state not in ('Succeeded', 'Failed'):
            self.state = self.get_operation_state()["status"]
            sleep(3)
            if max_iter == 0:
                raise Exception("Operation did not complete after 60 seconds")
            max_iter -= 1
        return self.state
    

def check_long_running_operation(headers, auth):
    """Check the status of a long running operation"""
    location = headers.get('Location', None)
    operation_id = headers.get('x-ms-operation-id', None)
    if location:
        operation_id = location.split("/")[-1]
    
    if not operation_id:
        print("Operation initiated, no operation id found")
        return None
    lro = LongRunningOperation(operation_id=operation_id, auth=auth)
    lro.wait_for_completion()
    
    return lro.get_operation_results()
import logging
from time import sleep, time
from msfabricpysdkcore.coreapi import FabricClientCore
from msfabricpysdkcore.util import logger


class LongRunningOperation:
    """Class to represent a workspace in Microsoft Fabric"""

    _logger: logging.Logger

    def __init__(self, operation_id, core_client: FabricClientCore) -> None:
        """Initialize the LongRunningOperation object"""

        self._logger = logger.getChild(__name__)
        self.operation_id = operation_id
        self.core_client = core_client

        self.state = self.get_operation_state()["status"]

    def get_operation_results(self):
        return self.core_client.get_operation_results(operation_id=self.operation_id)
    
    def get_operation_state(self):
        return self.core_client.get_operation_state(operation_id=self.operation_id) 
    
    def wait_for_completion(self):
        """Wait for the operation to complete"""
        start_time = time()
        while self.state not in ('Succeeded', 'Failed'):
            self.state = self.get_operation_state()["status"]
            duration = int(time() - start_time)
            if duration > 60:
                
                if self.state == "Running":
                    self._logger.info(f"Operation did not complete after {duration} seconds")
                    return "Running"
                raise TimeoutError(f"Operation did not complete after {duration} seconds")
            sleep(3)
        return self.state
    

def check_long_running_operation(headers, core_client):
    """Check the status of a long-running operation"""
    location = headers.get('Location', None)
    operation_id = headers.get('x-ms-operation-id', None)
    if location:
        operation_id = location.split("/")[-1]
    
    if not operation_id:
        self._logger.info("Operation initiated, no operation id found")
        return None
    lro = LongRunningOperation(operation_id=operation_id, core_client=core_client)
    lro.wait_for_completion()
    
    return lro.get_operation_results()
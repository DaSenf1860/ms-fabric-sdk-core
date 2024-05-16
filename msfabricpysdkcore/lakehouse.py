import json 
import requests
from time import sleep

from msfabricpysdkcore.item import Item
from msfabricpysdkcore.long_running_operation import check_long_running_operation

class Lakehouse(Item):
    """Class to represent a item in Microsoft Fabric"""

    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def from_dict(item_dict, auth):
        return Lakehouse(id=item_dict['id'], display_name=item_dict['displayName'], type=item_dict['type'], workspace_id=item_dict['workspaceId'],
            properties=item_dict.get('properties', None),
            definition=item_dict.get('definition', None), description=item_dict.get('description', ""), auth=auth)

    def list_tables(self, continuationToken = None):
        """List all tables in the lakehouse"""
        # GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/tables
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/lakehouses/{self.id}/tables"

        if continuationToken:
            url = f"{url}?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error listing tables: {response.status_code},  {response.text}")
            break
        resp_dict = json.loads(response.text)

        table_list = resp_dict["data"]

        if "continuationToken" in resp_dict and resp_dict["continuationToken"] is not None:
            table_list_next = self.list_tables(continuationToken=resp_dict["continuationToken"])
            table_list.extend(table_list_next)

        return table_list
    
    def load_table(self, table_name, path_type, relative_path,
                    file_extension = None, format_options = None,
                    mode = None, recursive = None, wait_for_completion = True):
        """Load a table in the lakehouse"""
        # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/tables/{tableName}/load
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/lakehouses/{self.id}/tables/{table_name}/load"

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

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202:
                if wait_for_completion:
                    success = self.check_if_table_is_created(table_name)
                    
                if not success:
                    print("Warning: Table not created after 3 minutes")
                else:
                    print("Table created")
            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error loading table: {response.status_code},  {response.text}")
            break

        return response.status_code
    
    def check_if_table_is_created(self, table_name):
        """Check if the table is created"""
        for _ in range(60):
            table_names = [table["name"] for table in self.list_tables()]
            if table_name in table_names:
                return True
            
            sleep(3)
        return False
    
    # run on demand table maintenance
    # POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/jobs/instances?jobType={jobType}

    def run_on_demand_table_maintenance(self, execution_data, job_type = "TableMaintenance", wait_for_completion = True):
        """Run on demand table maintenance"""
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}/lakehouses/{self.id}/jobs/instances?jobType={job_type}"

        body = {
                "executionData": execution_data
              }

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
                
            if response.status_code not in (200, 202, 429):
                print(response.status_code)
                print(response.text)

                raise Exception(f"Error at run on demand table maintenance: {response.text}")
            break

        return response
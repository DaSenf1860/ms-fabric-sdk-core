import json
from time import sleep

import requests
from msfabricpysdkcore.long_running_operation import check_long_running_operation

class Domain:
    """Class to represent a domain in Microsoft Fabric"""

    def __init__(self, id, display_name, description, parent_domain_id, contributors_scope, auth):
        """Constructor for the Domain class
        
        Args:
            id (str): The ID of the domain
            display_name (str): The display name of the domain
            description (str): The description of the domain
            parent_domain_id (str): The parent domain ID of the domain
            contributors_scope (str): The contributors scope of the domain
        Returns:
            Domain: The Domain object created"""

        self.id = id
        self.display_name = display_name
        self.description = description
        self.parent_domain_id = parent_domain_id
        self.contributors_scope = contributors_scope

        self.auth = auth

    def __str__(self):
        """Method to return a string representation of the Domain object
        
        Returns:
            str: The string representation of the Domain object
        """
        dic = {
            'id': self.id,
            'display_name': self.display_name,
            'description': self.description,
            'parent_domain_id': self.parent_domain_id,
            'contributors_scope': self.contributors_scope
        }
        return json.dumps(dic, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()

    def from_dict(dic, auth):
        """Method to create a Domain object from a dictionary
        
        Args:
            dic (dict): The dictionary containing the domain information
        Returns:
            Domain: The Domain object created from the dictionary
        
        """
        if "display_name" not in dic:
            dic["display_name"] = dic["displayName"]
        if "parent_domain_id" not in dic:
            dic["parent_domain_id"] = dic["parentDomainId"]
        if "contributors_scope" not in dic:
            dic["contributors_scope"] = dic["contributorsScope"]
        return Domain(id=dic['id'], display_name=dic['display_name'],
                      description=dic['description'], parent_domain_id=dic['parent_domain_id'], 
                      contributors_scope=dic['contributors_scope'], auth=auth)

    def list_domain_workspaces(self, workspace_objects = False, continuationToken = None):
        """Method to list the workspaces in the domain
        
        Args:
            continuationToken (str): The continuation token to use for pagination
        Returns:
            list: The list of workspaces in the domain
        """
        if workspace_objects:
            from msfabricpysdkcore import FabricClientCore
            fc = FabricClientCore()
                    
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/workspaces"
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
                raise Exception(f"Error listing workspaces: {response.text}")
            break

        resp_dict = json.loads(response.text)
        workspaces = resp_dict["value"]

        if workspace_objects:
            workspaces = [fc.get_workspace_by_id(workspace["id"]) for workspace in workspaces]

        if "continuationToken" in resp_dict:
            workspaces_next = self.list_domain_workspaces(continuationToken=resp_dict["continuationToken"])
            workspaces.extend(workspaces_next)

        return workspaces
    
    def delete(self):
        """Method to delete the domain

        Returns:
            int: The status code of the response
        """
        # DELETE https://api.fabric.microsoft.com/v1/admin/domains/{domainId}
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}"
        for _ in range(10):
            response = requests.delete(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error deleting domain: {response.text}")
            break

        return response.status_code
    

    # PATCH https://api.fabric.microsoft.com/v1/admin/domains/{domainId}

    def update(self, description = None, display_name = None, contributors_scope = None):
        """Method to update the domain
        
        Args:
            description (str): The description of the domain
            display_name (str): The display name of the domain
            contributors_scope (str): The contributors scope of the domain
        Returns:
             Domain: The Domain object created from the dictionary
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}"
        body = {}
        if description:
            body["description"] = description
        else:
            body["description"] = self.description

        if display_name:
            body["displayName"] = display_name
        else:
            body["displayName"] = self.display_name

        if contributors_scope:
            body["contributorsScope"] = contributors_scope
        else:
            body["contributorsScope"] = self.contributors_scope

        for _ in range(10):
            response = requests.patch(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error updating domain: {response.text}")
            break

        self.description = body["description"]
        self.display_name = body["displayName"]
        self.contributors_scope = body["contributorsScope"]

        return self
    
    def assign_workspaces_by_capacities(self, capacities_ids, wait_for_completion=True):
        """Method to assign workspaces to the domain based on capacities_ids
        
        Args:
            capacities_ids (list): The list of capacitiy ids to assign workspaces
        Returns:
            int: The status code of the response
        """
        # POST https://api.fabric.microsoft.com/v1/admin/domains/{domainId}/assignWorkspacesByCapacities
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/assignWorkspacesByCapacities"

        body = {
            "capacitiesIds": capacities_ids
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202 and wait_for_completion:
                check_long_running_operation(response.headers, self.auth)
            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error assigning workspaces by capacities: {response.text}")
            break

        return response.status_code


    def assign_workspaces_by_ids(self, workspaces_ids):

        """Method to assign workspaces to the domain based on workspaces_ids
        
        Args:
            workspaces_ids (list): The list of workspace ids to assign workspaces
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/assignWorkspaces"
        body = {
            "workspacesIds": workspaces_ids
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error assigning workspaces by ids: {response.text}")
            break

        return response.status_code
    

    def assign_workspaces_by_principals(self, principals, wait_for_completion=True):
        """Method to assign workspaces to the domain based on principals
        
        Args:
            principals (list): The list of principals to assign workspaces
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/assignWorkspacesByPrincipals"
        body = {
            "principals": principals
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code == 202 and wait_for_completion:
                check_long_running_operation(response.headers, self.auth)
            if response.status_code not in (202, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error assigning workspaces by principals: {response.text}")
            break

        return response.status_code
    
    # POST https://api.fabric.microsoft.com/v1/admin/domains/{domainId}/roleAssignments/bulkAssign

    def role_assignments_bulk_assign(self, type, principals):
        """Method to bulk assign role assignments
        
        Args:
            type (str): The type of the role assignment
            principals (list): The list of principals to assign the role
        Returns:
            int: The status code of the response
        """
        
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/roleAssignments/bulkAssign"
        body = {
            "type": type,
            "principals": principals
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error bulk assigning role assignments: {response.text}")
            break

        return response.status_code
    

    def role_assignments_bulk_unassign(self, type, principals):
        """Method to bulk unassign role assignments
        
        Args:
            type (str): The type of the role assignment
            principals (list): The list of principals to unassign the role
        Returns:
            int: The status code of the response
        """
        
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/roleAssignments/bulkUnassign"
        body = {
            "type": type,
            "principals": principals
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error bulk unassigning role assignments: {response.text}")
            break

        return response.status_code
    

    def unassign_all_workspaces(self):
        """Method to unassign all workspaces from the domain
        
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/unassignAllWorkspaces"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error unassigning all workspaces: {response.text}")
            break

        return response.status_code
    
    def unassign_workspaces_by_ids(self, workspace_ids):
        """Method to unassign workspaces from the domain
        
        Args:
            workspace_ids (list): The list of workspace ids to unassign
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{self.id}/unassignWorkspaces"
        body = {
            "workspacesIds": workspace_ids
        }

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error unassigning workspaces by ids: {response.text}")
            break

        return response.status_code
import requests
import json
import os
from time import sleep

from msfabricpysdkcore.admin_item import AdminItem
from msfabricpysdkcore.client import FabricClient
from msfabricpysdkcore.domain import Domain
from msfabricpysdkcore.admin_workspace import AdminWorkspace

class FabricClientAdmin(FabricClient):
    """FabricClientAdmin class to interact with Fabric Admin APIs"""

    def __init__(self, tenant_id = None, client_id = None, client_secret = None) -> None:
        """Initialize FabricClientAdmin object"""
        super().__init__(tenant_id, client_id, client_secret)

    
    def list_domains(self, nonEmptyOnly=False):
        """List all domains in the tenant
        
        Args:
            nonEmptyOnly (bool): Whether to list only non-empty domains
        Returns:
            list: List of Domain objects"""
        url = "https://api.fabric.microsoft.com/v1/admin/domains"
        if nonEmptyOnly:
            url = f"{url}?nonEmptyOnly=True"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error listing domains: {response.text}")
            break

        resp_dict = json.loads(response.text)
        domains = resp_dict["domains"]

        domains = [Domain.from_dict(i, self.auth) for i in domains]
        return domains
    
    def get_domain_by_id(self, domain_id):
        """Method to get a domain by ID
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            Domain: The Domain object
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}"
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting domain: {response.text}")
            break

        domain_dict = json.loads(response.text)
        domain = Domain.from_dict(domain_dict, self.auth)
        return domain

    def get_domain_by_name(self, domain_name):
        """Method to get a domain by name
        
        Args:
            domain_name (str): The name of the domain
        Returns:
            Domain: The Domain object
        """
        domains = self.list_domains()
        for domain in domains:
            if domain.display_name == domain_name:
                return domain
        raise ValueError("Domain not found")
    
    def get_domain(self, domain_id = None, domain_name = None):
        """Get a domain by ID or name
        
        Args:
            domain_id (str): The ID of the domain
            domain_name (str): The name of the domain
        Returns:
            Domain: The Domain object
        """
        if domain_id:
            return self.get_domain_by_id(domain_id)
        if domain_name:
            return self.get_domain_by_name(domain_name)
        raise ValueError("Either domain_id or domain_name must be provided")
    
    def create_domain(self, display_name, description = None, parent_domain_id = None):
        """Method to create a domain
        
        Args:
            display_name (str): The display name of the domain
            description (str): The description of the domain
            parent_domain_id (str): The parent domain ID
        Returns:
            Domain: The Domain object
        """
        # POST https://api.fabric.microsoft.com/v1/admin/domains
        url = "https://api.fabric.microsoft.com/v1/admin/domains"
        body = {
            "displayName": display_name
        }
        if description:
            body["description"] = description
        if parent_domain_id:
            body["parentDomainId"] = parent_domain_id
        
        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 201, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error creating domain: {response.text}")
            break

        domain_dict = json.loads(response.text)
        domain = Domain.from_dict(domain_dict, self.auth)
        return domain
    
    def delete_domain(self, domain_id):
        """Method to delete a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            status_code (int): The status code of the request
        """
        return self.get_domain_by_id(domain_id).delete()

    def update_domain(self, domain_id, description = None, display_name = None, contributors_scope = None):
        """Method to update a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            Domain: The Domain object
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.update(description = description, display_name = display_name, contributors_scope = contributors_scope)
    
    def list_domain_workspaces(self, domain_id, workspace_objects = False):
        """List workspaces in a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            list: List of Workspace objects
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.list_domain_workspaces(workspace_objects=workspace_objects)
    
    def assign_domain_workspaces_by_capacities(self, domain_id, capacities_ids, wait_for_completion=True):
        """Assign workspaces to a domain by capacities
        
        Args:
            domain_id (str): The ID of the domain
            capacities (list): The list of capacity IDs
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.assign_workspaces_by_capacities(capacities_ids, wait_for_completion)
    
    def assign_domain_workspaces_by_ids(self, domain_id, workspace_ids):
        """Assign workspaces to a domain by workspace IDs
        
        Args:
            domain_id (str): The ID of the domain
            workspace_ids (list): The list of workspace IDs
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.assign_workspaces_by_ids(workspace_ids)
    
    def assign_domains_workspaces_by_principals(self, domain_id, principals, wait_for_completion=True):
        """Assign workspaces to a domain by principals
        
        Args:
            domain_id (str): The ID of the domain
            principals (list): The list of principal IDs
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.assign_workspaces_by_principals(principals=principals, wait_for_completion=wait_for_completion)
    
    def role_assignments_bulk_assign(self, domain_id, type, principals):
        """Assign a role to principals in bulk
        
        Args:
            domain_id (str): The ID of the domain
            type (str): The type of the role assignment
            principals (list): The list of principals
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.role_assignments_bulk_assign(type, principals)
    
    def role_assignments_bulk_unassign(self, domain_id, type, principals):
        """Unassign a role from principals in bulk
        
        Args:
            domain_id (str): The ID of the domain
            type (str): The type of the role assignment
            principals (list): The list of principals
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.role_assignments_bulk_unassign(type, principals)
    
    def unassign_all_domain_workspaces(self, domain_id):
        """Unassign all workspaces from a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.unassign_all_workspaces()
    
    def unassign_domain_workspaces_by_ids(self, domain_id, workspace_ids):
        """Unassign workspaces from a domain by workspace IDs
        
        Args:
            domain_id (str): The ID of the domain
            workspace_ids (list): The list of workspace IDs
        Returns:
            int: The status code of the response
        """
        domain = self.get_domain_by_id(domain_id)
        return domain.unassign_workspaces_by_ids(workspace_ids=workspace_ids)
    
    def get_workspace(self, workspace_id):
        """Get a workspace by ID
        
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            Workspace: The Workspace object
        """

        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}"
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting workspace: {response.text}")
            break

        workspace_dict = json.loads(response.text)
        workspace = AdminWorkspace.from_dict(workspace_dict, self.auth)
        return workspace
    
    def get_workspace_access_details(self, workspace_id):
        """Get the access details of the workspace
        
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The access details of the workspace
        """
        print("DEPRECATED: Use list_workspace_access_details instead")
        return self.list_workspace_access_details(workspace_id)

    def list_workspace_access_details(self, workspace_id):
        """Get the access details of the workspace
        
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The access details of the workspace
        """
        ws = self.get_workspace(workspace_id)
        return ws.list_workspace_access_details()
    
    def list_workspaces(self, capacity_id = None, name=None, state=None, type=None, continuationToken = None):
        """List all workspaces
        
        Args:
            capacity_id (str): The ID of the capacity
        Returns:
            list: List of Workspace objects
        """
        #GET https://api.fabric.microsoft.com/v1/admin/workspaces?type={type}&capacityId={capacityId}&name={name}&state={state}&continuationToken={continuationToken}
        url = "https://api.fabric.microsoft.com/v1/admin/workspaces"
        first_parameter = False
        if type:
            url = f"{url}?type={type}"
            first_parameter = True
        if capacity_id:
            if first_parameter:
                url = f"{url}&capacityId={capacity_id}"
            else:
                url = f"{url}?capacityId={capacity_id}"

        if name:
            if first_parameter:
                url = f"{url}&name={name}"
            else:
                url = f"{url}?name={name}"
        
        if state:
            if first_parameter:
                url = f"{url}&state={state}"
            else:
                url = f"{url}?state={state}"

        if continuationToken:
            if first_parameter:
                url = f"{url}&continuationToken={continuationToken}"
            else:
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
        workspaces = resp_dict["workspaces"]

        workspaces = [AdminWorkspace.from_dict(i, self.auth) for i in workspaces]

        if "continuationToken" in resp_dict and resp_dict["continuationToken"] is not None:
            workspaces_next = self.list_workspaces(capacity_id=capacity_id, name=name, state=state, type=type,
                                                   continuationToken=resp_dict["continuationToken"])
            workspaces.extend(workspaces_next)

        return workspaces
        
    def list_items(self, workspace_id = None, capacity_id = None, type=None,
                   state=None, continuationToken = None):
        """List all items

        Returns:
            list: The list of items in the workspace
        """
        
        url = f"https://api.fabric.microsoft.com/v1/admin/items"
        first_parameter = False
        if workspace_id:
            url = f"{url}?workspaceId={workspace_id}"
            first_parameter = True
        if capacity_id:
            if first_parameter:
                url = f"{url}&capacityId={capacity_id}"
            else:
                url = f"{url}?capacityId={capacity_id}"
        if type:
            if first_parameter:
                url = f"{url}&type={type}"
            else:
                url = f"{url}?type={type}"
        if state:
            if first_parameter:
                url = f"{url}&state={state}"
            else:
                url = f"{url}?state={state}"
        if continuationToken:
            if first_parameter:
                url = f"{url}&continuationToken={continuationToken}"
            else:
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
                raise Exception(f"Error listing items: {response.text}")
            break
        resp_dict = json.loads(response.text)
        items =  [AdminItem.from_dict(item, self.auth) for item in resp_dict["itemEntities"]]

        if "continuationToken" in items and items["continuationToken"] is not None:
            items_next = self.list_items(workspace_id=workspace_id, capacity_id=capacity_id, type=type,
                                         state=state, continuationToken=items["continuationToken"])
            items.extend(items_next)

        return items
    
    def get_item(self, item_id, workspace_id, type = None):
        """Get an item from the workspace
        
        Args:
            item_id (str): The ID of the item
            workspace_id (str): The ID of the workspace
            type (str): The type of the item
        Returns:
            AdminItem: The item object
        """
        ws = self.get_workspace(workspace_id)
        return ws.get_item(item_id, type)
    

    def get_tenant_settings(self):
        """Get the tenant settings
        
        Returns:
            dict: The tenant settings
        """
        print("DEPRECATED: Use list_tenant_settings instead")
        return self.list_tenant_settings()
    
    def list_tenant_settings(self):
        """Get the tenant settings
        
        Returns:
            dict: The tenant settings
        """
        url = "https://api.fabric.microsoft.com/v1/admin/tenantsettings"
        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error getting tenant settings: {response.text}")
            break

        return json.loads(response.text)
    

    def list_capacities_tenant_settings_overrides(self, continuationToken = None):
        """Returns list of tenant setting overrides that override at the capacities
        
        Returns:
            list: The capacities tenant settings overrides
        """
        url = "https://api.fabric.microsoft.com/v1/admin/capacities/delegatedTenantSettingOverrides"
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
                raise Exception(f"Error getting capacities tenant settings overrides: {response.text}")
            break

        resp_dict = json.loads(response.text)
        overrides = resp_dict["Overrides"]

        if "continuationToken" in resp_dict and resp_dict["continuationToken"] is not None:
            overrides_next = self.list_capacities_tenant_settings_overrides(continuationToken=resp_dict["continuationToken"])
            overrides.extend(overrides_next)

        return overrides

    def get_capacities_tenant_settings_overrides(self):
        """Returns list of tenant setting overrides that override at the capacities
        
        Returns:
            list: The capacities tenant settings overrides
        """
        print("DEPRECATED: Use list_capacities_tenant_settings_overrides instead")
        return self.list_capacities_tenant_settings_overrides()
    

    def get_access_entities(self, user_id, type = None):
        """Get the access entities for a user
        
        Args:
            user_id (str): The ID of the user
            type (str): The type of the access entity
            continuationToken (str): The continuation token
        Returns:
            list: The list of access entities
        """
        print("DEPRECATED: Use list_access_entities instead")
        return self.list_access_entities(user_id, type)

    def list_access_entities(self, user_id, type = None, continuationToken = None):
        """Get the access entities for a user
        
        Args:
            user_id (str): The ID of the user
            type (str): The type of the access entity
            continuationToken (str): The continuation token
        Returns:
            list: The list of access entities
        """

        url = f"https://api.fabric.microsoft.com/v1/admin/users/{user_id}/access"

        first_parameter = False
        if type:
            url = f"{url}?type={type}"
            first_parameter = True
        if continuationToken:
            if first_parameter:
                url = f"{url}&continuationToken={continuationToken}"
            else:
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
                raise Exception(f"Error getting access entities: {response.text}")
            break

        resp_dict = json.loads(response.text)
        access_entities = resp_dict["accessEntities"]

        if "continuationToken" in resp_dict and resp_dict["continuationToken"] is not None:
            access_entities_next = self.list_access_entities(user_id, type, continuationToken=resp_dict["continuationToken"])
            resp_dict["accessEntities"].extend(access_entities_next)
        
        return access_entities
    
    def list_item_access_details(self, workspace_id, item_id, type=None):
        """Get the access details of the item
        
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            dict: The access details of the item
        """
        ws = self.get_workspace(workspace_id)
        item = ws.get_item(item_id, type)
        return item.list_item_access_details(type)
    
    def get_item_access_details(self, workspace_id, item_id, type=None):
        """Get the access details of the item
        
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            dict: The access details of the item
        """
        print("DEPRECATED: Use list_item_access_details instead")
        return self.list_item_access_details(workspace_id, item_id, type)
    
    def bulk_set_labels(self, items, label_id, assignment_method = None, delegated_principal = None):
        """Set labels in bulk"""
        # POST https://api.fabric.microsoft.com/v1/admin/items/bulkSetLabels

        url = "https://api.fabric.microsoft.com/v1/admin/items/bulkSetLabels"

        if len(items) > 2000:
            self.bulk_set_labels(items[2000:], label_id, assignment_method, delegated_principal)
            items = items[:2000]

        body = {
            "items": items,
            "labelId": label_id
        }
        if assignment_method:
            body["assignmentMethod"] = assignment_method

        if delegated_principal:
            body["delegatedPrincipal"] = delegated_principal

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers(), json=body)
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                print(response.status_code)
                print(response.text)
                raise Exception(f"Error setting labels: {response.text}")
            break

        response = json.loads(response.text)
        return response
    

    def bulk_remove_labels(self, items):
        """Remove labels in bulk
        Args:
            items (list): The list of item IDs
            
        Returns:
            dict: The response from the API"""
        # POST https://api.fabric.microsoft.com/v1/admin/items/bulkRemoveLabels

        url = "https://api.fabric.microsoft.com/v1/admin/items/bulkRemoveLabels"

        if len(items) > 2000:
            self.bulk_remove_labels(items[2000:])
            items = items[:2000]
        
        body = {
            "items": items
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
                raise Exception(f"Error removing labels: {response.text}")
            break

        response = json.loads(response.text)
        return response
    
    def list_external_data_shares(self, continuationToken = None):
        # GET https://api.fabric.microsoft.com/v1/admin/items/externalDataShares
        """List external data shares
        
        Returns:
            list: The list of external data shares
        """
        url = "https://api.fabric.microsoft.com/v1/admin/items/externalDataShares"

        if continuationToken:
            url = f"{url}?continuationToken={continuationToken}"

        for _ in range(10):
            response = requests.get(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error listing external data shares: {response.status_code}, {response.text}")
            break

        response = json.loads(response.text)
        list_data_shares = response["value"]

        if "continuationToken" in response and response["continuationToken"] is not None:
            list_data_shares_next = self.list_external_data_shares(continuationToken=response["continuationToken"])
            list_data_shares.extend(list_data_shares_next)
        return list_data_shares
    
    def revoke_external_data_share(self, external_data_share_id, item_id, workspace_id):
        # POST https://api.fabric.microsoft.com/v1/admin/workspaces/{workspaceId}/items/{itemId}/externalDataShares/{externalDataShareId}/revoke
        """Revoke an external data share"""
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}/items/{item_id}/externalDataShares/{external_data_share_id}/revoke"

        for _ in range(10):
            response = requests.post(url=url, headers=self.auth.get_headers())
            if response.status_code == 429:
                print("Too many requests, waiting 10 seconds")
                sleep(10)
                continue
            if response.status_code not in (200, 429):
                raise Exception(f"Error revoking external data share: {response.status_code}, {response.text}")
            break

        return response.status_code


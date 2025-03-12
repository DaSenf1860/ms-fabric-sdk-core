import requests
import json
import os
from time import sleep
from warnings import warn

from msfabricpysdkcore.client import FabricClient

class FabricClientAdmin(FabricClient):
    """FabricClientAdmin class to interact with Fabric Admin APIs"""

    def __init__(self, tenant_id = None, client_id = None, client_secret = None,
                 username = None, password = None) -> None:
        """Initialize FabricClientAdmin object"""
        super().__init__(scope="https://api.fabric.microsoft.com/.default", 
                         tenant_id=tenant_id, client_id=client_id, client_secret=client_secret,
                         username=username, password=password)


    def long_running_operation(self, response_headers):
        """Check the status of a long running operation"""
        from msfabricpysdkcore.coreapi import FabricClientCore
        fc = FabricClientCore(tenant_id=self.tenant_id, client_id=self.client_id, client_secret=self.client_secret)

        return fc.long_running_operation(response_headers)

    # Domain APIs

    def assign_domain_workspaces_by_ids(self, domain_id, workspaces_ids):
        """Assign workspaces to a domain by workspace IDs
        
        Args:
            domain_id (str): The ID of the domain
            workspace_ids (list): The list of workspace IDs
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/assignWorkspaces"
        body = {
            "workspacesIds": workspaces_ids
        }

        response:requests.Response = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                          error_message = "Error assigning workspaces by ids", return_format="response")

        return response.status_code
    
    def assign_domains_workspaces_by_principals(self, domain_id, principals, wait_for_completion=True):
        """Assign workspaces to a domain by principals
        
        Args:
            domain_id (str): The ID of the domain
            principals (list): The list of principal IDs
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/assignWorkspacesByPrincipals"
        body = {
            "principals": principals
        }

        response:requests.Response = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [202, 429],
                                                          error_message = "Error assigning workspaces by principals", wait_for_completion=wait_for_completion,
                                                          return_format="response")

        return response.status_code
    
    def create_domain(self, display_name, description = None, parent_domain_id = None):
        """Method to create a domain
        
        Args:
            display_name (str): The display name of the domain
            description (str): The description of the domain
            parent_domain_id (str): The parent domain ID
        Returns:
            Domain: The Domain object
        """
        from msfabricpysdkcore.domain import Domain

        url = "https://api.fabric.microsoft.com/v1/admin/domains"
        body = {
            "displayName": display_name
        }
        if description:
            body["description"] = description
        if parent_domain_id:
            body["parentDomainId"] = parent_domain_id

        domain_dict = self.calling_routine(url = url, operation = "POST", body = body, return_format="json",
                                           response_codes = [200, 201, 429], error_message = "Error creating domain")
    
        domain = Domain.from_dict(domain_dict, self)
        return domain
    
    def delete_domain(self, domain_id):
        """Method to delete a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            status_code (int): The status code of the request
        """

        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}"

        response:requests.Response = self.calling_routine(url = url, operation = "DELETE", response_codes = [200, 429],
                                                          error_message = "Error deleting domain",
                                                          return_format="response")

        return response.status_code
    
    def get_domain_by_id(self, domain_id):
        """Method to get a domain by ID
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            Domain: The Domain object
        """
        from msfabricpysdkcore.domain import Domain

        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}"

        domain_dict = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429], error_message = "Error getting domain",
                                           return_format="json")
        domain = Domain.from_dict(domain_dict, self)
        return domain

    def get_domain_by_name(self, domain_name):
        """Method to get a domain by name
        
        Args:
            domain_name (str): The name of the domain
        Returns:
            Domain: The Domain object
        """
        domains = self.list_domains()
        domains = [domain for domain in domains if domain.display_name == domain_name]
        if len(domains) > 0:
            return self.get_domain_by_id(domains[0].id)
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
    
    def list_domain_workspaces(self, domain_id, workspace_objects = False):
        """List workspaces in a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            list: List of Workspace objects
        """

       
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/workspaces"

        workspaces = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429], error_message = "Error listing domain workspaces",
                                          return_format="value_json", paging=True)

        if workspace_objects:
            from msfabricpysdkcore import FabricClientCore
            fc = FabricClientCore(tenant_id=self.tenant_id, client_id=self.client_id, client_secret=self.client_secret)
            workspaces = [fc.get_workspace_by_id(workspace["id"]) for workspace in workspaces]

        return workspaces
    
    def list_domains(self, nonEmptyOnly=False):
        """List all domains in the tenant
        
        Args:
            nonEmptyOnly (bool): Whether to list only non-empty domains
        Returns:
            list: List of Domain objects"""
        from msfabricpysdkcore.domain import Domain

        url = "https://api.fabric.microsoft.com/v1/admin/domains"
        if nonEmptyOnly:
            url = f"{url}?nonEmptyOnly=True"

        resp_dict = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429], error_message = "Error listing domains",
                                         return_format="json")
        domains = resp_dict["domains"]

        domains = [Domain.from_dict(i, self) for i in domains]
        return domains

    def role_assignments_bulk_assign(self, domain_id, type, principals):
        """Assign a role to principals in bulk
        
        Args:
            domain_id (str): The ID of the domain
            type (str): The type of the role assignment
            principals (list): The list of principals
        Returns:
            int: The status code of the response
        """

        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/roleAssignments/bulkAssign"
        body = {
            "type": type,
            "principals": principals
        }

        response: requests.Response = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                           error_message = "Error bulk assigning role assignments",
                                                           return_format="response")

        return response.status_code
    
    def role_assignments_bulk_unassign(self, domain_id, type, principals):
        """Unassign a role from principals in bulk
        
        Args:
            domain_id (str): The ID of the domain
            type (str): The type of the role assignment
            principals (list): The list of principals
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/roleAssignments/bulkUnassign"
        body = {
            "type": type,
            "principals": principals
        }

        response: requests.Response = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                           error_message = "Error bulk unassigning role assignments",
                                                           return_format="response")

        return response.status_code

    def unassign_all_domain_workspaces(self, domain_id):
        """Unassign all workspaces from a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/unassignAllWorkspaces"

        response:requests.Response = self.calling_routine(url = url, operation = "POST", response_codes = [200, 429],
                                                          error_message = "Error unassigning all workspaces",
                                                          return_format="response")
        return response.status_code
    
    def unassign_domain_workspaces_by_ids(self, domain_id, workspace_ids):
        """Unassign workspaces from a domain by workspace IDs
        
        Args:
            domain_id (str): The ID of the domain
            workspace_ids (list): The list of workspace IDs
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/unassignWorkspaces"
        body = {
            "workspacesIds": workspace_ids
        }

        response:requests.Response = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                          error_message = "Error unassigning workspaces by ids",
                                                          return_format="response")

        return response.status_code
    
    def update_domain(self, domain_id, description = None, display_name = None, contributors_scope = None, return_item = False):
        """Method to update a domain
        
        Args:
            domain_id (str): The ID of the domain
        Returns:
            Domain: The Domain object
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}"
        body = {}
        if description:
            body["description"] = description

        if display_name:
            body["displayName"] = display_name

        if contributors_scope:
            body["contributorsScope"] = contributors_scope

        response_json = self.calling_routine(url = url, operation = "PATCH", body = body,
                                             response_codes = [200, 429], error_message = "Error updating domain",
                                             return_format="json")

        if return_item:
            return self.get_domain_by_id(domain_id)
        return response_json

    
    def assign_domain_workspaces_by_capacities(self, domain_id, capacities_ids, wait_for_completion=True):
        """Assign workspaces to a domain by capacities
        
        Args:
            domain_id (str): The ID of the domain
            capacities (list): The list of capacity IDs
            wait_for_completion (bool): Whether to wait for the operation to complete
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/domains/{domain_id}/assignWorkspacesByCapacities"

        body = {
            "capacitiesIds": capacities_ids
        }

        response:requests.Response = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [202, 429],
                                                          error_message = "Error assigning workspaces by capacities", wait_for_completion=wait_for_completion,
                                                          return_format="response")

        return response.status_code
    
    # External Data Share APIs
    
    def list_external_data_shares(self):
        # GET https://api.fabric.microsoft.com/v1/admin/items/externalDataShares
        """List external data shares
        
        Returns:
            list: The list of external data shares
        """
        url = "https://api.fabric.microsoft.com/v1/admin/items/externalDataShares"


        items: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                           error_message = "Error listing external data shares",
                                           return_format="value_json", paging=True)

        return items
    
    def revoke_external_data_share(self, external_data_share_id, item_id, workspace_id):
        """Revoke an external data share
        Args:
            external_data_share_id (str): The ID of the external data share
            item_id (str): The ID of the item
            workspace_id (str): The ID of the workspace
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}/items/{item_id}/externalDataShares/{external_data_share_id}/revoke"

        response:requests.Response = self.calling_routine(url = url, operation = "POST", response_codes = [200, 429],
                                                          error_message = "Error revoking external data share",
                                                          return_format="response")

        return response.status_code

    # Items APIs
    
    def get_item(self, item_id, workspace_id, type = None):
        """Get an item from the workspace
        
        Args:
            item_id (str): The ID of the item
            workspace_id (str): The ID of the workspace
            type (str): The type of the item
        Returns:
            AdminItem: The item object
        """
        from msfabricpysdkcore.admin_item import AdminItem

        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}/items/{item_id}"
        if type:
            url += f"?type={type}"

        response_json: dict = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                                   error_message = "Error getting item", return_format="json")

        return AdminItem.from_dict(response_json, self)
    
    
    def list_item_access_details(self, workspace_id, item_id, type=None):
        """Get the access details of the item
        
        Args:
            workspace_id (str): The ID of the workspace
            item_id (str): The ID of the item
            type (str): The type of the item
        Returns:
            dict: The access details of the item
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}/items/{item_id}/users"

        if type:
            url += f"?type={type}"

        response_json: dict = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                                   error_message = "Error getting item access details", return_format="json")
           
        return response_json
    
    def list_items(self, workspace_id = None, capacity_id = None, type=None,
                   state=None):
        """List all items

        Returns:
            list: The list of items in the workspace
        """
        from msfabricpysdkcore.admin_item import AdminItem

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
                first_parameter = True
        if type:
            if first_parameter:
                url = f"{url}&type={type}"
            else:
                url = f"{url}?type={type}"
                first_parameter = True
        if state:
            if first_parameter:
                url = f"{url}&state={state}"
            else:
                url = f"{url}?state={state}"

        items = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                     error_message = "Error listing items", return_format="itemEntities", paging=True)

        items =  [AdminItem.from_dict(item, self) for item in items]
        return items
    
    # Labels APIs

      
    def bulk_remove_labels(self, items):
        """Remove labels in bulk
        Args:
            items (list): The list of item IDs  
        Returns:
            dict: The response from the API"""

        url = "https://api.fabric.microsoft.com/v1/admin/items/bulkRemoveLabels"

        if len(items) > 2000:
            self.bulk_remove_labels(items[2000:])
            items = items[:2000]
        
        body = {
            "items": items
        }

        response_json: dict = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                   error_message = "Error removing labels", return_format="json")

        return response_json
      
    def bulk_set_labels(self, items, label_id, assignment_method = None, delegated_principal = None):
        """Set labels in bulk
        Args:
            items (list): The list of item IDs
            label_id (str): The ID of the label
            assignment_method (str): The assignment method
            delegated_principal (str): The delegated principal
        Returns:
            dict: The response from the API
        """

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

        response_json: dict = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                   error_message = "Error setting labels", return_format="json")

        return response_json

    # Tenant Settings APIs

    # DELETE https://api.fabric.microsoft.com/v1/admin/capacities/{capacityId}/delegatedTenantSettingOverrides/{tenantSettingName}
    def delete_capacity_tenant_setting_override(self, capacity_id, tenant_setting_name):
        """Delete a tenant setting override at the capacity
        
        Args:
            capacity_id (str): The ID of the capacity
            tenant_setting_name (str): The name of the tenant setting
            
        Returns:
            int: The status code of the response
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/capacities/{capacity_id}/delegatedTenantSettingOverrides/{tenant_setting_name}"

        response:requests.Response = self.calling_routine(url = url, operation = "DELETE", response_codes = [200, 429],
                                                          error_message = "Error deleting capacity tenant setting override",
                                                          return_format="response")

        return response.status_code

    def list_capacities_tenant_settings_overrides(self):
        """Returns list of tenant setting overrides that override at the capacities
        
        Returns:
            list: The capacities tenant settings overrides
        """
        url = "https://api.fabric.microsoft.com/v1/admin/capacities/delegatedTenantSettingOverrides"


        items: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                           error_message = "Error listing capacities tenant settings overrides",
                                           return_format="value", paging=True)

        return items
    
    # GET https://api.fabric.microsoft.com/v1/admin/capacities/{capacityId}/delegatedTenantSettingOverrides?continuationToken={continuationToken}
    def list_capacity_tenant_settings_overrides_by_capacity_id(self, capacity_id):
        """Returns list of tenant setting overrides that override at the capacity
        
        Args:
            capacity_id (str): The ID of the capacity
        Returns:
            list: The capacities tenant settings overrides
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/capacities/{capacity_id}/delegatedTenantSettingOverrides"

        items: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                           error_message = "Error listing capacity tenant settings overrides",
                                           return_format="value", paging=True)

        return items

    # GET https://api.fabric.microsoft.com/v1/admin/domains/delegatedTenantSettingOverrides?continuationToken={continuationToken}
    def list_domain_tenant_settings_overrides(self):
        """Returns list of tenant setting overrides that override at the domains

        Returns:
            list: The domains tenant settings overrides
        """
        url = "https://api.fabric.microsoft.com/v1/admin/domains/delegatedTenantSettingOverrides"

        items: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                           error_message = "Error listing domain tenant settings overrides",
                                           return_format="value", paging=True)

        return items
    
    def list_tenant_settings(self):
        """Get the tenant settings
        
        Returns:
            dict: The tenant settings
        """
        url = "https://api.fabric.microsoft.com/v1/admin/tenantsettings"

        response_json = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                             error_message = "Error getting tenant settings", paging= True, return_format="value")
        return response_json
    
    # GET https://api.fabric.microsoft.com/v1/admin/workspaces/delegatedTenantSettingOverrides?continuationToken={continuationToken}
    def list_workspace_tenant_settings_overrides(self):
        """Returns list of tenant setting overrides that override at the workspaces
        
        Returns:
            list: The workspaces tenant settings overrides
        """
        url = "https://api.fabric.microsoft.com/v1/admin/workspaces/delegatedTenantSettingOverrides"

        items: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                           error_message = "Error listing workspace tenant settings overrides",
                                           return_format="value", paging=True)

        return items
    
    # POST https://api.fabric.microsoft.com/v1/admin/capacities/{capacityId}/delegatedTenantSettingOverrides/{tenantSettingName}/update
    def update_capacity_tenant_setting_override(self, capacity_id, tenant_setting_name, enabled, delegate_to_workspace = None,
                                                enabled_security_groups = None, excluded_security_groups = None):
        """Update a tenant setting override at the capacity
        
        Args:
            capacity_id (str): The ID of the capacity
            tenant_setting_name (str): The name of the tenant setting
            enabled (bool): Whether the tenant setting is enabled
            delegate_to_workspace (bool): Indicates whether the tenant setting can be delegated to a workspace admin. False - Workspace admin cannot override the tenant setting. True - Workspace admin can override the tenant setting.
            enabled_security_groups (list): The list of enabled security groups
            excluded_security_groups (list): The list of excluded security groups
        Returns:
            dict: The overrides
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/capacities/{capacity_id}/delegatedTenantSettingOverrides/{tenant_setting_name}/update"
        body = {
            "enabled": enabled
        }
        if delegate_to_workspace:
            body["delegateToWorkspace"] = delegate_to_workspace
        if enabled_security_groups:
            body["enabledSecurityGroups"] = enabled_security_groups
        if excluded_security_groups:
            body["excludedSecurityGroups"] = excluded_security_groups

        response_json : dict = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                    error_message = "Error updating capacity tenant setting override", return_format="json")

        return response_json

    # POST https://api.fabric.microsoft.com/v1/admin/tenantsettings/{tenantSettingName}/update
    def update_tenant_setting(self, tenant_setting_name, enabled, delegate_to_capacity = None, delegate_to_domain = None,
                              delegate_to_workspace = None, enabled_security_groups = None, excluded_security_groups = None, properties = None):
        """Update a tenant setting

        Args:
            capacity_id (str): The ID of the capacity
            tenant_setting_name (str): The name of the tenant setting
            enabled (bool): Whether the tenant setting is enabled
            delegate_to_capacity (bool): Indicates whether the tenant setting can be delegated to a capacity admin. False - Capacity admin cannot override the tenant setting. True - Capacity admin can override the tenant setting.
            delegate_to_domain (bool): Indicates whether the tenant setting can be delegated to a domain admin. False - Domain admin cannot override the tenant setting. True - Domain admin can override the tenant setting.
            delegate_to_workspace (bool): Indicates whether the tenant setting can be delegated to a workspace admin. False - Workspace admin cannot override the tenant setting. True - Workspace admin can override the tenant setting.
            enabled_security_groups (list): The list of enabled security groups
            excluded_security_groups (list): The list of excluded security groups
        Returns:
            dict: The tenant settings
        """

        url = f"https://api.fabric.microsoft.com/v1/admin/tenantsettings/{tenant_setting_name}/update"

        body = {
            "enabled": enabled
        }
        if delegate_to_capacity:
            body["delegateToCapacity"] = delegate_to_capacity
        if delegate_to_domain:
            body["delegateToDomain"] = delegate_to_domain
        if delegate_to_workspace:
            body["delegateToWorkspace"] = delegate_to_workspace
        if enabled_security_groups:
            body["enabledSecurityGroups"] = enabled_security_groups
        if excluded_security_groups:
            body["excludedSecurityGroups"] = excluded_security_groups
        if properties:
            body["properties"] = properties

        response_json : dict = self.calling_routine(url = url, operation = "POST", body = body, response_codes = [200, 429],
                                                    error_message = "Error updating tenant setting", return_format="json")
        
        return response_json


    
    # Users APIs

    def list_access_entities(self, user_id, type = None):
        """Get the access entities for a user
        
        Args:
            user_id (str): The ID of the user
            type (str): The type of the access entity
        Returns:
            list: The list of access entities
        """

        url = f"https://api.fabric.microsoft.com/v1/admin/users/{user_id}/access"

        if type:
            url = f"{url}?type={type}"

        access_entities: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                                     error_message = "Error getting access entities", return_format="accessEntities", paging=True)
                
        return access_entities

    # Workspaces APIs
    
    def get_workspace(self, workspace_id):
        """Get a workspace by ID
        
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            Workspace: The Workspace object
        """
        from msfabricpysdkcore.admin_workspace import AdminWorkspace

        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}"

        response_json: dict = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                                   error_message = "Error getting workspace", return_format="json")
    
        workspace = AdminWorkspace.from_dict(response_json, self)
        return workspace
    
    # GET https://api.fabric.microsoft.com/v1/admin/workspaces/discoverGitConnections
    def discover_git_connections(self):
        """Discover Git connections
        
        Returns:
            dict: The Git connections
        """
        url = "https://api.fabric.microsoft.com/v1/admin/workspaces/discoverGitConnections"

        response_json = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                             error_message = "Error discovering Git connections", return_format="value_json", paging=True)
        return response_json

    def list_workspace_access_details(self, workspace_id):
        """Get the access details of the workspace
        
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            dict: The access details of the workspace
        """
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}/users"

        response_json = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                             error_message = "Error getting workspace access details", return_format="json")
        return response_json
    

    def list_workspaces(self, capacity_id = None, name=None, state=None, type=None, continuationToken = None):
        """List all workspaces
        
        Args:
            capacity_id (str): The ID of the capacity
        Returns:
            list: List of Workspace objects
        """
        from msfabricpysdkcore.admin_workspace import AdminWorkspace

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
                first_parameter = True

        if name:
            if first_parameter:
                url = f"{url}&name={name}"
            else:
                url = f"{url}?name={name}"
                first_parameter = True
        
        if state:
            if first_parameter:
                url = f"{url}&state={state}"
            else:
                url = f"{url}?state={state}"
                first_parameter = True

        workspaces: list = self.calling_routine(url = url, operation = "GET", response_codes = [200, 429],
                                                error_message = "Error listing workspaces", return_format="workspaces", paging=True)

        workspaces = [AdminWorkspace.from_dict(i, self) for i in workspaces]

        return workspaces
    
    def restore_workspace(self, workspace_id, new_workspace_admin_principal, new_workspace_name = None):
        """Restore a workspace
        
        Args:
            workspace_id (str): The ID of the workspace
        Returns:
            response: The response from the API
        """

        restore_request = {
            "newWorkspaceAdminPrincipal": new_workspace_admin_principal,
            "newWorkspaceName": new_workspace_name
        }
        url = f"https://api.fabric.microsoft.com/v1/admin/workspaces/{workspace_id}/restore"

        response_json = self.calling_routine(url = url, operation = "POST", body = restore_request,
                                             response_codes = [200, 429], error_message = "Error restoring workspace",
                                             return_format="response")

        return response_json

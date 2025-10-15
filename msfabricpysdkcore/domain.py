import json
from msfabricpysdkcore.adminapi import FabricClientAdmin

class Domain:
    """Class to represent a domain in Microsoft Fabric"""

    def __init__(self, id, display_name, description, parent_domain_id, default_label_id, contributors_scope, core_client: FabricClientAdmin):
        """Constructor for the Domain class
        
        Args:
            id (str): The ID of the domain
            display_name (str): The display name of the domain
            description (str): The description of the domain
            parent_domain_id (str): The parent domain ID of the domain
            default_label_id (str): The default label ID of the domain
            contributors_scope (str): The contributors scope of the domain
        Returns:
            Domain: The Domain object created"""

        self.id = id
        self.display_name = display_name
        self.description = description
        self.parent_domain_id = parent_domain_id
        self.default_label_id = default_label_id
        self.contributors_scope = contributors_scope

        self.core_client = core_client

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
            'default_label_id': self.default_label_id,
            'contributors_scope': self.contributors_scope
        }
        return json.dumps(dic, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()

    def from_dict(dic, core_client):
        """Method to create a Domain object from a dictionary
        
        Args:
            dic (dict): The dictionary containing the domain information
        Returns:
            Domain: The Domain object created from the dictionary
        
        """
        if "display_name" not in dic:
            dic["display_name"] = dic["displayName"]
        if "parent_domain_id" not in dic:
            if "parentDomainId" in dic:
                dic["parent_domain_id"] = dic["parentDomainId"]
            else:
                dic["parent_domain_id"] = None
        if "contributors_scope" not in dic:
            if "contributorsScope" in dic:
                dic["contributors_scope"] = dic["contributorsScope"]
            else:
                dic["contributors_scope"] = None
        
        if "default_label_id" not in dic:
            if "defaultLabelId" in dic:
                dic["default_label_id"] = dic["defaultLabelId"]
            else:
                dic["default_label_id"] = None
        
        return Domain(id=dic['id'], display_name=dic['display_name'],
                      description=dic['description'], parent_domain_id=dic['parent_domain_id'], default_label_id=dic.get('default_label_id', None),
                      contributors_scope=dic.get('contributors_scope', None), core_client=core_client)

    def list_domain_workspaces(self, workspace_objects = False):
        """Method to list the workspaces in the domain
        
        Args:
            continuationToken (str): The continuation token to use for pagination
        Returns:
            list: The list of workspaces in the domain
        """
        return self.core_client.list_domain_workspaces(self.id, workspace_objects)
    
    def delete(self):
        """Method to delete the domain

        Returns:
            int: The status code of the response
        """
        return self.core_client.delete_domain(self.id)
    

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

        resp_dict = self.core_client.update_domain(self.id, description, display_name, contributors_scope)
        assert "id" in resp_dict
        self.description = description
        self.display_name = display_name
        self.contributors_scope = contributors_scope

        return self
    
    def assign_workspaces_by_capacities(self, capacities_ids, wait_for_completion=True):
        """Method to assign workspaces to the domain based on capacities_ids
        
        Args:
            capacities_ids (list): The list of capacitiy ids to assign workspaces
        Returns:
            int: The status code of the response
        """
        # POST https://api.fabric.microsoft.com/v1/admin/domains/{domainId}/assignWorkspacesByCapacities
        return self.core_client.assign_domain_workspaces_by_capacities(self.id, capacities_ids, wait_for_completion)


    def assign_workspaces_by_ids(self, workspaces_ids):

        """Method to assign workspaces to the domain based on workspaces_ids
        
        Args:
            workspaces_ids (list): The list of workspace ids to assign workspaces
        Returns:
            int: The status code of the response
        """
        return self.core_client.assign_domain_workspaces_by_ids(self.id, workspaces_ids)
    

    def assign_workspaces_by_principals(self, principals, wait_for_completion=True):
        """Method to assign workspaces to the domain based on principals
        
        Args:
            principals (list): The list of principals to assign workspaces
        Returns:
            int: The status code of the response
        """
        return self.core_client.assign_domains_workspaces_by_principals(self.id, principals, wait_for_completion)
    
    def role_assignments_bulk_assign(self, type, principals):
        """Method to bulk assign role assignments
        
        Args:
            type (str): The type of the role assignment
            principals (list): The list of principals to assign the role
        Returns:
            int: The status code of the response
        """
        return self.core_client.role_assignments_bulk_assign(self.id, type, principals)
    

    def role_assignments_bulk_unassign(self, type, principals):
        """Method to bulk unassign role assignments
        
        Args:
            type (str): The type of the role assignment
            principals (list): The list of principals to unassign the role
        Returns:
            int: The status code of the response
        """
        
        return self.core_client.role_assignments_bulk_unassign(self.id, type, principals)
    

    def unassign_all_workspaces(self):
        """Method to unassign all workspaces from the domain
        
        Returns:
            int: The status code of the response
        """
        return self.core_client.unassign_all_domain_workspaces(self.id)
    
    def unassign_workspaces_by_ids(self, workspace_ids):
        """Method to unassign workspaces from the domain
        
        Args:
            workspace_ids (list): The list of workspace ids to unassign
        Returns:
            int: The status code of the response
        """
        return self.core_client.unassign_domain_workspaces_by_ids(self.id, workspace_ids)
    
    def list_role_assignments(self):
        """Method to list role assignments in the domain
        
        Returns:
            list: The list of role assignments in the domain
        """
        return self.core_client.list_role_assignments(domain_id=self.id)
    
    def sync_role_assignments_to_subdomains(self, role):
        """Method to sync role assignments to subdomains
        
        Args:
            role (str): The role to sync
        Returns:
            int: The status code of the response
        """
        return self.core_client.sync_role_assignments_to_subdomains(self.id, role)

from warnings import warn

from msfabricpysdkcore.client import FabricClient


class FabricAzureClient(FabricClient):

    def __init__(self, tenant_id=None, client_id=None, client_secret=None, silent=None) -> None:
        super().__init__(scope = "https://management.azure.com/.default",
                         tenant_id = tenant_id,
                         client_id = client_id,
                         client_secret = client_secret,)

        if silent is not None:
            warn("The 'silent' parameter is deprecated and will be removed in a future version.", DeprecationWarning, stacklevel=2)


    def check_name_availability(self, subscription_id, location, name, type = "Microsoft.Fabric/capacities"):
        """Check name availability
        Args:
            subscription_id (str): The subscription ID
            location (str): The location
            name (str): The name
            type (str): The type
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Fabric/locations/{location}/checkNameAvailability?api-version=2023-11-01"

        body = {
            "name": name,
            "type": type
        }

        response = self.calling_routine(url=url, operation="POST", body=body, response_codes=[200], return_format="json", error_message="Failed to check name availability")
        return response

    def create_or_update_capacity(self, subscription_id, resource_group_name, capacity_name, location, properties_administration, sku, tags = None):
        """Create or update capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
            location (str): The location
            properties_administration (dict): The administration properties
            sku (dict): The sku
            tags (dict): The tags
        Returns:
            FabricAzureCapacity: The capacity
        """
        from msfabricpysdkcore.fabric_azure_capacity import FabricAzureCapacity

        if sku and "name" in sku:
            sku = sku["name"]

        body = {
            "location": location,
            "properties": {
                "administration": properties_administration
            },
            "sku": {"name": sku,
                    "tier": "Fabric"}
        }

        if tags is not None:
            body["tags"] = tags
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="PUT", body=body, response_codes=[200, 201], return_format="json", error_message="Failed to create or update capacity")
        response["subscription_id"] = subscription_id
        response["resource_group_name"] = resource_group_name

        return FabricAzureCapacity.from_dict(response, self)


    def delete_capacity(self, subscription_id, resource_group_name, capacity_name):
        """Delete capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="DELETE", response_codes=[202], return_format="response", error_message="Failed to delete capacity")
        return response


    def get_capacity(self, subscription_id, resource_group_name, capacity_name):
        """Get capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
        Returns:
            FabricAzureCapacity: The capacity
        """
        from msfabricpysdkcore.fabric_azure_capacity import FabricAzureCapacity

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="GET", response_codes=[200], return_format="json", error_message="Failed to get capacity")
        response["subscription_id"] = subscription_id
        response["resource_group_name"] = resource_group_name

        return FabricAzureCapacity.from_dict(response, self)

    def list_by_resource_group(self, subscription_id, resource_group_name):
        """List capacities by resource group
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="GET", response_codes=[200], return_format="value_json", error_message="Failed to list capacities by resource group")
        return response


    def list_by_subscription(self, subscription_id):
        """List capacities by subscription
        Args:
            subscription_id (str): The subscription ID
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Fabric/capacities?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="GET", response_codes=[200], return_format="value_json", error_message="Failed to list capacities by subscription")
        return response

    def list_skus(self, subscription_id):
        """List skus
        Args:
            subscription_id (str): The subscription ID
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Fabric/skus?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="GET", response_codes=[200], return_format="value_json", error_message="Failed to list skus")
        return response
    
    def list_skus_for_capacity(self, subscription_id, resource_group_name, capacity_name):
        """List skus for capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}/skus?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="GET", response_codes=[200], return_format="value_json", error_message="Failed to list skus for capacity")
        return response

    def resume_capacity(self, subscription_id, resource_group_name, capacity_name):
        """Resume capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}/resume?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="POST", response_codes=[202], return_format="response", error_message="Failed to resume capacity")
        return response

    def suspend_capacity(self, subscription_id, resource_group_name, capacity_name):
        """Suspend capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
        Returns:
            dict: The response
        """

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}/suspend?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="POST", response_codes=[202], return_format="response", error_message="Failed to suspend capacity")
        return response
    
    def update_capacity(self, subscription_id, resource_group_name, capacity_name, properties_administration = None, sku = None, tags = None):
        """Update capacity
        Args:
            subscription_id (str): The subscription ID
            resource_group_name (str): The resource group name
            capacity_name (str): The capacity name
            body (dict): The body of the request
        Returns:
            FabricAzureCapacity: The capacity
        """
        from msfabricpysdkcore.fabric_azure_capacity import FabricAzureCapacity

        body = {}
        if sku and "name" in sku:
            sku = sku["name"]

        if properties_administration is not None:
            body["properties"] = {}
            body["properties"]["administration"] = properties_administration

        if sku is not None:
            body["sku"] = {"name": sku,
                           "tier": "Fabric"}
        
        if tags is not None:
            body["tags"] = tags

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Fabric/capacities/{capacity_name}?api-version=2023-11-01"

        response = self.calling_routine(url=url, operation="PATCH", body=body, response_codes=[200, 202],
                                        return_format="json", error_message="Failed to update capacity")
        response["subscription_id"] = subscription_id
        response["resource_group_name"] = resource_group_name

        return FabricAzureCapacity.from_dict(response, self)

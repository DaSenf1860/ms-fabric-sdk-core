import json 

class Capacity:
    """Class to represent a capacity in Microsoft Fabric"""


    def __init__(self, id, display_name, sku, region, state):
        """Constructor for the Capacity class
        
        Args:
            id (str): The ID of the capacity
            display_name (str): The display name of the capacity
            sku (str): The SKU of the capacity
            region (str): The region of the capacity
            state (str): The state of the capacity
        
        Returns:
            Capacity: The Capacity object created
        """
        self.id = id
        self.display_name = display_name
        self.sku = sku
        self.region = region
        self.state = state

    def __str__(self):
        """Method to return a string representation of the Capacity object
        
        Returns:
            str: The string representation of the Capacity object
        """
        dic = {
            'id': self.id,
            'display_name': self.display_name,
            'sku': self.sku,
            'region': self.region,
            'state': self.state
        }
        return json.dumps(dic, indent=2)

    def from_dict(dic):
        """Method to create a Capacity object from a dictionary
        
        Args:
            dic (dict): The dictionary containing the capacity information
        Returns:
            Capacity: The Capacity object created from the dictionary
        
        """
        if "display_name" not in dic:
            dic["display_name"] = dic["displayName"]
        return Capacity(dic['id'], dic['display_name'], dic['sku'], dic['region'], dic['state'])
        
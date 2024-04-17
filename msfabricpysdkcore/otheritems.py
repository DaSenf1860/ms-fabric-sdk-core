from time import sleep

from msfabricpysdkcore.item import Item

class SparkJobDefinition(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class Warehouse(Item):
    """Class to represent a warehouse in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class KQLDatabase(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class KQLQueryset(Item):
    """Class to represent a kql database in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class Eventstream(Item):
    """Class to represent a eventstream in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class MLExperiment(Item):
    """Class to represent a ml experiment in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class MLModel(Item):
    """Class to represent a ml model in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class Notebook(Item):
    """Class to represent a notebook in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class Report(Item):
    """Class to represent a report in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class SemanticModel(Item):
    """Class to represent a semantic model in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

class DataPipeline(Item):
    """Class to represent a spark job definition in Microsoft Fabric"""
     
    def __init__(self, id, display_name, type, workspace_id, auth, properties = None, definition=None, description=""):
        super().__init__(id, display_name, type, workspace_id, auth, properties, definition, description)

    def run_on_demand_item_job(self, execution_data=None):
        return super().run_on_demand_item_job(job_type = "Pipeline", execution_data=execution_data)
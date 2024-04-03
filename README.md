# A Python SDK for Microsoft Fabric

This is a Python SDK for Microsoft Fabric. It is a wrapper around the REST APIs of Fabric*.

![Python hugging a F](assets/fabricpythontransparent.png)

The Microsoft Fabric REST APIs are documented [here](https://docs.microsoft.com/en-us/rest/api/fabric/).
They are designed to automate your Fabric processes.

This SDK helps to interact with the Fabric APIs in a more Pythonic way.
Additionally it brings some extra features like:
- Authentication is handled for you (currently Azure CLI Authentication  and Service Principal Authentication are supported)
- Waiting for completion of long running operations
- Retry logic when hitting the API rate limits
- Referencing objects by name instead of ID
- More granular objects, e.g. a Workspace and Item object instead of referencing IDs all the time
- Do bulk operations**
- Pagination support**

Currently it supports all Core APIs, i.e.:
- [Capacities](#working-with-capacities)
- [Git](#working-with-git)
- [Items](#working-with-items)
- [Job Scheduler](#working-with-job-scheduler)
- Long Running Operations
- [OneLakeShortcuts](#working-with-one-lake-shortcuts)
- [Workspaces](#working-with-workspaces)

It is planned to support also the Admin and Lakehouse APIs and new APIs which are not released yet.
Eventually Power BI APIs like the Scanner API will be covered as well.

*Because this SDK uses the API in the background, all limitations and restrictions of the API apply to this SDK as well. This includes rate limits, permissions, etc.

**These features are not yet implemented but are planned for the near future.



## Installation

```bash
pip install msfabricpysdkcore
```


## Usage


### Client initialization and authentication
```python
from msfabricpysdkcore import FabricClientCore

# Create a client

# Either login with the Azure CLI first and initiate the client directly
fc = FabricClientCore()

# Or use a service principal (note that not all APIs are supported with service principal)
# You can also use environment variables to set the service principal id and secret. The environment variables are:
# FABRIC_CLIENT_ID
# FABRIC_CLIENT_SECRET
# FABRIC_TENANT_ID

fc = FabricClientCore(tenant_id = "tenant_id",
                      client_id = "your_service_principal_id",
                      client_secret = "your_service_principal_secret")


```

### Working with workspaces
    
```python
# Create a workspace
ws_created = fc.create_workspace(display_name="testworkspace",
                                 description="test workspace", 
                                 exists_ok=False)


# Get a workspace by id
workspace_id = ws_created.id
ws = fc.get_workspace_by_id(id = workspace_id)


# Get a workspace by name
workspace_name = ws_created.display_name
ws = fc.get_workspace_by_name(name = workspace_name)


# List workspaces
result = fc.list_workspaces()
for ws in result:
    print(ws)


# Update workspace
fc.update_workspace(workspace_id=ws.id,                          
                    display_name="newname8912389u1293", 
                    description="new description")
# or
ws.update(display_name="newname8912389u1293", 
          description="new description")


# Delete workspace
fc.delete_workspace(workspace_id="workspace_id")
# or
ws.delete()

    
 # Add workspace role assignment
fc.add_workspace_role_assignment(workspace_id = ws.id,
                                 principal = {"id" : "abadfbafb",
                                              "type" : "ServicePrincipal"},
                                 role = 'Member')
# or
ws.add_role_assignment(principal = {"id" : "abadfbafb",
                                    "type" : "ServicePrincipal"},
                       role = 'Member')

 
 # Get workspace role assignments
fc.get_workspace_role_assignments(workspace_id = ws.id)
# or
ws.get_role_assignments()


# Update workspace role assignment
fc.update_workspace_role_assignment(workspace_id = ws.id, 
                                    role = "Contributor", 
                                    principal_id = "abadfbafb")
# or
ws.update_role_assignment(role = "Contributor", 
                          principal_id = "abadfbafb")


# Delete workspace role assignment
fc.delete_workspace_role_assignment(workspace_id = ws.id,
                                    principal_id = "abadfbafb")
# or
ws.delete_role_assignment(principal_id = "abadfbafb")

```

### Working with capacities

```python

# Assign a capaycity to a workspace
fc.assign_to_capacity(workspace_id=workspace_id,
                      capacity_id="capacityid123123")
# or
ws.assign_to_capacity(capacity_id="capacityid123123")      

# Unassign from capacity
fc.unassign_from_capacity(workspace_id=ws.id)
# or
ws.unassign_from_capacity()


# List capacities
fc.list_capacities()
```

### Working with items

```python

# Create an item
fc.create_item(display_name="item_name", type="Lakehouse", workspace_id="workspace_id", definition = None, description = None) 
# or
ws.create_item(display_name="item_name", type="Lakehouse", definition = None, description = None)


# Get an item
item = fc.get_item(workspace_id="workspace_id", item_id="item_id")
# or
item = ws.get_item(item_id="item_id") 


# List items
item_list = fc.list_items(workspace_id="workspace_id")
# or
item_list = ws.list_items()


# Update an item
fc.update_item(workspace_id="workspace_id", item_id="item_id" display_name="new_item_name", description = None)
# or
ws.update_item(item_id="item_id", display_name="new_item_name", description = None)
# or
item.update(display_name="new_item_name", description = None)


# Delete an item
fc.delete_item(workspace_id="workspace_id", item_id="item_id")
# or
ws.delete_item(item_id="item_id")
# or
item.delete()

```

### Working with Git

```python

# Connect to a git repository

git_provider_details = {'organizationName': 'dasenf1860',
                'projectName': 'fabrictest',
                'gitProviderType': 'AzureDevOps',
                'repositoryName': 'fabrictest',
                'branchName': 'main',
                'directoryName': '/folder1'}

fc.git_connect(workspace_id="workspaceid", git_provider_details=git_provider_details)
# or
ws.git_connect(git_provider_details=git_provider_details)


# Initialize a git connection

initialization_strategy = "PreferWorkspace"

fc.git_initialize_connection(workspace_id="workspaceid", initialization_strategy=initialization_strategy)
# or
ws.git_initialize_connection(initialization_strategy=initialization_strategy)


# Get git connection details
fc.git_get_connection(workspace_id="workspaceid")
# or
ws.git_get_connection()


# Get git status
fc.git_get_status(workspace_id="workspaceid")
# or
ws.git_get_status()


# Update from git
fc.update_from_git(workspace_id="workspaceid", remote_commit_hash="commit_hash", 
                   conflict_resolution = None, options = None, workspace_head = None)
# or
ws.update_from_git(remote_commit_hash="commit_hash", conflict_resolution = None, options = None, workspace_head = None)


# Commit to git
fc.commit_to_git(workspace_id="workspaceid", mode = "All", comment="commit message", items=None, workspace_head=None)
# or
ws.commit_to_git(mode = "All", comment="commit message", items=None, workspace_head=None)


# Disconnect from git
fc.git_disconnect(workspace_id="workspaceid")
# or
ws.git_disconnect()

``` 	

### Working with one lake shortcuts

```python

# Create a shortcut
fc.create_shortcut(workspace_id="workspace_id",
                   item_id="item_id",
                   path="path",
                   name="name",
                   target={"oneLake": {"itemId": "item_id_target",
                                       "path": "path_target",
                                       "workspaceId": "workspace_id_target"}})
# or
ws.create_shortcut(item_id="item_id",
                   path="path",
                   name="name",
                   target={"oneLake": {"itemId": "item_id_target",
                                       "path": "path_target",
                                       "workspaceId": "workspace_id_target"}})
# or 
item.create_shortcut(path="path",
                     name="name",
                     target={"oneLake": {"itemId": "item_id_target",
                                       "path": "path_target",
                                       "workspaceId": "workspace_id_target"}})


# Get a shortcut
shortcut = fc.get_shortcut(workspace_id="workspace_id",
                           item_id="item_id",
                           path="path",
                           name="name")
# or
shortcut = ws.get_shortcut(item_id="item_id",
                           path="path",
                           name="name")
# or
shortcut = item.get_shortcut(path="path",
                             name="name")


# Delete a shortcut
fc.delete_shortcut(workspace_id="workspace_id",
                   item_id="item_id",
                   path="path",
                   name="name")
# or
ws.delete_shortcut(item_id="item_id",
                   path="path",
                   name="name")
# or
item.delete_shortcut(path="path",
                   name="name")

```


### Working with job scheduler

```python

# Run a on demand item job
fc.run_on_demand_item_job(workspace_id="workspace_id", item_id="item_id", job_type="RunNotebook", execution_data = None)
# or
ws.run_on_demand_item_job(item_id="item_id", job_type="RunNotebook", execution_data = None)
# or
item.run_on_demand_item_job(job_type="RunNotebook", execution_data = None)


# Get an item job instance
fc.get_item_job_instance(workspace_id="workspace_id", item_id="item_id", job_instance_id="job_instance_id")
# or
ws.get_item_job_instance(item_id="item_id", job_instance_id="job_instance_id")
# or
item.get_item_job_instance(job_instance_id="job_instance_id")

# Cancel an item job instance
fc.cancel_item_job_instance(workspace_id="workspace_id", item_id="item_id", job_instance_id="job_instance_id")
# or
ws.cancel_item_job_instance(item_id="item_id", job_instance_id="job_instance_id")
# or 
item.cancel_item_job_instance(job_instance_id="job_instance_id")

```



Note: This SDK is not an official SDK from Microsoft. It is a community project and not supported by Microsoft. Use it at your own risk.
Also the API is still in preview and might change. This SDK is not yet feature complete and might not cover all APIs yet. Feel free to contribute to this project to make it better.
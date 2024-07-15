# Python SDK for Microsoft Fabric

This is a Python SDK for Microsoft Fabric. It is a wrapper around the REST APIs (v1) of Fabric*.
It supports all REST APIs of Fabric (as of July 15, 2024)

![Python hugging a F](assets/fabricpythontransparent.png)

The Microsoft Fabric REST APIs are documented [here](https://docs.microsoft.com/en-us/rest/api/fabric/).
They are designed to automate your Fabric processes.

This SDK helps to interact with the Fabric APIs in a more Pythonic way.
Additionally it brings some extra features like:
- Authentication is handled for you (currently Azure CLI Authentication, Authentication from a Microsoft Fabric notebook and Service Principal Authentication are supported)
- Waiting for completion of long running operations
- Retry logic when hitting the API rate limits
- Referencing objects by name instead of ID
- More granular objects, e.g. a Workspace and Item object instead of referencing IDs all the time
- Do bulk operations (see [Usage Patterns](usage_patterns.md))
- Pagination support

See the latest release notes [here](releasenotes/release_notes.md).

Currently it supports all Core APIs, Admin APIs, Lakehouse APIs and all other item specific CRUD APIs, i.e.:
- Core APIs
  - [Capacities](#working-with-capacities)
  - [Deployment Pipelines](#deployment-pipelines)
  - [External Data Shares](#external-data-shares)
  - [Git](#working-with-git)
  - [Items](#working-with-items)
  - [Job Scheduler](#working-with-job-scheduler)
  - [Long Running Operations](#long-running-operations)
  - [OneLakeDataAccessSecurity](#one-lake-data-access-security)
  - [OneLakeShortcuts](#working-with-one-lake-shortcuts)
  - [Workspaces](#working-with-workspaces)
- Admin APIs
  - [Domains](#admin-api-for-domains)
  - [External Data Shares](#admin-api-for-external-data-shares)
  - [Items](#admin-api-for-items)
  - [Labels](#admin-api-for-labels)
  - [Tenants](#admin-api-for-tenants)
  - [Users](#admin-api-for-users)
  - [Workspaces](#admin-api-for-workspaces)
- [Item Specific APIs](item_specific_apis.md), e.g.
  - List, create, update, delete warehouses, notebooks, semantic models, kql databases,.....
  - Lakehouse operations (Load table, list tables, run table maintenance)
  - Spark Pool operations

It is planned to support also new APIs which are not released yet.
Also we have plans to support APIs to interact with Fabric capacities on the Azure Side.
Eventually Power BI APIs like the Scanner API will be covered as well.

*Because this SDK uses the API in the background, all limitations and restrictions of the API apply to this SDK as well. This includes rate limits, permissions, etc.




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
# This also works directly in a Microsoft Fabric notebook
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

 
 # List workspace role assignments
fc.list_workspace_role_assignments(workspace_id = ws.id)
# or
ws.list_role_assignments()


# Get workspace role assignment
fc.get_workspace_role_assignment(workspace_id = ws.id, 
                                 workspace_role_assignment_id = "dagdasf")  
# or
ws.get_role_assignment(workspace_role_assignment_id = "fsgdg")

# Update workspace role assignment
fc.update_workspace_role_assignment(workspace_id = ws.id, 
                                    role = "Contributor", 
                                    workspace_role_assignment_id = "abadfbafb")
# or
ws.update_role_assignment(role = "Contributor", 
                          workspace_role_assignment_id = "abadfbafb")


# Delete workspace role assignment
fc.delete_workspace_role_assignment(workspace_id = ws.id,
                                    workspace_role_assignment_id = "abadfbafb")
# or
ws.delete_role_assignment(workspace_role_assignment_id = "abadfbafb")


# Provision Identity
result = fc.provision_identity(workspace_id=ws.id)
print(result["applicationId"]))

# Deprovision Identity
fc.deprovision_identity(workspace_id=ws.id)

```

### Working with capacities

```python


capacity_object = fc.get_capacity(capacity_id = "0129389012u8938491") 
#or 
capacity_object = fc.get_capacity(capacity_name = "sandboxcapacitygermanywc") 

# Assign a capaycity to a workspace
fc.assign_to_capacity(workspace_id=workspace_id,
                      capacity_id=capacity_object.id)
# or
ws.assign_to_capacity(capacity_id=capacity_object.id)      

# Unassign from capacity
fc.unassign_from_capacity(workspace_id=ws.id)
# or
ws.unassign_from_capacity()


# List capacities
fc.list_capacities()
```

### Deployment Pipelines

```python


# List deployment pipelines 

depl_pipes = fc.list_deployment_pipelines()

pipe = [pipe for pipe in depl_pipes if pipe.display_name == 'sdkpipe'][0]
pipe_id = pipe.id

# Get a deployment pipeline
pipe = fc.get_deployment_pipeline(pipe_id)


# Get deployment pipeline stages
stages = fc.list_deployment_pipeline_stages(pipe_id)

names = [stage.display_name for stage in stages]

dev_stage = [stage for stage in stages if stage.display_name == "Development"][0]
prod_stage = [stage for stage in stages if stage.display_name == "Production"][0]

# Get deployment pipeline stages items
items = fc.list_deployment_pipeline_stages_items(pipeline_id=pipe_id, stage_id=dev_stage.id)


items = [item for item in dev_stage.get_items() if item["itemDisplayName"] == 'cicdlakehouse']
item = items[0]
item = {"sourceItemId": item["itemId"],
        "itemType": item["itemType"]}
items = [item]

# Deploy stage content
response = pipe.deploy(source_stage_id=dev_stage.id,target_stage_id=prod_stage.id, items=items)

```

### External Data Shares

```python
from msfabricpysdkcore.coreapi import FabricClientCore

fc = FabricClientCore()

workspace_id = 'yxcvyxcvyxcv'
item_id = 'sdfsdfsdfsf'


# Create

recipient = {
    "userPrincipalName": "lisa4@fabrikam.com"
}
paths=["Files/external"]

data_share = fc.create_external_data_share(workspace_id, item_id, paths, recipient)

# Get

data_share2 = fc.get_external_data_share(workspace_id, item_id, data_share['id'])

# List

data_share_list = fc.list_external_data_shares_in_item(workspace_id, item_id)

data_share_ids = [ds['id'] for ds in data_share_list]

# Revoke

response_code = fc.revoke_external_data_share(workspace_id, item_id, data_share['id'])

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
fc.update_item(workspace_id="workspace_id", item_id="item_id" display_name="new_item_name", description = None, return_item=True)
# or
ws.update_item(item_id="item_id", display_name="new_item_name", description = None, return_item=True)
# or
item.update(display_name="new_item_name", description = None, return_item=True)


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

# Other job types are e.g.:
jobType=Pipeline


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


### Long Running Operations

```python

# Get the state of an operation

operation_id = "801783df0123gsdgsq80"

state = fc.get_operation_state(operation_id)

# Get the results of an operation

results = fc.get_operation_results(operation_id)

```

### One Lake Data Access Security

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore() 

workspace_id = "d8aafgasdsdbe5"
item_id = "503hsdfhs48364"

# List 

resp = fc.list_data_access_roles(workspace_id=workspace_id, item_id=item_id)

roles = resp[0]
etag = resp[1]


# Create or Update

role1 = roles[1]

item_access = role1["members"]["fabricItemMembers"][0]['itemAccess']
+
if 'ReadAll' in item_access:
    item_access = ['Read', 'Write', 'Execute']
else:
    item_access.append('ReadAll')

role1["members"]["fabricItemMembers"][0]['itemAccess'] = item_access
roles[1] = role1

resp = fc.create_or_update_data_access_roles(workspace_id=workspace_id, 
                                              item_id=item_id, 
                                              data_access_roles=roles, 
                                              etag_match={"If-Match":etag})

```

### Admin API for Workspaces

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()


# List workspaces
ws = fca.list_workspaces(name="testworkspace")[0]

# Get workspace
ws = fca.get_workspace(workspace_id="workspace_id")

# Get workspace access details

ws_access = fca.list_workspace_access_details("workspace_id")
# or
ws_access = ws.list_access_details()
```

### Admin API for Users

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# Get access entities

user_id = 'b4fuhaidc2'
access_entities = fca.list_access_entities(user_id, type="Notebook")

```

### Admin API for Tenants

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# Get tenant settings

tenant_settings = fca.list_tenant_settings()

# Get capacity tenant settings overrides

overrides = fca.list_capacities_tenant_settings_overrides()

```

### Admin API for Items

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# List items

item_list = fca.list_items(workspace_id="wsid")

# Get item

item = fca.get_item(workspace_id="wsid", item_id=item_list[0].id)
# or
item = ws.get_item(item_id=item_list[0].id)

# Get item access details

item_access = fca.list_item_access_details(workspace_id="wsid", item_id=item_list[0].id)
#or
item_access = ws.list_item_access_details(item_id=item_list[0].id)
# or
item_access = item.get_access_details()

```

### Admin API for Labels

```python

from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

items = [{"id": "d417b843534cf0-23423523", "type": "Lakehouse"}]
label_id = "de8912714345d2" # to be found in Microsoft Purview Compliance Center

# Bulk set labels 

resp = fca.bulk_set_labels(items=items, label_id=label_id)

# Bulk remove labels

resp = fca.bulk_remove_labels(items=items)

```


### Admin API for Domains

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# Create domain
domain_name = "sdktestdomains"
domain = fca.create_domain(display_name=domain_name)

# Get domain by name
domain_clone = fca.get_domain_by_name(domain_name)

# Get domain by id
domain_clone = fca.get_domain_by_id(domain.id)

# List domains
domains = fca.list_domains()

# Update domain
domain_new_name = "sdktestdomains2"
domain_clone = fca.update_domain(domain.id, display_name=domain_new_name, return_item=True)

# Assign domain workspaces by Ids
fca.assign_domain_workspaces_by_ids(domain.id, ["workspace_id_1", "workspace_id_2"])

# List domain workspaces
workspaces = fca.list_domain_workspaces(domain.id, workspace_objects=True)

# Unassign domain workspaces by ids
status_code = fca.unassign_domain_workspaces_by_ids(domain.id, ["workspace_id_1", "workspace_id_2"])

# Assign domain workspaces by capacities
status_code = fca.assign_domain_workspaces_by_capacities(domain.id, ["cap_id1", "cap_id2"])

# Unassign all domain workspaces
status_code = fca.unassign_all_domain_workspaces(domain.id)

# Assign domain workspaces by principals
principal1 = {'id': '6edbsdfbfdgdf656', 'type': 'User'}
principal2 = {'id': '6eyxcbyyxc57', 'type': 'User'}

status_code = fca.assign_domains_workspaces_by_principals(domain.id, [principal1, principal2], wait_for_completion=True)

# Role assignments bulk assign

principals = [principal, principal_2]
status_code = fca.role_assignments_bulk_assign(domain.id, "Contributors", principals)

# Role assignments bulk unassign
status_code = fca.role_assignments_bulk_unassign(domain.id, "Contributors", [principal_2])

# Delete domain
status_code = fca.delete_domain(domain.id)
```

### Admin API for External Data Shares

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# List external data shares

data_shares = fca.list_external_data_shares()
ws = fca.list_workspaces(name="testworkspace")[0]

data_shares = [d for d in data_shares if d['workspaceId'] == ws.id]

# Revoke external data share

fca.revoke_external_data_share(external_data_share_id = data_shares[0]['id'], 
                                item_id = data_shares[0]['itemId'], 
                                workspace_id = data_shares[0]['workspaceId'])


```


Note: This SDK is not an official SDK from Microsoft. It is a community project and not supported by Microsoft. Use it at your own risk.
Also the API is still in preview and might change. This SDK is not yet feature complete and might not cover all APIs yet. Feel free to contribute to this project to make it better.

# Python SDK for Microsoft Fabric

This is a Python SDK for Microsoft Fabric. It is a wrapper around the REST APIs (v1) of Fabric*. It supports all Fabric REST APIs as well as Azure Resource Management APIs for Fabric (as of October 10, 2025).

![Python hugging a F](assets/fabricpythontransparent.png)

<a href="https://badgen.net/github/license/DaSenf1860/ms-fabric-sdk-core" target="_blank">
    <img src="https://badgen.net/github/license/DaSenf1860/ms-fabric-sdk-core" alt="License">
</a>
<a href="https://badgen.net/github/releases/DaSenf1860/ms-fabric-sdk-core" target="_blank">
    <img src="https://badgen.net/github/releases/DaSenf1860/ms-fabric-sdk-core" alt="Test">
</a>
<a href="https://badgen.net/github/contributors/DaSenf1860/ms-fabric-sdk-core" target="_blank">
    <img src="https://badgen.net/github/contributors/DaSenf1860/ms-fabric-sdk-core" alt="Publish">
</a>
<a href="https://badgen.net/github/commits/DaSenf1860/ms-fabric-sdk-core" target="_blank">
    <img src="https://badgen.net/github/commits/DaSenf1860/ms-fabric-sdk-core" alt="Commits">
</a>
<a href="https://badgen.net/pypi/v/msfabricpysdkcore" target="_blank">
    <img src="https://badgen.net/pypi/v/msfabricpysdkcore" alt="Package version">
</a>
  <a href="https://badgen.net/pypi/dm/msfabricpysdkcore" target="_blank">
    <img src="https://badgen.net/pypi/dm/msfabricpysdkcore" alt="Monthly Downloads">
</a>

<p>    </p>


The Microsoft Fabric REST APIs are documented [here](https://docs.microsoft.com/en-us/rest/api/fabric/).
The Azure Resoure Management APIs for Fabric are documented [here](https://learn.microsoft.com/en-us/rest/api/microsoftfabric/fabric-capacities?view=rest-microsoftfabric-2023-11-01).
They are designed to automate your Fabric processes.

This SDK helps to interact with the Fabric APIs in a more Pythonic way.
Additionally it brings some extra features like:
- Authentication is handled for you, the following is supported:
  - Azure CLI Authentication
  - Authentication from a Microsoft Fabric notebook
  - Service Principal Authentication
  - MSALConfidentialClientApplicationAuthentication
- Waiting for completion of long running operations
- Retry logic when hitting the API rate limits
- Referencing objects by name instead of ID
- More granular objects, e.g. a Workspace and Item object instead of referencing IDs all the time
- Do bulk operations (see [Usage Patterns](usage_patterns.md))
- Pagination support

See the latest release notes [here](releasenotes/release_notes.md).

Currently it supports all Core APIs, Admin APIs, all item specific CRUD APIs and Azure Resource Management APIs for Fabric capacities, i.e.:
- Core APIs
  - [Capacities](#working-with-capacities)
  - [Connections](#connections)
  - [Deployment Pipelines](#deployment-pipelines)
  - [External Data Shares Provider](#external-data-shares-provider)
  - [External Data Shares Recipient](#external-data-shares-recipient)
  - [Folders](#folders)
  - [Gateways](#gateways)
  - [Git](#working-with-git)
  - [Items](#working-with-items)
  - [Job Scheduler](#working-with-job-scheduler)
  - [Managed Private Endpoints](#managed-private-endpoints)
  - [Long Running Operations](#long-running-operations)
  - [OneLakeDataAccessSecurity](#one-lake-data-access-security)
  - [OneLakeShortcuts](#working-with-one-lake-shortcuts)
  - [Tags](#tags)
  - [Workspaces](#working-with-workspaces)
- Admin APIs
  - [Domains](#admin-api-for-domains)
  - [External Data Shares](#admin-api-for-external-data-shares)
  - [Items](#admin-api-for-items)
  - [Labels](#admin-api-for-labels)
  - [Tags](#admin-api-for-tags)
  - [Tenants](#admin-api-for-tenants)
  - [Users](#admin-api-for-users)
  - [Workspaces](#admin-api-for-workspaces)
- [Item Specific APIs](item_specific_apis.md), e.g.
  - List, create, update, delete warehouses, notebooks, semantic models, kql databases,.....
  - Lakehouse operations (Load table, list tables, run table maintenance)
  - Spark Pool operations
- [Azure Resource Management APIs for Fabric capacities](#azure-resource-management-apis-for-fabric-capacities)
- [Logging](#logging)

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
### Getting a token
```python
# Getting a token

token = fc.get_token()
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

# Get network communication policy
policy = fc.get_network_communication_policy(workspace_id=ws.id)

# Set network communication policy
inbound = {'publicAccessRules': {'defaultAction': 'Allow'}}
outbound = {'publicAccessRules': {'defaultAction': 'Allow'}}

resp = fc.set_network_communication_policy(workspace_id=ws.id, inbound=inbound, outbound=outbound)


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
### Connections

```python

# Add connection role assignment
principal = {"id" : "755f273c-98f8-408c-a886-691794938bd8",
            "type" : "ServicePrincipal"}

add_role_assi = fc.add_connection_role_assignment(connection_id="id", principal=principal, role='User')

# Create Connection 
display_name = "ContosoCloudConnection" + datetime_str

cr = {"connectivityType": "ShareableCloud",
    "displayName": display_name,
    "connectionDetails": {
        'type': "SQL",
        'creationMethod': 'SQL',
        "parameters": [
            {
                "dataType": "Text",
                "name": "server",
                "value": "server_name.database.windows.net"
            },
            {
                "dataType": "Text",
                "name": "database",
                "value": "database_name"
            }
            ]},
    'privacyLevel': 'Organizational',
    'credentialDetails': {'credentials':{'credentialType': 'Basic', 
                                        'userName': 'supercoolusername', 
                                        'password': 'StrongPassword123!'},
                            'singleSignOnType': 'None',
                            'connectionEncryption': 'NotEncrypted',
                            'skipTestConnection': False}
}
    
connection = fc.create_connection(connection_request=cr)

# Delete connection
status_code = fc.delete_connection(connection_id="id")

# Delete connection role assignment
status_code = fc.delete_connection_role_assignment(connection_id="id",
                                                    connection_role_assignment_id="role_assi_id")

# Get Connection
connection2 = fc.get_connection(connection_name="display_name")

# Get connection role assignment
role_assi = fc.get_connection_role_assignment(connection_id="id",
                                              connection_role_assignment_id="role_assi_id")

# List connection role assignments
role_assis = fc.list_connection_role_assignments(connection_id="id")

# List Connections
connections = fc.list_connections()

# List supported connection types
supported_methods = fc.list_supported_connection_types(gateway_id='gw_id', 
                                                       show_all_creation_methods=True)

# Update connection
cr = {
"connectivityType": "ShareableCloud",
"displayName": f"sqlserver{datetime_str}"
}

updated_connection = fc.update_connection(connection_id="id", connection_request=cr)

# Update connection role assignment
role_assi = fc.update_connection_role_assignment(connection_id="id",
                                      connection_role_assignment_id="role_assi_id",
                                      role='UserWithReshare')


```

### Deployment Pipelines

```python
from msfabricpysdkcore import FabricClientCore

fcc = FabricClientCore()
workspace_id = "72dasdfasdf56"

user_id = "e05sadfasfd23"
capacity_id = "9e7easdfasdf2a00"

prod_workspace = fcc.create_workspace("prodworkspace")
prod_workspace.assign_to_capacity(capacity_id)

stages =  [
    {
    "displayName": "Development",
    "description": "Development stage description",
    "isPublic": False
    },
    {
    "displayName": "Production",
    "description": "Production stage description",
    "isPublic":True
    }
]

# Create deployment pipeline
pipe =fcc.create_deployment_pipeline(display_name="sdktestpipeline",
                        description="Test Deployment Pipeline Description",
                        stages=stages)
pipe_id = pipe.id

for stage in pipe.stages:
    if stage["displayName"] == "Development":
        dev_stage = stage
    else:
        prod_stage = stage

# Get deployment pipeline
stage = fcc.get_deployment_pipeline_stage(deployment_pipeline_id=pipe_id,
                                            stage_id=dev_stage["id"])

# Assign workspace to stage
resp = fcc.assign_workspace_to_stage(deployment_pipeline_id=pipe_id,
                        stage_id=dev_stage["id"],
                        workspace_id=workspace_id)


resp = fcc.assign_workspace_to_stage(deployment_pipeline_id=pipe_id,
                        stage_id=prod_stage["id"],
                        workspace_id=prod_workspace.id)

# Add deployment pipeline role assignment
principal = {
    "id": user_id,
    "type": "User"
}

resp = fcc.add_deployment_pipeline_role_assignment(deployment_pipeline_id=pipe_id,principal=principal, role="Admin")

# List deployment pipeline role assignments
roles = fcc.list_deployment_pipeline_role_assignments(deployment_pipeline_id=pipe_id)

# Delete deployment pipeline role assignment
resp = fcc.delete_deployment_pipeline_role_assignment(deployment_pipeline_id=pipe_id, principal_id=user_id)

# List deployment pipelines
pipes = fcc.list_deployment_pipelines(with_details=False)
sdk_pipes = [pipe for pipe in pipes  if "sdk" in pipe["displayName"]]

# Deploy stage content
resp = fcc.deploy_stage_content(deployment_pipeline_id=pipe_id,
                source_stage_id=dev_stage["id"],
                target_stage_id=prod_stage["id"], wait_for_completion=False)

# List deployment pipeline operations
ops = fcc.list_deployment_pipeline_operations(deployment_pipeline_id=pipe_id)

# Get deployment pipeline operation
ops = fcc.get_deployment_pipeline_operation(deployment_pipeline_id=pipe_id, operation_id=ops[0]["id"])

# List deployment pipeline stages
stages = fcc.list_deployment_pipeline_stages(deployment_pipeline_id=pipe_id)

# List deployment pipeline stage items
items = fcc.list_deployment_pipeline_stage_items(deployment_pipeline_id=pipe_id, stage_id=dev_stage["id"])

# Update deployment pipeline
updated_pipe = fcc.update_deployment_pipeline(deployment_pipeline_id=pipe.id, display_name="sdknewname", description="newdescription")

# Get deployment pipeline
pipe = fcc.get_deployment_pipeline(pipe_id)

# Update deployment pipeline stage
updated_stage = fcc.update_deployment_pipeline_stage(deployment_pipeline_id=pipe_id, stage_id=prod_stage["id"],
                                                display_name="newname", description="newdescription")

# Get deployment pipeline stage
stage = fcc.get_deployment_pipeline_stage(deployment_pipeline_id=pipe_id, stage_id=prod_stage["id"])

# Unassign workspace from stage
resp = fcc.unassign_workspace_from_stage(deployment_pipeline_id=pipe_id,stage_id=prod_stage["id"])

# Delete deployment pipeline
resp = fcc.delete_deployment_pipeline(deployment_pipeline_id=pipe_id)
```

### External Data Shares Provider

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

# Delete
response_code = fc.delete_external_data_share(workspace_id, item_id, data_share['id'])
```

### External Data Shares Recipient

```python
from msfabricpysdkcore.coreapi import FabricClientCore
fcc = FabricClientCore()

# Accept external data share invitation
invitation_id = "adfasdfsd"
workspace_id = "asdfsdf"
item_id = "asdfsdf"
provider_tenant_id = "asdfsdf"
payload = {
    "payloadType": "ShortcutCreation",
    "path": "Files/DataFromContoso",
    "createShortcutRequests": [
      {
        "pathId": "5c95314c-ef86-4663-9f1e-dee186f38715",
        "shortcutName": "Shortcut_To_Contoso_Sales_2023"
      },
      {
        "pathId": "6c95314c-ef86-4663-9f1e-dee186f38716",
        "shortcutName": "Shortcut_To_Contoso_Sales_2024"
      }
    ]
  }
obj = fcc.accept_external_data_share_invitation(invitation_id=invitation_id, item_id=item_id,payload=payload, provider_tenant_id=provider_tenant_id,workspace_id=workspace_id):

# Get external data share invitation details
details = fcc.get_external_data_share_invitation(invitation_id=invitation_id, provider_tenant_id=provider_tenant_id)
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

# Get item definition
response = fc.get_item_definition(workspace_id="123123", item_id="123123", type = "Notebook")

# List items
item_list = fc.list_items(workspace_id="workspace_id")
# or
item_list = ws.list_items()

# List item connections
connections = fc.list_item_connections(workspace_id = '6a3',
                                       item_id = '1bcc876')


# Update an item
fc.update_item(workspace_id="workspace_id", item_id="item_id" display_name="new_item_name", description = None, return_item=True)
# or
ws.update_item(item_id="item_id", display_name="new_item_name", description = None, return_item=True)
# or
item.update(display_name="new_item_name", description = None, return_item=True)

# Update item definition
response = fc.update_item_definition(workspace_id="dasf",
                                     item_id="fsdsd", definition=definition)

# Delete an item
fc.delete_item(workspace_id="workspace_id", item_id="item_id")
# or
ws.delete_item(item_id="item_id")
# or
item.delete()

```

### Folders
```python
from msfabricpysdkcore import FabricClientCore
fcc = FabricClientCore()


workspace_id = "asdfasfd"
folder_id = "asdfasdff"

# Create a folder
folder = fcc.create_folder(workspace_id=workspace_id, display_name="sdk_sub_folder", parent_folder_id=folder_id)

# Get a folder
folder_ = fcc.get_folder(workspace_id=workspace_id, folder_id=folder.id)

# List folders
folders = fcc.list_folders(workspace_id=workspace_id)

# Update a folder
folder = fcc.update_folder(workspace_id=workspace_id, folder_id=folder.id, display_name="sdk_sub_folder_updated")

# Move a folder
folder = fcc.move_folder(workspace_id=workspace_id, folder_id=folder.id)

# Delete a folder
fcc.delete_folder(workspace_id=workspace_id, folder_id=folder.id)


```

### Gateways
  
```python

# Add gateway role assignment
principal = {"id" : "75dsbd8",
        "type" : "ServicePrincipal"}
new_ras = fc.add_gateway_role_assignment(gateway_id="gw['id']", principal=principal, role='ConnectionCreator')

# Create a gateway
display_name = 'fabricvnet-123123' + datetime_str
gwr =  {'displayName': display_name,
        'capacityId': '33saf79',
        'virtualNetworkAzureResource': {'virtualNetworkName': 'fabricvnet',
        'subnetName': 'default3',
        'resourceGroupName': 'fabricdemo',
        'subscriptionId': 'cfgf8'},
        'inactivityMinutesBeforeSleep': 30,
        'numberOfMemberGateways': 2,
        'type': 'VirtualNetwork'}

gw = fc.create_gateway(gateway_request=gwr)

# Delete gateway
resp_code = fc.delete_gateway(gateway_id= "gateway_id")

# Delete gatewway member
resp_code = fc.delete_gateway_member(gateway_id= "gateway_id", gateway_member_id= "gateway_member_id")

# Delete gateway role assignment
resp_code = fc.delete_gateway_role_assignment(gateway_id=gw['id'], gateway_role_assignment_id=new_ras['id'])

# Get gateway
gw_ = fc.get_gateway(gateway_id=gw["id"])

# Get gateway role assignment
new_ras_ = fc.get_gateway_role_assignment(gateway_id=gw['id'], gateway_role_assignment_id=new_ras['id'])

# List gateway members
gw_members = fc.list_gateway_members(gateway_id="gw_id")

# List gateway role assignments
ras = fc.list_gateway_role_assignments(gateway_id=gw['id'])

# list gateways
gateways = fc.list_gateways()

# Update gateway
gwr = {
    "type": "OnPremises",
    "displayName": "new_name",
    "loadBalancingSetting": "Failover",
    "allowCloudConnectionRefresh": False,
    "allowCustomConnectors": False
    }

gw_ = fc.update_gateway(gateway_id="gateway_id", gateway_request="gwr")

# Update gateway member
gw_member = fc.update_gateway_member(gateway_id = "gw_id", gateway_member_id = "gateway_member_id", 
                                     display_name="display_name_member", enabled=True)

# Update gateway role assignment
new_ras = fc.update_gateway_role_assignment(gateway_id= gw['id'], gateway_role_assignment_id=new_ras['id'], role='Admin')

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

# Optional:
my_git_credentials = {
    "source": "ConfiguredConnection",
    "connectionId": "3f2asdfasdf82c3301"
}

fc.git_connect(workspace_id="workspaceid", git_provider_details=git_provider_details, my_git_credentials=my_git_credentials)
# or
ws.git_connect(git_provider_details=git_provider_details, my_git_credentials=my_git_credentials)


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

# Get my credentials
git_credentials = fc.get_my_git_credentials(workspace_id="123123")

# Update my credentials
fc.update_my_git_credentials(workspace_id = "1232", source = "Automatic")
fc.update_my_git_credentials(workspace_id = "1232", source = "ConfiguredConnection", connection_id = "3f2504e0aasdfasdf")

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


# Bulk create shortcuts
fc.create_shortcuts_bulk(workspace_id="workspace_id",
                         item_id="item_id",
                         create_shortcut_requests=[
                             {
                                 "path": "Files",
                                 "name": "sales_2023",
                                 "target": {
                                     "oneLake": {
                                         "workspaceId": "workspace_id_target",
                                         "itemId": "item_id_target",
                                         "path": "Tables/Sales2023"
                                     }
                                 }
                             },
                              {
                                "path": "Files/landingZone",
                                "name": "PartnerProducts",
                                "target": {
                                    "adlsGen2": {
                                        "location": "https://casdfasdfat.dfs.core.windows.net",
                                        "subpath": "/mycontainer/data/ContosoProducts",
                                        "connectionId": "91asdfasdfa1e"
                                    }
                                }
                              }
                         ])

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

# List shortcuts of an item

fc.list_shortcuts(workspace_id="workspace_id",
                  item_id="item_id",
                  # optional parent_path="Tables"
                  )

# or
ws.list_shortcuts(item_id="item_id",
                  # optional parent_path="Tables"
                  )

# or
item.list_shortcuts(parent_path="Tables")

# Reset shortcut cache
fc.reset_shortcut_cache(workspace_id="23232", wait_for_completion = False)

```

### Tags

```python
from msfabricpysdkcore import FabricClientCore
fcc = FabricClientCore()

# List tags
tags = fcc.list_tags()

tag_ids = [tag["id"] for tag in tags]

# Apply tags
resp = fcc.apply_tags(workspace_id = "adsfsdf", item_id = "a9e59ec1-524b-49b1-a185-37e47dc0ceb9", tags = tag_ids)

# Unapply tags
resp = fcc.unapply_tags(workspace_id = "adsfsdf", item_id = "a9e59ec1-524b-49b1-a185-37e47dc0ceb9", tags = tag_ids)

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
jobType="Pipeline"


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

# List item job instances
job_instances = fc.list_item_job_instances(workspace_id="workspace_id",
                                           item_id="item_id")

# Create item schedule
configuration = {'type': 'Daily',
                  'startDateTime': '2024-11-21T00:00:00',
                  'endDateTime': '2028-11-08T23:59:00',
                  'localTimeZoneId': 'Romance Standard Time',
                  'times': ['15:39']}

schedule = fc.create_item_schedule(workspace_id="1232", item_id="1232", job_type="sparkjob", configuration=configuration, enabled=True)

# Delete item schedule
fc.delete_item_schedule(workspace_id="1232", item_id="1232", schedule_id="schedule_id", job_type="sparkjob")

# Get item schedule
schedule_check = fc.get_item_schedule(workspace_id="1232", item_id="1232", 
                                      schedule_id="schedule_id", job_type="sparkjob")

# Update item schedule
schedule_new = fc.update_item_schedule(workspace_id="1232", item_id="1232",
                                       schedule_id="schedule_id", job_type="sparkjob", configuration=configuration, enabled=False)

# List item schedules
list_schedules = fc.list_item_schedules(workspace_id="1232", item_id="1232", job_type="sparkjob")


```


### Long Running Operations

```python

# Get the state of an operation

operation_id = "801783df0123gsdgsq80"

state = fc.get_operation_state(operation_id)

# Get the results of an operation

results = fc.get_operation_results(operation_id)

```

### Managed Private Endpoints

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

# Create a workspace managed private endpoint
mpe = fc.create_workspace_managed_private_endpoint(workspace_id='535fb',
                                                   name = 'testmpe',
                                                   target_private_link_resource_id = '/subscriptions/c78/resourceGroups/fabricdemo/providers/Microsoft.Storage/storageAccounts/pu39',
                                                   target_subresource_type = 'dfs',
                                                   request_message = 'testmessage')

# Delete workspace managed private endpoint
status_code = fc.delete_workspace_managed_private_endpoint(workspace_id='53b',
                                                           managed_private_endpoint_id="mpeid")

# Get workspace managed private endpoint
mpe2 = fc.get_workspace_managed_private_endpoint(workspace_id='5355fb', 
                                                 managed_private_endpoint_id="mpeid")

# List workspace managed private endpoints
mpes = fc.list_workspace_managed_private_endpoints(workspace_id='53b')
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

# Get workspace
ws = fca.get_workspace(workspace_id="workspace_id")

# List git connectsions
git_connections = fca.discover_git_connections()

# List workspace access details
ws_access = fca.list_workspace_access_details("workspace_id")

# List workspaces
ws = fca.list_workspaces(name="testworkspace")[0]

# Restore workspace
fca.restore_workspace(workspace_id = "213123",
                      new_workspace_admin_principal={"id": "081adiaj3", "type":"User"},
                      new_workspace_name = "Contoso Workspace")
```

### Admin API for Users

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# Get access entities

user_id = 'b4fuhaidc2'
access_entities = fca.list_access_entities(user_id, type="Notebook")

```

### Admin API for Sharing Links

```python
from msfabricpysdkcore import FabricClientAdmin
fca = FabricClientAdmin()

items = [
    {
      "id": "fe472f5e-636e-4c10-a1c6-7e9edc0b542a",
      "type": "Report"
    },
    {
      "id": "476fcafe-b514-495d-b13f-ca9a4f0b1d8b",
      "type": "Report"
    }]

# Bulk remove sharing links
fca.bulk_remove_sharing_links(items = items, sharing_link_type = "OrgLink")

# Remove all sharing links
fca.remove_all_sharing_links(sharing_link_type = "OrgLink")
```

### Admin API for Tags

```python

from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# Bulk create tags
new_tags = [{"displayName": "sdk_tag_temp"}]
resp = fca.bulk_create_tags(create_tags_request=new_tags)

# Delete tag
fca.delete_tag(tag_id="adsfasdf")

# List tags
tag_list = fca.list_tags()

# Update Tag
updated_tag = fca.update_tag(tag_id="adsfasdf", display_name="sdk_tag_updated")


```


### Admin API for Tenants

```python
from msfabricpysdkcore import FabricClientAdmin

fca = FabricClientAdmin()

# List tenant settings
tenant_settings = fca.list_tenant_settings()

# Get capacity tenant settings overrides
overrides = fca.list_capacities_tenant_settings_overrides()

# Get domain tenant settings overrides
overrides = fca.list_domain_tenant_settings_overrides()

# Get workspace tenant settings overrides
overrides = fca.list_workspace_tenant_settings_overrides()

# Get capacity tenant settings overrides by capacity id
overrides = fca.list_capacity_tenant_settings_overrides_by_capacity_id(capacity_id="adsfasdfasf")

# Update tenant setting
fc.update_tenant_setting(tenant_setting_name = "PlatformMonitoringTenantSetting", enabled = True, delegate_to_capacity = None, delegate_to_domain = None,
                              delegate_to_workspace = None, enabled_security_groups = None, excluded_security_groups = None, properties = None)

# Update capacity tenant setting override
fc.update_capacity_tenant_setting_override(capacity_id = "capacity_id", tenant_setting_name = "PlatformMonitoringTenantSetting", enabled = True, delegate_to_workspace = None, 
                                                enabled_security_groups = None, excluded_security_groups = None)


# Delete capacity tenant setting override
fc.delete_capacity_tenant_setting_override(capacity_id = "capacity_id", tenant_setting_name = "PlatformMonitoringTenantSetting")

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

# List role assignments
resp = fca.list_role_assignments(domain_id=domain.id)

# Sync role assignments to subdomains
resp = fca.sync_role_assignments_to_subdomains(domain_id=domain.id, role="Contributor")



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


### Azure Resource Management APIs for Fabric capacities

```python
from msfabricpysdkcore import FabricAzureClient

fac = FabricAzureClient()

subscription_id = "fsdgdfgds"
resource_group_name = "fabricdemo"
capacity_name = "rgsdfgsdfgsd"
capacity_name_new = "dsfgsdfgsdfg" + datetime.now().strftime("%Y%m%d%H%M%S")

# Check name availability

resp = fac.check_name_availability(subscription_id, "westeurope", capacity_name_new)

# Create or update capacity
resp = fac.create_or_update_capacity(subscription_id, resource_group_name, capacity_name_new, 
                                    location="westeurope",
                                    properties_administration={"members": ['hfds@afasf.com']},
                                    sku = "F2")

# Get capacity
resp = fac.get_capacity(subscription_id, resource_group_name, capacity_name_new)
sku = resp.sku['name']

# Delete capacity
resp = fac.delete_capacity(subscription_id, resource_group_name, capacity_name_new)

# List capacities by resource group
resp = fac.list_by_resource_group(subscription_id, resource_group_name)
cap_names = [cap["name"] for cap in resp]

# List capacities by subscription
resp = fac.list_by_subscription(subscription_id)
cap_names = [cap["name"] for cap in resp]

# List SKUs
resp = fac.list_skus(subscription_id)

# List SKUs for capacity
resp = fac.list_skus_for_capacity(subscription_id, resource_group_name, capacity_name)

# Resume capacity
resp = fac.resume_capacity(subscription_id, resource_group_name, capacity_name)

# Suspend capacity
resp = fac.suspend_capacity(subscription_id, resource_group_name, capacity_name)

# Update capacity
resp = fac.update_capacity(subscription_id, resource_group_name, capacity_name, sku="F4")
```

### Logging

The SDK uses the Python logging module, following the logging settings of your application. You can set up logging in 
your project like this:

```python
import logging
from msfabricpysdkcore import FabricClientCore

logging.basicConfig(level=logging.DEBUG)
fc = FabricClientCore() # The client will now log
```

You can also set the environment variable `FABRIC_SDK_DEBUG` to `1` to enable debug logging.

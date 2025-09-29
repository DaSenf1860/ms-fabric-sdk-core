# Release Notes

## 0.2.9
### New Features
- Bulk creation of shortcuts in an item
- Git connect with my git credentials

## 0.2.8
### New Features
- Workspace APIs:
  - Get workspace by id with return_item parameter
  - workspace item gives all the new properties like capacity_region, one_lake_endpoints, capacity_assignment_progress, workspace_identity

## 0.2.7
### New Features
- external data shares providers delete
- dataflow - Background jobs
- Warehouse Snapshot
- Apache Airflow Job
- digital twin builder
- digital twin builder flow
- mirrored azure databricks 
- sql endpoint refresh metadata

## 0.2.6

### Bug Fixes
- Reworked the new addition of lakehouses with schemas to work correctly with the API.

## 0.2.5

### New Features
- Allow to create lakehouses with creation payload which allows lakehouses with schemas

## 0.2.4

### New Features
- Admin APIs: 
  - Tags APIs
  - Sharing Links (Removal) APIs
- Core APIs:
  - Tags APIs
  - Folders APIs
  - Copy Jobs APIs
  - Dataflows APIs
  - Data Pipeline Definition APIs
  - Deployment Pipelines (new version) APIs
  - Variable Library APIs
  - Eventstream Topology APIs
  - External Data Shares Recipient APIs
  - Lakehouse Livy Sessions APIs
  - Notebooks Livy Sessions APIs
  - Spark Livy Sessions APIs
  - SJD Livy Sessions APIs

## 0.2.3

### Hotfixes
- there was a change in the git API for initializing the connection. This is now adjusted
- there was a change in the API for getting a domain object. This is now adjusted

## 0.2.2

### New Features
- One Lake Shortcuts: Reset Shortcut Cache
- Admin Tenant APIs
- Eventhouse: Get and update definition
- Eventstream: Get and update definition
- KQL database: Get and update definition
- Reflex: CRUDL
- Sqldatabase: CRUDL
- GraphQLAPI: 
- MountedDatafactory: CRUDL
- Report: Update Report


## 0.2.1

### New Features
- admin APIs: discover/list git connections for all workspaces
- core-git APIs: get/update my credentials
- core-item APIs: list item connections
- kql dashboard CRUD APIs
- paginated reports: update
- semantic model: update
- managed private endpoints: create/delete/get/list
- job scheduler: item schedules, list instances
- gateway APIs: create/update/delete/get/list + members + role assignemtns 
- connection API: create/update/delete/get/list + role assignemtns
- kqlquerysets API: create/update/delete/get/list 
- mirrored database API: create/update/delete/get/list + start/stop/status mirroring 

### Changed Behaviour
- Update of items or definitions don´t return the updated items by default. You can get the updated items by setting the parameter `return_item=True` in the update function.

## 0.1.8

### Bug Fixes
- added listing of one lake shortcuts

## 0.1.7

### Bug Fixes
- fixed a bug that the authentication in a Fabric notebook didn´t work correctly

## 0.1.6

### Bug Fixes
- fixed a bug that the list_items functions with the parameter "with_properties = True" didn´t work correctly

## 0.1.5

- added MSALConfidentialClientApplicationAuthentication

## 0.1.4

### Bug Fixes
- now you can use a Service Principal to work against the Azure Resoure Management APIs

## 0.1.3

- adding logging logics

## 0.1.2

### New Features
- added Azure Resource Manager APIs for Fabric capacities

## 0.1.1

### Refactoring
Massive refactoring to simplify the code and make it more maintainable. The main changes are:
- All APIs are called from the client classes. 
- The API calls are handled by a single function
This leads to an improvement of performance of the application by reducing the number of API calls.
Each function normally is doing a single API call.


## 0.0.14

### New Features
- added APIs for environment spark libraries

## 0.0.13

### New Features 
- added external data share APIs for core and admin APIs
- added one lake data access security APIs

## 0.0.12

### New Features 
- accomodated the latest core Workspaces APIs changes regarding role assignments
- added provisioning and deprovisioning of workspace identities
- added API for run on demand spark job definition

## 0.0.11

### New Features

- added Eventhouse APIs (create, update, delete, get, list)
- added Environment APIs (create, update, delete, get, list)
- added Environment details APIs except upload_staging_library (implemented are get published settings, get staging settings, update staging settings) 
- added KQL Database Create API

## 0.0.10

### New Features

- added deployment pipeline APIs
- added APIs for spark custom pools and workspace settings
- added Create Data Pipeline API
- added Long Running Operations API
- added Lakehouse background jobs API for manual table maintenance
- added the Label APIs as part of the Admin APIs
- added get and update definition APIs for semantic models, notebooks, reports and spark job definitions

### Revisions

- some Admin APIs have changed and are called list_..._settings instead of get_..._settings. The naming in the SDK is changed accordingly although we tried to keep the old naming still vialbe for backwards compatibility with a deprecation warning. The old naming will be removed in one of the next releases.

## 0.0.9

### New Features

- adding a Synapse Spark authentication client, so that it is possible to use via a Fabric Notebook

## 0.0.7

### New Features

- changing pypi package to allow for python >=3.10 instead of >=3.11 so that you can use it from fabric directly

## 0.0.6

### New Features

- adding item specific CRUD APIs

## 0.0.5

### New Features

- getting or creating an item will retrieve automatically additional properties and item definitions. Note that when retrieving a list this is disabled by default, but can be enabled by setting `with_properties=True` (It is disabled because it takes significantly more time to retrieve all properties for all items)

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()
ws = fc.get_workspace_by_name("testworkspace")
items_with_details = ws.list_items(with_properties=True)
```

## 0.0.4

### New Features

- introduced general client
- added admin api client
- moved old client to core client
- added domains and all other admin apis
- more advanced usage patterns


## 0.0.3

### New Features

- added pagination
- added getting item by name and type
- added Lakehouse APIs for listing tables and loading tables
- added capacity reference by name
- added usage patterns for bulk operations

### Bug Fixes

- added a workaround for the create item API bug which does not return the item for all types

# Release Notes

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

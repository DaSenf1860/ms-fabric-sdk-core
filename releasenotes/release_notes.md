# Release Notes

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

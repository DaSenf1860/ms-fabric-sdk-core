# Advanced Usage Patterns

Here are some examples to make use of the SDK for specific tasks:

- [Bulk capacity assignment](#bulk-capacity-assignment)
- [Bulk workspace deletion](#bulk-workspace-deletion)
- [Bulk workspace creation and capacity assignment](#bulk-workspace-creation-and-capacity-assignment)
- [Bulk delete all items in a workspace](#bulk-delete-all-items-in-a-workspace)
- [Return all workspaces assigned to a specific capacity](#return-all-workspaces-assigned-to-a-specific-capacity)
- [Do a "landing zone"- deployment](#do-a-landing-zone--deployment)
- [Bulk set labels for all items in a workspace](#bulk-set-labels-for-all-items-in-a-workspace)
- [Bulk suspend capacities](#bulk-suspend-capacities)
- [Use username and password authentication via az-cli](#use-username-and-password-authentication)



## Bulk capacity assignment

You can move workspaces in a bulk to different capacities, e.g. moving from a Power BI Premium Capacity to a Fabric Capacity.

```python
#### Move selected workspaces to another capacity
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

list_workspaces = ["sales_forecast_dev", "sales_forecast_qa", "sales_sandbox", "finance_sandbox"]
cap = fc.get_capacity(capacity_name="democapacity")
capacity_id = cap.id

for ws in list_workspaces:
    ws_ = fc.get_workspace_by_name(ws)
    ws_.assign_capacity(capacity_id)

##### Move all workspaces from one capacity to another
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()
cap_source = fc.get_capacity(capacity_id="ioasdjfoas12i312")
cap_target = fc.get_capacity(capacity_name="nameoftargetcapacity")

ws_in_cap = [ws for ws in fc.list_workspaces() if ws.capacity_id == cap_source.id]
for ws in ws_in_cap:
    ws.assign_to_capacity(cap_target.id)
    print(f"Assigned {ws.display_name} to {cap_target.display_name}")

```

## Bulk workspace deletion

Delete a list of workspaces in a bulk.

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

list_workspaces = ["sales_forecast_dev", "sales_forecast_qa", "sales_sandbox", "finance_sandbox"]


for ws in list_workspaces:
    ws_ = fc.get_workspace_by_name(ws)
    ws_.delete()

```

## Bulk workspace creation and capacity assignment

Create a list of workspaces and assign them to a capacity.

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

list_workspaces = ["sales_forecast_dev", "sales_forecast_qa", "sales_sandbox", "finance_sandbox"]
cap_target = fc.get_capacity(capacity_name="nameoftargetcapacity")

for ws in list_workspaces:
    ws_ = fc.create_wor(ws)
    ws_.assign_to_capacity(cap_target.id)

```

## Bulk delete all items in a workspace

Delete all items in a workspace.

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

ws = fc.get_workspace_by_name("sales_forecast_dev")
for item in ws.get_items():
    item.delete()

```

## Return all workspaces assigned to a specific capacity

Get all workspaces assigned to a specific capacity.

```python
from msfabricpysdkcore import FabricClientCore

fcc = FabricClientCore()

cap = fcc.get_capacity(capacity_name="demofabric1203d")
all_ws = fcc.list_workspaces()
cap_ws = [ws for ws in all_ws if ws.capacity_id == cap.id]
print(cap_ws)
    
```

## Do a "landing zone"- deployment
```python
## Creating a new capacity, create a new domain, create new workspaces, assign the new capacity to these workspaces, assign the workspaces to the domain, assign users to the workspaces, create a skeleton of workspace items in those workspaces

from msfabricpysdkcore import FabricAzureClient, FabricClientCore, FabricClientAdmin
from datetime import datetime

fac = FabricAzureClient()
fcc = FabricClientCore()
fca = FabricClientAdmin()


subscription_id = "casdfaa8"
resource_group_name = "fabricdemo"
capacity_name = "asdfasdf"
capacity_name_new = "asdfasfd" + datetime.now().strftime("%Y%m%d%H%M%S")


resp = fac.create_or_update_capacity(subscription_id, resource_group_name, capacity_name_new, 
                                    location="westeurope",
                                    properties_administration={"members": ['asdfads@dasfasdf.com']},
                                    sku = "F2")

capacity = fcc.get_capacity(capacity_name = capacity_name_new)

ws_created = fcc.create_workspace(display_name="workspace" + datetime.now().strftime("%Y%m%d%H%M%S"),
                                  description="test workspace")
result_status_code = fcc.assign_to_capacity(workspace_id=ws_created.id, 
                                            capacity_id=capacity.id)


domain = fca.create_domain(display_name="domain" + datetime.now().strftime("%Y%m%d%H%M%S"))

status_code = fca.assign_domain_workspaces_by_ids(domain.id, [ws_created.id])
#....
```

## Bulk set labels for all items in a workspace

```python
from msfabricpysdkcore import FabricClientCore, FabricClientAdmin

fcc = FabricClientCore()
fca = FabricClientAdmin()

ws = fcc.get_workspace_by_name("testitems")
items = fcc.list_items(ws.id)
items_ = [{"id": item.id, "type": item.type} for item in items]
label_id = "de8271asdf4345d2" # to be found in Microsoft Purview Compliance Center

# Bulk set labels 
resp = fca.bulk_set_labels(items=items_, label_id=label_id)
```

## Bulk suspend capacities

```python
from msfabricpysdkcore import FabricAzureClient

fac = FabricAzureClient()
subscription_id = "ca------------asd"

caps = fac.list_by_subscription(subscription_id)
for cap in caps:
    if cap["properties"]["state"] == "Paused":
        continue
    try:
        resource_id = cap["id"].split("/")
        resource_group_name = resource_id[4]
        subscription_id = resource_id[2]
        fac.suspend_capacity(subscription_id, resource_group_name, cap["name"])
    except Exception as e:
        print(e)
```

## Use username and password authentication
.env File
```
FABRIC_USERNAME=yourmail@yourcompany.com
FABRIC_PASSWORD=...
```

Additional requirement: azure-cli
```
pip install azure-cli
```

Use Azure CLI login in Python:
```python
import os
from msfabricpysdkcore import FabricClientCore

def prepare_authentication():
    # get username and password from environment variables
    username = os.environ.get('FABRIC_USERNAME')
    password = os.environ.get('FABRIC_PASSWORD')

    cmd = f"az login --allow-no-subscriptions --username {username} --password {password}"
    # execute python in command line
    os.system(cmd)


prepare_authentication()

fc = FabricClientCore()
```

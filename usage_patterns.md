# Advanced Usage Patterns

Here are some examples to make use of the SDK for specific tasks:

- [Bulk capacity assignment](#bulk-capacity-assignment)
- [Bulk workspace deletion](#bulk-workspace-deletion)
- [Bulk workspace creation and capacity assignment](#bulk-workspace-creation-and-capacity-assignment)
- [Bulk delete all items in a workspace](#bulk-delete-all-items-in-a-workspace)
- [Return all workspaces assigned to a specific capacity](#return-all-workspaces-assigned-to-a-specific-capacity)



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


for ws in list_workspaces:
    ws_ = fc.create_wor(ws)
    ws_.delete()

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
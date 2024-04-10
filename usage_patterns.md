# Advanced Usage Patterns

Here are some examples to make use of the SDK for specific tasks:


## Bulk capacity assignment

You can move workspaces in a bulk to different capacities, e.g. moving from a Power BI Premium Capacity to a Fabric Capacity.

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

list_workspaces = ["sales_forecast_dev", "sales_forecast_qa", "sales_sandbox", "finance_sandbox"]
cap = fc.get_capacity(capacity_name="democapacity")
capacity_id = cap.id

for ws in list_workspaces:
    ws_ = fc.get_workspace_by_name(ws)
    ws_.assign_capacity(capacity_id)

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

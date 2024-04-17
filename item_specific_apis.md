# Item specific APIs

Each item type has its own set of APIs. The following are the APIs for each item type.
All APIs are also available on workspace level as well.

## Dashboards, DataMarts, SQL Endpoints, Mirrored Warehouses, Paginated Reports

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List dashboards
list_dashboards = fc.list_dashboards(workspace_id)

# List datamarts
list_datamarts = fc.list_datamarts(workspace_id)

# List sql endpoints
list_sql_endpoints = fc.list_sql_endpoints(workspace_id)

# List mirrored warehouses
list_mirrored_warehouses = fc.list_mirrored_warehouses(workspace_id)

# List paginated reports
list_paginated_reports = fc.list_paginated_reports(workspace_id)

```

## Lakehouse

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()
workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# Get Lakehouse
lakehouse = fc.get_lakehouse(workspace_id=workspace_id, item_name="lakehouse1")
item_id = lakehouse.id
date_str = datetime.now().strftime("%Y%m%d%H%M%S")
table_name = f"table{date_str}"

# Load Table
status_code = fc.load_table(workspace_id=workspace_id, item_id=item_id, table_name=table_name, 
                            path_type="File", relative_path="Files/folder1/titanic.csv")

# List Tables
table_list = fc.list_tables(workspace_id=workspace_id, item_id=item_id)

# Create Lakehouse
lakehouse = fc.create_lakehouse(workspace_id=workspace_id, display_name="lakehouse2")
        
# List Lakehouses
lakehouses = fc.list_lakehouses(workspace_id)

# Get Lakehouse
lakehouse2 = fc.get_lakehouse(workspace_id=workspace_id, lakehouse_id=lakehouse.id)
        
# Update Lakehouse
lakehouse2 = fc.update_lakehouse(workspace_id=workspace_id, lakehouse_id=lakehouse.id, display_name="lakehouse3")

# Delete Lakehouse
fc.delete_lakehouse(workspace_id=workspace_id, lakehouse_id=lakehouse.id)

```

## Data Pipelines

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Data Pipelines

dps = fc.list_data_pipelines(workspace_id)

# Get Data Pipeline
dp = fc.get_data_pipeline(workspace_id, data_pipeline_name="pipeline1")

# Update Data Pipeline
dp2 = fc.update_data_pipeline(workspace_id, dp.id, display_name="pipeline2")

# Delete Data Pipeline
fc.delete_data_pipeline(workspace_id, dp.id)

```

## Eventstreams

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Eventstreams
eventstreams = fc.list_eventstreams(workspace_id)

# Create Eventstream
es = fc.create_eventstream(workspace_id, display_name="es1")

# Get Eventstream
es = fc.get_eventstream(workspace_id, eventstream_name="es1")

# Update Eventstream
es2 = fc.update_eventstream(workspace_id, es.id, display_name="es2")

# Delete Eventstream
fc.delete_eventstream(workspace_id, es.id)

```

## KQL Databases

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List KQL Databases
kql_databases = fc.list_kql_databases(workspace_id)

# Get KQL Database
kqldb = fc.get_kql_database(workspace_id, kql_database_name="kqldatabase1")

# Update KQL Database
kqldb2 = fc.update_kql_database(workspace_id, kqldb.id, display_name="kqldb2")

# Delete KQL Database
fc.delete_kql_database(workspace_id, kqldb.id)

```

## KQL Querysets

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List KQL Querysets
kql_querysets = fc.list_kql_querysets(workspace_id)

# Get KQL Queryset
kqlq = fc.get_kql_queryset(workspace_id, kql_queryset_name="kqlqueryset1")

# Update KQL Queryset
kqlq2 = fc.update_kql_queryset(workspace_id, kqlq.id, display_name="kqlqueryset2")

# Delete KQL Queryset
fc.delete_kql_queryset(workspace_id, kqlq.id)

```

## ML Experiments

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List ML Experiments
ml_experiments = fc.list_ml_experiments(workspace_id)

# Create ML Experiment
mle = fc.create_ml_experiment(workspace_id, display_name="mlexperiment1")

# Get ML Experiment
mle = fc.get_ml_experiment(workspace_id, ml_experiment_name="mlexperiment1")

# Update ML Experiment
mle2 = fc.update_ml_experiment(workspace_id, mle.id, display_name="mlexperiment2")

# Delete ML Experiment
fc.delete_ml_experiment(workspace_id, mle.id)

```

## ML Models

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List ML Models
ml_models = fc.list_ml_models(workspace_id)

# Create ML Model
ml_model = fc.create_ml_model(workspace_id, display_name="mlmodel1")

# Get ML Model
ml_model = fc.get_ml_model(workspace_id, ml_model_name="mlmodel1")

# Update ML Model
ml_model2 = fc.update_ml_model(workspace_id, ml_model_id=ml_model.id, display_name="mlmodel2")

# Delete ML Model
fc.delete_ml_model(workspace_id, ml_model.id)

```

## Notebooks

```python

 from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Notebooks
notebooks = fc.list_notebooks(workspace_id)

# Create Notebook
notebook_w_content = fc.get_notebook(workspace_id, notebook_name="HelloWorld")
definition = notebook_w_content.definition
notebook = fc.create_notebook(workspace_id, definition = definition, display_name="notebook1")

# Get Notebook
notebook = fc.get_notebook(workspace_id, notebook_name="notebook1")

# Update Notebook
notebook2 = fc.update_notebook(workspace_id, notebook.id, display_name="notebook2")

# Update Notebook Definition
fc.update_notebook_definition(workspace_id, notebook.id, definition=definition)

# Delete Notebook
fc.delete_notebook(workspace_id, notebook.id)

```

## Reports

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Reports
reports = fc.list_reports(workspace_id)

# Create Report
report_w_content = fc.get_report(workspace_id, report_name="HelloWorldReport")
definition = report_w_content.definition
report = fc.create_report(workspace_id, display_name="report1", definition=definition)

# Get Report
report = fc.get_report(workspace_id, report_name="report1")

# Update Report Definition
fc.update_report_definition(workspace_id, report.id, definition=definition)

# Delete Report
fc.delete_report(workspace_id, report.id)

```

## Semantic Models

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Semantic Models
semantic_models = fc.list_semantic_models(workspace_id)

# Create Semantic Model
semantic_model_w_content = fc.get_semantic_model(workspace_id, semantic_model_name="Table")
definition = semantic_model_w_content.definition
semantic_model = fc.create_semantic_model(workspace_id, display_name="semanticmodel1", definition=definition)

# Get Semantic Model
semantic_model = fc.get_semantic_model(workspace_id, semantic_model_name="semanticmodel1")

# Update Semantic Model Definition
fc.update_semantic_model_definition(workspace_id, semantic_model.id, definition=definition)

# Delete Semantic Model
fc.delete_semantic_model(workspace_id, semantic_model.id)

```

## Spark Job Definitions


```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Spark Job Definitions
spark_job_definitions = fc.list_spark_job_definitions(workspace_id)

# Create Spark Job Definition
spark_job_definition_w_content = fc.get_spark_job_definition(workspace_id, spark_job_definition_name="helloworld")
definition = spark_job_definition_w_content.definition
spark_job_definition = fc.create_spark_job_definition(workspace_id, display_name=spark_job_definition_name, definition=definition)
# Get Spark Job Definition
spark_job_definition = fc.get_spark_job_definition(workspace_id, spark_job_definition_name="helloworld")

# Update Spark Job Definition
spark_job_definition2 = fc.update_spark_job_definition(workspace_id, spark_job_definition.id, display_name="sparkjobdefinition2")

# Update Spark Job Definition Definition
fc.update_spark_job_definition_definition(workspace_id, spark_job_definition.id, definition=definition)

# Delete Spark Job Definition
fc.delete_spark_job_definition(workspace_id, spark_job_definition.id)

```

## Warehouses

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Warehouses
warehouses = fc.list_warehouses(workspace_id)

# Create Warehouse
warehouse = fc.create_warehouse(workspace_id, display_name="wh1")

# Get Warehouse
warehouse = fc.get_warehouse(workspace_id, warehouse_name="wh1")

# Update Warehouse
warehouse2 = fc.update_warehouse(workspace_id, warehouse.id, display_name="wh2")

# Delete Warehouse
fc.delete_warehouse(workspace_id, warehouse.id)

```
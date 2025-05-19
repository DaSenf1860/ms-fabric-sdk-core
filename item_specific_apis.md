# Item specific APIs

Each item type has its own set of APIs. The following are the APIs for each item type.
All APIs are also available on workspace level as well.

Go to:
- [Dashboards, DataMarts, SQL Endpoints, Mirrored Warehouses, Paginated Reports](#dashboards-datamarts-sql-endpoints-mirrored-warehouses-paginated-reports)
- [Copy Jobs](#copy-jobs)
- [Dataflows](#dataflows)
- [Data Pipelines](#data-pipelines)
- [Environments](#environments)
- [Eventhouses](#eventhouses)
- [Eventstreams](#eventstreams)
- [Eventstream Topology](#eventstream-topology)
- [GraphQL APIs](#graphql-apis)
- [KQL Dashboards](#kql-dashboards)
- [KQL Databases](#kql-databases)
- [KQL Querysets](#kql-querysets)
- [Lakehouse](#lakehouse)
- [Mirrored Database](#mirrored-database)
- [ML Experiments](#ml-experiments)
- [ML Models](#ml-models)
- [Notebooks](#notebooks)
- [Reports](#reports)
- [Semantic Models](#semantic-models)
- [Spark Livy Sessions](#spark-livy-sessions)
- [Spark Custom Pools](#spark-custom-pools)
- [Spark Job Definitions](#spark-job-definitions)
- [SQL Databases](#sql-databases)
- [Variable Libraries](#variable-libraries)
- [Warehouses](#warehouses)


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

# Update paginated report
fc.update_paginated_report(workspace_id="1232", paginated_report_id="12312",
                           display_name = "newname", description = "newdescription", return_item=False)

```

## Copy Jobs

```python
from msfabricpysdkcore import FabricClientCore
fcc = FabricClientCore()
workspace_id = "asdfasdf"
item_id = "asdfasdf9"

# Get copy job definition
copy_job_definition = fcc.get_copy_job_definition(workspace_id=workspace_id, copy_job_id=item_id)

# Create copy job
copy_job_new = fcc.create_copy_job(workspace_id=workspace_id, display_name="name", definition=definition)

# Get copy job
copy_job_get = fcc.get_copy_job(workspace_id=workspace_id, copy_job_id=copy_job_new.id)

# List copy jobs
copy_jobs = fcc.list_copy_jobs(workspace_id=workspace_id)

# Update copy job
copy_job_updated = fcc.update_copy_job(workspace_id=workspace_id, copy_job_id=copy_job_new.id, display_name="date_str_updated", return_item=True)

# Update copy job definition
copy_job_updated = fcc.update_copy_job_definition(workspace_id=workspace_id, copy_job_id=copy_job_new.id, definition=definition)

# Delete copy job
resp = fcc.delete_copy_job(workspace_id=workspace_id, copy_job_id=copy_job.id)


```

### Dataflows

```python
from msfabricpysdkcore import FabricClientCore
from datetime import datetime

fcc = FabricClientCore()

workspace_id = "0asdfasdfd3"
item_id = "8bsadf4088"

# List dataflows
dataflows = fcc.list_dataflows(workspace_id=workspace_id)

# Get dataflow definition
dataflow_definition = fcc.get_dataflow_definition(workspace_id=workspace_id, dataflow_id=item_id)
definition = dataflow_definition["definition"]

date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_str = date_str.replace(" ", "T").replace(":", "").replace("-", "")
date_str = f"dataflow{date_str}"

# Create dataflow
dataflow_new = fcc.create_dataflow(workspace_id=workspace_id, display_name=date_str, definition=definition)

# Get dataflow
dataflow_get = fcc.get_dataflow(workspace_id=workspace_id, dataflow_id=dataflow_new.id)

# Update dataflow
date_str_updated = date_str + "_updated"
dataflow_updated = fcc.update_dataflow(workspace_id=workspace_id, dataflow_id=dataflow_new.id, display_name=date_str_updated, return_item=True)

# Update dataflow definition
dataflow_updated = fcc.update_dataflow_definition(workspace_id=workspace_id, dataflow_id=dataflow_new.id, definition=definition)

# Delete dataflow
resp = fcc.delete_dataflow(workspace_id=workspace_id, dataflow_id=dataflow_new.id)


```

## Data Pipelines

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace_id = "asdfasdf"
item_id = "b7dasfasf26b5d3"

# List data pipelines
data_pipelines = fcc.list_data_pipelines(workspace_id=workspace_id)

# Get data pipeline definition
data_pipeline_definition = fcc.get_data_pipeline_definition(workspace_id=workspace_id, data_pipeline_id=item_id)
definition = data_pipeline_definition["definition"]

date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_str = date_str.replace(" ", "T").replace(":", "").replace("-", "")
date_str = f"data_pipeline{date_str}"

# Create data pipeline
data_pipeline_new = fcc.create_data_pipeline(workspace_id=workspace_id, display_name=date_str, definition=definition)

# Get data pipeline
data_pipeline_get = fcc.get_data_pipeline(workspace_id=workspace_id, data_pipeline_id=data_pipeline_new.id)

# Update data pipeline
date_str_updated = date_str + "_updated"
data_pipeline_updated = fcc.update_data_pipeline(workspace_id=workspace_id, data_pipeline_id=data_pipeline_new.id, display_name=date_str_updated, return_item=True)

# Update data pipeline definition
data_pipeline_updated = fcc.update_data_pipeline_definition(workspace_id=workspace_id, data_pipeline_id=data_pipeline_new.id, definition=definition)

# Delete data pipeline
resp = fcc.delete_data_pipeline(workspace_id=workspace_id, data_pipeline_id=data_pipeline_updated.id)


```

## Environments

```python
from msfabricpysdkcore import FabricClientCore
fc = FabricClientCore()
workspace_id = 'd8asd'

# Create environment
environment1 = fc.create_environment(workspace_id, display_name="environment1")

# List environments
environments = fc.list_environments(workspace_id)
environment_names = [env.display_name for env in environments]

# Get environment
env = fc.get_environment(workspace_id, environment_name="environment1")

# Update environment
env2 = fc.update_environment(workspace_id, env.id, display_name="environment2", return_item=True)

# Delete environment
status_code = fc.delete_environment(workspace_id, env.id)


# Get published settings
workspace_id = 'asdf5'
environment_id = 'asdf6f'
published_settings = fc.get_published_settings(workspace_id=workspace_id, environment_id=environment_id)

# Get staging settings
staging_settings = fc.get_staging_settings(workspace_id=workspace_id, environment_id=environment_id)

# Update staging settings
driver_cores = 4
updated_settings = fc.update_staging_settings(workspace_id=workspace_id, 
                                              environment_id=environment_id, 
                                              driver_cores=driver_cores)


# Environment libraries


workspace_id = 'affdg'
environment_id = 'bfdgfg'

# Get published libraries
resp = fc.get_published_libraries(workspace_id, environment_id)

# Upload staging library
resp = fc.upload_staging_library(workspace_id, environment_id, file_path='dummy.whl')

# Get staging libraries
resp = fc.get_staging_libraries(workspace_id, environment_id)

# Publish environment
resp = fc.publish_environment(workspace_id, environment_id)

# Cancel publish
resp = fc.cancel_publish(workspace_id, environment_id)

# Delete staging library
resp = fc.delete_staging_library(workspace_id, environment_id, 'dummy.whl')

```


## Eventhouses

```python	
from msfabricpysdkcore import FabricClientCore
fc = FabricClientCore()
workspace_id = 'd8a5abeieojfsdf-ab46-343bc57ddbe5'

# Create Eventhouse
eventhouse1 = fc.create_eventhouse(workspace_id, display_name="eventhouse1")

# List Eventhouses
eventhouses = fc.list_eventhouses(workspace_id)
eventhouse_names = [eh.display_name for eh in eventhouses]

# Get Eventhouse
eh = fc.get_eventhouse(workspace_id, eventhouse_name="eventhouse1")

# Update Eventhouse
eh2 = fc.update_eventhouse(workspace_id, eh.id, display_name="eventhouse2", return_item=True)

# Delete Eventhouse
status_code = fc.delete_eventhouse(workspace_id, eh.id)

# Get Eventhouse Definition
eventhouse_definition = fc.get_eventhouse_definition(workspace_id, eventhouse_id=eh.id, format = None):
eventhouse_definition = eventhouse_definition["definition"]

# Update Eventhouse Definition
fc.update_eventhouse_definition(workspace_id, eventhouse_id=eh.id, definition=eventhouse_definition, update_metadata = None):


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
es2 = fc.update_eventstream(workspace_id, es.id, display_name="es2", return_item=True)

# Delete Eventstream
fc.delete_eventstream(workspace_id, es.id)

# Get Eventstream Definition
eventstream_definition = fc.get_eventstream_definition(workspace_id, eventstream_id=es.id, format = None)
eventstream_definition = eventstream_definition["definition"]

# Update Eventstream Definition
fc.update_eventstream_definition(workspace_id, eventstream_id=es.id, definition=eventstream_definition, update_metadata = None)



```
## Eventstream Topology

```python
from msfabricpysdkcore import FabricClientCore

fcc = FabricClientCore()

workspace_id = "05basdfasdf1d3"

item_id = "94f4adfsff1b9"
custom_destination_id = "acdasdfasff2fb984d"
custom_source_id = "9f3829asdfasdf2ad3ecd"
source_id = "e58dasdfasf0540b17"
destination_id = "2446e6asdfasdfa3eb257"

# Get Eventstream Topology
topology = fcc.get_eventstream_topology(workspace_id, item_id)

# Get Eventstream Destination
destination = fcc.get_eventstream_destination(workspace_id, item_id, destination_id)

# Get Eventstream Destination Connection
destination_conn = fcc.get_eventstream_destination_connection(workspace_id, item_id, custom_destination_id)

# Get Eventstream Source
source = fcc.get_eventstream_source(workspace_id, item_id, source_id)

# Get Eventstream Source Connection
source_conn = fcc.get_eventstream_source_connection(workspace_id, item_id, custom_source_id)

# Pause Eventstream
resp = fcc.pause_eventstream(workspace_id, item_id)

# Resume Eventstream
resp = fcc.resume_eventstream(workspace_id, item_id, start_type="Now")

# Pause Eventstream Source
resp = fcc.pause_eventstream_source(workspace_id, item_id, source_id)

# Resume Eventstream Destination
resp = fcc.pause_eventstream_destination(workspace_id, item_id, destination_id)

# Resume Eventstream Source
resp = fcc.resume_eventstream_source(workspace_id, item_id, source_id, start_type="Now")

# Resume Eventstream Destination
resp = fcc.resume_eventstream_destination(workspace_id, item_id, destination_id, start_type="Now")

```
## GraphQL APIs

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List GraphQL APIs
graphql_apis = fc.list_graphql_apis(workspace_id = workspace_id)

# Create GraphQL API
graphql_api = fc.create_graphql_api(workspace_id = workspace_id, display_name="graphql_api1", description="description")

# Get GraphQL API
graphql_api = fc.get_graphql_api(workspace_id = workspace_id, graphql_api_name="graphql_api1", graphql_api_id=None)

# Update GraphQL API
graphql_api2 = fc.update_graphql_api(workspace_id = workspace_id, graphql_api_id = graphql_api.id, display_name="graphql_api2", description="description", return_item=True)

# Delete GraphQL API
fc.delete_graphql_api(workspace_id = workspace_id, graphql_api_id = graphql_api.id)

```



## KQL Dashboards

```python
from msfabricpysdkcore import FabricClientCore

# Create KQL Dashboard
kql_dash = fc.create_kql_dashboard(display_name="kql_dash_name", workspace_id="workspace_id")

# Delete KQL Dashboard
resp_code = fc.delete_kql_dashboard(workspace_id="w123", kql_dashboard_id="123123")

# Get KQL Dashboard
kql_dash2 = fc.get_kql_dashboard(workspace_id="w123", kql_dashboard_name="kql_dash_name")
kql_dash2 = fc.get_kql_dashboard(workspace_id="w123", kql_dashboard_id="123123")

# Get KQL Dashboard Definition
definition_orig = fc.get_kql_dashboard_definition(workspace_id="w123", kql_dashboard_id="dsfsf")

# Update KQL Dashboard
kql_dash3 = fc.update_kql_dashboard(workspace_id="w123", kql_dashboard_id="123123",
                                    display_name="new_name", return_item=True)

# Update KQL Dashboard Definition
definition = fc.update_kql_dashboard_definition(workspace_id="w123", kql_dashboard_id="2323", definition=definition_orig)

# List KQL Dashboards
kql_dashs = fc.list_kql_dashboards(workspace_id="w123")

```

## KQL Databases

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace_id = 'd8a5abe89jufojafds3bc57ddbe5'
evenhouse_id = "1482adfa290348238423428510a9197"

creation_payload = {"databaseType" : "ReadWrite",
                    "parentEventhouseItemId" : evenhouse_id}

# Create KQL Database
kqldb = fc.create_kql_database(workspace_id = workspace_id, display_name="kqldatabase12",
                                creation_payload=creation_payload)

# List KQL Databases
kql_databases = fc.list_kql_databases(workspace_id)
kql_database_names = [kqldb.display_name for kqldb in kql_databases]

# Get KQL Database
kqldb = fc.get_kql_database(workspace_id, kql_database_name="kqldatabase12")

# Update KQL Database
kqldb2 = fc.update_kql_database(workspace_id, kqldb.id, display_name="kqldb23", return_item=True)

# Delete KQL Database
status_code = fc.delete_kql_database(workspace_id, kqldb.id)

# Get KQL Database Definition
kql_database_definition = fc.get_kql_database_definition(workspace_id, kql_database_id=kqldb.id, format = None)

# Update KQL Database Definition
fc.update_kql_database_definition(workspace_id, kql_database_id=kqldb.id, definition=kql_database_definition, update_metadata = None)


```

## KQL Querysets

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

kqlq_w_content = fc.get_kql_queryset(workspace_id, kql_queryset_name=kql_queryset_name)
definition = fc.get_kql_queryset_definition(workspace_id, kqlq_w_content.id)
definition = definition["definition"]

# Create KQL Queryset
kqlq = fc.create_kql_queryset(workspace_id="workspace_id", definition=definition, display_name="kql_queryset_new")

# Delete KQL Queryset
status_code = fc.delete_kql_queryset(workspace_id="workspace_id", kql_queryset_id="kqlq.id")

# Get KQL Queryset
kqlq = fc.get_kql_queryset(workspace_id="workspace_id", kql_queryset_id="kqlq.id")
kqlq_w_content = fc.get_kql_queryset(workspace_id="workspace_id", kql_queryset_name="kql_queryset_name")

# Get KQL Queryset Definition
definition = fc.get_kql_queryset_definition(workspace_id="workspace_id", kql_queryset_id="kqlq.id")

# List KQL Querysets
kqlqs = fc.list_kql_querysets(workspace_id="workspace_id")

# Update KQL Queryset
kqlq2 = fc.update_kql_queryset(workspace_id="workspace_id", kql_queryset_id="kqlq.id", display_name="new_name", return_item=True)

# Update KQL Queryset Definition
fc.update_kql_queryset_definition(workspace_id="workspace_id", kql_queryset_id="kqlq.id", definition=definition)

```

## Lakehouse

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()
workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# Get Lakehouse
lakehouse = fc.get_lakehouse(workspace_id=workspace_id, item_name="lakehouse1")
lakehouse_id = lakehouse.id
date_str = datetime.now().strftime("%Y%m%d%H%M%S")
table_name = f"table{date_str}"

# Load Table
status_code = fc.load_table(workspace_id=workspace_id, lakehouse_id=lakehouse_id, table_name=table_name, 
                            path_type="File", relative_path="Files/folder1/titanic.csv")

# List Tables
table_list = fc.list_tables(workspace_id=workspace_id, lakehouse_id=lakehouse_id)


# Run on demand table maintenance
execution_data = {
    "tableName": table_name,
    "optimizeSettings": {
      "vOrder": True,
      "zOrderBy": [
        "tipAmount"
      ]
    },
    "vacuumSettings": {
      "retentionPeriod": "7:01:00:00"
    }
  }

fc.run_on_demand_table_maintenance(workspace_id=workspace_id, lakehouse_id=lakehouse_id, 
                                   execution_data = execution_data,
                                   job_type = "TableMaintenance", wait_for_completion = True)

# Create Lakehouse
lakehouse = fc.create_lakehouse(workspace_id=workspace_id, display_name="lakehouse2")
        
# List Lakehouses
lakehouses = fc.list_lakehouses(workspace_id)

# Get Lakehouse
lakehouse2 = fc.get_lakehouse(workspace_id=workspace_id, lakehouse_id=lakehouse.id)
        
# Update Lakehouse
lakehouse2 = fc.update_lakehouse(workspace_id=workspace_id, lakehouse_id=lakehouse.id, display_name="lakehouse3", return_item=True)

# Delete Lakehouse
fc.delete_lakehouse(workspace_id=workspace_id, lakehouse_id=lakehouse.id)

# List Livy Sessions
livy_sessions = fc.list_lakehouse_livy_sessions(workspace_id=workspace_id, lakehouse_id=lakehouse.id)

# Get Livy Session
livy_session = fc.get_lakehouse_livy_session(workspace_id=workspace_id, lakehouse_id=lakehouse.id, livy_id=livy_id)

```
## Mirrored Database

```python
from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

mirrored_db_w_content = fc.get_mirrored_database(workspace_id="workspace_id", mirrored_database_name="dbdemo")

# Get Mirroring Status
status = fc.get_mirroring_status(workspace_id="workspace_id", mirrored_database_id="mirrored_db_w_content.id")

# Get tables mirroring status
table_status = fc.get_tables_mirroring_status(workspace_id="workspace_id", mirrored_database_id="mirrored_db_w_content.id")

# Start Mirroring
fc.start_mirroring(workspace_id="workspace_id", mirrored_database_id="mirrored_db_w_content.id")

# Stop Mirroring
fc.stop_mirroring(workspace_id="workspace_id", mirrored_database_id="mirrored_db_w_content.id")

# Create Mirrored Database
mirrored_db = fc.create_mirrored_database(workspace_id="workspace_id", display_name="mirrored_db_name")

# Delete Mirrored Database
status_code = fc.delete_mirrored_database(workspace_id="workspace_id", mirrored_database_id="mirrored_db_check.id")

# Get Mirrored Database
mirrored_db_check = fc.get_mirrored_database(workspace_id="workspace_id", mirrored_database_id="mirrored_db.id")

# Get mirrored database definition
definition = fc.get_mirrored_database_definition(workspace_id="workspace_id", mirrored_database_id="mirrored_db_w_content.id")

# List Mirrored Databases
mirrored_dbs = fc.list_mirrored_databases(workspace_id="workspace_id")

# Update Mirrored Database
mirrored_db_2 = fc.update_mirrored_database(workspace_id="workspace_id", mirrored_database_id="mirrored_db_check.id",
                                            display_name="new_name", return_item=True)

# Update Mirrored Database Definition
fc.update_mirrored_database_definition(workspace_id="workspace_id", mirrored_database_id="mirrored_db_check.id", definition=definition)

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
mle2 = fc.update_ml_experiment(workspace_id, mle.id, display_name="mlexperiment2", return_item=True)

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
ml_model2 = fc.update_ml_model(workspace_id, ml_model_id=ml_model.id, display_name="mlmodel2", return_item=True)

# Delete ML Model
fc.delete_ml_model(workspace_id, ml_model.id)

```

## Mounted Data Factories

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Mounted Data Factories
mounted_data_factories = fc.list_mounted_data_factories(workspace_id = workspace_id)

mounted_data_factory_w_content = fc.get_mounted_data_factory(workspace_id = workspace_id, mounted_data_factory_name="HelloWorld")

# Create Mounted Data Factory
mounted_data_factory = fc.create_mounted_data_factory(workspace_id = workspace_id, display_name="mounted_data_factory1", description="description", definition=mounted_data_factory_w_content.definition)

# Get Mounted Data Factory
mounted_data_factory = fc.get_mounted_data_factory(workspace_id = workspace_id, mounted_data_factory_name="mounted_data_factory1", mounted_data_factory_id=None)

# Update Mounted Data Factory
mounted_data_factory2 = fc.update_mounted_data_factory(workspace_id = workspace_id, mounted_data_factory_id = mounted_data_factory.id, display_name="mounted_data_factory2", return_item=True)

# Delete Mounted Data Factory
fc.delete_mounted_data_factory(workspace_id = workspace_id, mounted_data_factory_id = mounted_data_factory.id)

# Get Mounted Data Factory Definition
mounted_data_factory_definition = fc.get_mounted_data_factory_definition(workspace_id = workspace_id, mounted_data_factory_id = mounted_data_factory.id, format=None)

# Update Mounted Data Factory Definition
fc.update_mounted_data_factory_definition(workspace_id = workspace_id, mounted_data_factory_id = mounted_data_factory.id, definition=mounted_data_factory_w_content.definition, update_metadata=None)

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
notebook2 = fc.update_notebook(workspace_id, notebook.id, display_name="notebook2", return_item=True)

# Get Notebook Definition
fc.get_notebook_definition(workspace_id, notebook.id, format=None)

# Update Notebook Definition
fc.update_notebook_definition(workspace_id, notebook.id, definition=definition)

# Delete Notebook
fc.delete_notebook(workspace_id, notebook.id)

# List Notebook Livy Sessions
notebook_livy_sessions = fc.list_notebook_livy_sessions(workspace_id, notebook.id)

# Get Notebook Livy Session
notebook_livy_session = fc.get_notebook_livy_session(workspace_id, notebook.id, livy_id=livy_id)

```

## Reports

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Reports
reports = fc.list_reports(workspace_id = workspace_id)

# Create Report
report_w_content = fc.get_report(workspace_id = workspace_id, report_name="HelloWorldReport")
definition = report_w_content.definition
report = fc.create_report(workspace_id = workspace_id, display_name="report1", definition=definition)

# Get Report
report = fc.get_report(workspace_id = workspace_id, report_name="report1")

# Get Report Definition
fc.get_report_definition(workspace_id = workspace_id, report_id = report.id, format=None)

# Update Report Definition
fc.update_report_definition(workspace_id = workspace_id, report_id = report.id, definition=definition)

# Update Report
fc.update_report(workspace_id = workspace_id, report_id = report.id, display_name = "name", description = "Description", return_item=False):

# Delete Report
fc.delete_report(workspace_id = workspace_id, report_id = report.id)

```

## Reflexes

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Reflexes
reflexes = fc.list_reflexes(workspace_id=workspace_id)

# Create Reflex
reflex_w_content = fc.get_reflex(workspace_id=workspace_id, reflex_name="HelloWorld")
definition = reflex_w_content.definition
reflex = fc.create_reflex(workspace_id=workspace_id, display_name="reflex1", description = "Description", definition=definition)

# Get Reflex
reflex = fc.get_reflex(workspace_id=workspace_id, reflex_name="reflex1")

# Get Reflex Definition
definition = fc.get_reflex_definition(workspace_id=workspace_id, reflex_id=reflex.id, format=None)

# Update Reflex
reflex2 = fc.update_reflex(workspace_id=workspace_id, reflex_id= reflex.id, display_name="reflex2", description = "Description", return_item=True)

# Update Reflex Definition
fc.update_reflex_definition(workspace_id=workspace_id, reflex_id= reflex.id, definition=definition)

# Delete Reflex
fc.delete_reflex(workspace_id=workspace_id, reflex_id=reflex.id)

```

## Semantic Models

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Semantic Models
semantic_models = fc.list_semantic_models(workspace_id="1232")

# Create Semantic Model
semantic_model_w_content = fc.get_semantic_model(workspace_id="1232", semantic_model_name="Table")
definition = semantic_model_w_content.definition
semantic_model = fc.create_semantic_model(workspace_id="1232", display_name="semanticmodel1", definition=definition)

# Get Semantic Model
semantic_model = fc.get_semantic_model(workspace_id="1232", semantic_model_name="semanticmodel1")
semantic_model = fc.get_semantic_model(workspace_id="1232", semantic_model_id="semantic_model.id")

# Get Semantic Model Definition
definition = fc.get_semantic_model_definition(workspace_id="1232", semantic_model_id="semantic_model.id", format=None)

# Update Semantic Model
fc.update_semantic_model(workspace_id="1232", semantic_model_id="semantic_model.id", display_name="new_name", return_item=True)

# Update Semantic Model Definition
fc.update_semantic_model_definition(workspace_id="1232", semantic_model_id="semantic_model.id", definition=definition)

# Delete Semantic Model
fc.delete_semantic_model(workspace_id="1232", semantic_model_id="semantic_model.id")

```

## Spark Livy Sessions

```python
from msfabricpysdkcore import FabricClientCore
fc = FabricClientCore()
workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List Spark Livy Sessions
spark_livy_sessions = fc.list_livy_sessions(workspace_id=workspace_id)

```

## Spark Custom Pools

```python	
workspace_id = "sfgsdfgs34234"

# List spark custom pools

pools = fc.list_workspace_custom_pools(workspace_id=workspace_id)
pool1 = [p for p in pools if p.name == "pool1"][0]

# Get a spark custom pool

pool1_clone = fc.get_workspace_custom_pool(workspace_id=workspace_id, pool_id=pool1.id)

# Create a spark custom pool

pool2 = fc.create_workspace_custom_pool(workspace_id=workspace_id, 
                                name="pool2", 
                                node_family="MemoryOptimized",
                                node_size="Small", 
                                auto_scale = {"enabled": True, "minNodeCount": 1, "maxNodeCount": 2},
                                dynamic_executor_allocation = {"enabled": True, "minExecutors": 1, "maxExecutors": 1})

# Update a spark custom pool

pool2 = fc.update_workspace_custom_pool(workspace_id=workspace_id, pool_id=pool2.id,
                                auto_scale = {"enabled": True, "minNodeCount": 1, "maxNodeCount": 7}, return_item=True)


# Delete a spark custom pool

status_code = fc.delete_workspace_custom_pool(workspace_id=workspace_id, pool_id=pool2.id)

```

## Spark Workspace Settings

```python

workspace_id = "io4i34t0sfg"

# Get spark settings

settings = fc.get_spark_settings(workspace_id)

# Update
settings["automaticLog"]["enabled"] = not settings["automaticLog"]["enabled"]
settings = fc.update_spark_settings(workspace_id, automatic_log=settings["automaticLog"])
  
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

# Run on demand spark job definition
job_instance = fc.run_on_demand_spark_job_definition(workspace_id, spark_job_definition.id, job_type="sparkjob")

# Update Spark Job Definition
spark_job_definition2 = fc.update_spark_job_definition(workspace_id, spark_job_definition.id, display_name="sparkjobdefinition2", return_item=True)

# Get Spark Job Definition Definition
fc.get_spark_job_definition_definition(workspace_id, spark_job_definition.id, format=None)

# Update Spark Job Definition Definition
fc.update_spark_job_definition_definition(workspace_id, spark_job_definition.id, definition=definition)

# Delete Spark Job Definition
fc.delete_spark_job_definition(workspace_id, spark_job_definition.id)

# List Spark Job Definition Livy Sessions
spark_job_definition_livy_sessions = fc.list_spark_job_definition_livy_sessions(workspace_id, spark_job_definition.id)

# Get Spark Job Definition Livy Session
spark_job_definition_livy_session = fc.get_spark_job_definition_livy_session(workspace_id, spark_job_definition.id, livy_id=livy_id)



```

## SQL Databases

```python

from msfabricpysdkcore import FabricClientCore

fc = FabricClientCore()

workspace = fc.get_workspace_by_name("testitems")
workspace_id = workspace.id

# List SQL Databases
sql_databases = fc.list_sql_databases(workspace_id=workspace_id)

# Create SQL Database
sql_database = fc.create_sql_database(workspace_id=workspace_id, display_name="sqldb1", description="description")

# Get SQL Database
sql_database = fc.get_sql_database(workspace_id=workspace_id, sql_database_name="sqldb1")

# Update SQL Database
sql_database2 = fc.update_sql_database(workspace_id=workspace_id, sql_database_id=sql_database.id, display_name="sqldb2", description="description", return_item=True)

# Delete SQL Database
fc.delete_sql_database(workspace_id=workspace_id, sql_database_id=sql_database.id)

```

## Variable Libraries

```python
from msfabricpysdkcore import FabricClientCore
fcc = FabricClientCore()

workspace_id = "0asdfasdf8151d3"
item_id = "0812fasdfsdf2709ec"

# get variable library definition
variable_library_definition = fcc.get_variable_library_definition(workspace_id=workspace_id, variable_library_id=item_id)
definition = variable_library_definition["definition"]


# create variable library
date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_str = date_str.replace(" ", "T").replace(":", "").replace("-", "")
date_str = f"variablelibrary{date_str}"

variable_library_new = fcc.create_variable_library(workspace_id=workspace_id, display_name=date_str, definition=definition)


# get variable library
variable_library_get = fcc.get_variable_library(workspace_id=workspace_id, variable_library_id=variable_library_new.id)

# list variable libraries
variable_librarys = fcc.list_variable_libraries(workspace_id=workspace_id)

# update variable library
date_str_updated = date_str + "_updated"
variable_library_updated = fcc.update_variable_library(workspace_id=workspace_id, variable_library_id=variable_library_new.id, display_name=date_str_updated, return_item=True)

# update variable library definition
variable_library_updated = fcc.update_variable_library_definition(workspace_id=workspace_id, variable_library_id=variable_library_new.id, definition=definition)

# delete variable library
resp = fcc.delete_variable_library(workspace_id=workspace_id, variable_library_id=variable_library_updated.id)

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
warehouse2 = fc.update_warehouse(workspace_id, warehouse.id, display_name="wh2", return_item=True)

# Delete Warehouse
fc.delete_warehouse(workspace_id, warehouse.id)

```


# gen_dash_from_metrics_list.py

A tool to help generate Grafana dashboards from file with list of Kafka metrics
Tested with Python 3.11, should work with 3.9+.

## How to use this tool

### Create input files

Create files with list of metrics, and file name should be same as "job" label, which is used for filtering.

For example, file `kafka-broker-ingress.txt`:

```
kafka_app_info_start_time_ms
kafka_producer_batch_size_avg
kafka_producer_batch_size_max
...
```

will generate dashboard json `dashboard-kafka-broker-ingress.json` (in same directory where script is run). This dashboard will have time series per metric name in input txt file. Each time series will be filtered with `job=kafka-broker-ingress`, job name is name of input txt file without extention.

### Set env vars:

```
DATASOURCE='{"type": "prometheus","uid": "1111111-1111-1111-1111-111111111111"}'
```

DATASOURCE is json of datasource to use in dashboards.

```
METRICS_FILES="kafka-broker-ingress.txt,kafka-sink-ingress.txt"
```

list of file paths - each file has metrics list in them, newline separated (like kafka-broker-ingress.txt snippet above).


Set optional env vars:

```
DASH_TEMPLATE_FILE="dash.txt"
```

File with template of dashboard (__title__, __metrics_list__, __uid__, __metrics_list__ placeholders).
Default dash-template-json.txt.

```
METRIC_TEMPLATE_FILE="metric.txt"
```

File with template of panel (time series), __metric__, __job_name__, __datasource__ placeholders.
Default metric-template-json.json.


### Run

```
>  python .\gen_dash_from_metrics_list.py
```

This will create a number of `dashboard-*.json` files in same directory.

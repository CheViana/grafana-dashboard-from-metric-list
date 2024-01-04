import random
import string
import os
import pathlib
import json


def get_unquoted_lines(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    lines = file_contents.split('\n')
    return [line.replace('"', "") for line in lines]


def get_template_content(file_path):
    with open(file_path, 'r') as file:
        template_content = file.read()
    return template_content

def get_random_str(n):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def gen_uid():
    return '-'.join([
        get_random_str(8),
        get_random_str(4),
        get_random_str(4),
        get_random_str(4),
        get_random_str(12)
    ])


def generate_grafana_dashboard_json(metrics_file_path):
    metrics = get_unquoted_lines(metrics_file_path)
    metrics = list(set(metrics))
    job_name = pathlib.Path(metrics_file_path).stem

    print(f"Job {job_name} has {len(metrics)} metrics")

    template_content = get_template_content(
        os.getenv("METRIC_TEMPLATE_FILE", "metric-template-json.json")
    )
    datasource = {
        "type": "prometheus",
        "uid": "1111111-1111-1111-1111-111111111111"
    }
    if os.getenv("DATASOURCE"):
        datasource = json.loads(os.getenv("DATASOURCE"))
    metrics_list = [
        template_content.replace(
            "__metric__", metric
        ).replace(
            "__job_name__", job_name
        ).replace(
            "__datasource__", json.dumps(datasource)
        ).replace("__UID__", gen_uid()) for metric in metrics
    ]
    metrics_text = ",".join(metrics_list)
    dashboard_content = get_template_content(
        os.getenv("DASH_TEMPLATE_FILE", "dash-template-json.txt")
    )
    dashboard = dashboard_content.replace(
        "__datasource__", json.dumps(datasource)
    ).replace(
        "__title__", f"{job_name} Kafka metrics"
    ).replace(
        "__UID__", gen_uid()
    ).replace(
        "__metrics_list__", metrics_text
    )
    with open(f'dashboard-{job_name}.json', 'w') as file:
        file.write(dashboard)


if __name__ == "__main__":
    metrics_file_paths = os.getenv("METRICS_FILES", "job.txt").split(',')
    # metrics_file_paths = [
    # #     "kafka-broker-dispatcher.txt",
    # #     "kafka-broker-ingress.txt",
    # #     "kafka-sink-ingress.txt"
    #     "source-metrics-service.txt"
    # ]
    for metrics_file_path in metrics_file_paths:
        generate_grafana_dashboard_json(metrics_file_path)

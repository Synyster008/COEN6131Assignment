from concurrent import futures
import time

import grpc
import server_pb2
import server_pb2_grpc
import pandas as pd
import json
import statistics as st
import numpy as np
from flask import Flask, request, json

app = Flask(__name__)


@app.route('/fetcher', methods=['GET'])
def fetcher():
    workload_files = {
        '1': 'DVD-testing.csv',
        '2': 'DVD-training.csv',
        '3': 'NDBench-testing.csv',
        '4': 'NDBench-training.csv'
    }

    metric = {
        '1': 'CPUUtilization_Average',
        '2': 'NetworkIn_Average',
        '3': 'NetworkOut_Average',
        '4': 'MemoryUtilization_Average',
    }

    request_info = server_pb2.RequestInfo.FromString(request.data)
    result = server_pb2.Response()
    rfw_id = request_info.r_id
    benchmark_type = request_info.benchmark_type
    workload_metric = request_info.workload_metric
    batch_unit = request_info.batch_unit
    batch_id = request_info.batch_id
    batch_size = request_info.batch_size
    file_type = request_info.file_type

    no_of_samples = int(batch_unit) * int(batch_size)
    initial = int(batch_id) * int(batch_unit)
    m = int(batch_id)

    if benchmark_type == '1':
        benchmark = str(int(benchmark_type) * int(file_type))
    else:
        benchmark = str(int(benchmark_type) + int(file_type))

    df = pd.read_csv(workload_files[benchmark])
    requested_data = df[metric[workload_metric]][initial + 1:no_of_samples + initial + 1]

    max_batch_id = len(df) / int(batch_unit)

    if (m + 10 > max_batch_id):
        print("Batch ID or Batch Size out of range")
        quit()

    row = []
    for line in requested_data:
        row.append(line)

    analytics = {
        'avg': np.average(row),
        'max': max(row),
        'min': min(row),
        'std': round(st.stdev(row), 2),
        '10p': len([i for i in row if i >= round(np.percentile(row, 10), 2)]),
        '50p': len([i for i in row if i >= round(np.percentile(row, 50), 2)]),
        '95p': len([i for i in row if i >= round(np.percentile(row, 90), 2)]),
        '99p': len([i for i in row if i >= round(np.percentile(row, 99), 2)]),
    }

    print(analytics)

    #final = [row[i * int(batch_unit):(i + 1) * int(batch_unit)] for i in
             #range((len(row) + int(batch_unit) - 1) // int(batch_unit))]

    id = str(initial + int(batch_size) - 1)

    response = {'RFW ID': rfw_id, 'Last batch ID': id, 'Requested data': row,
                'Analytics': analytics}

    print(response)

    result.rfw_id = response['RFW ID']
    result.last_batch_id = response['Last batch ID']
    result.requested_data.extend(response['Requested data'])
    #for num in response['Requested data']:
        #result.requested_data.append(num)

    result.avg = response['Analytics']['avg']
    result.max = response['Analytics']['max']
    result.min = response['Analytics']['min']
    result.std = response['Analytics']['std']
    result.p10 = response['Analytics']['10p']
    result.p50 = response['Analytics']['50p']
    result.p95 = response['Analytics']['95p']
    result.p99 = response['Analytics']['99p']

    if result is not None:
        serialized_data = result.SerializeToString()
        return serialized_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

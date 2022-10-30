import pandas as pd
import json
import statistics as st
import numpy as np

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

rfw_id = input("RFW ID :\n")
benchmark_type = input(
    'Benchmark type : \n 1: DVD \n 2:NDBench\n ')
workload_metric = input(
    " Workload metric : \n 1: Cpu utilization average\n 2: Network in average\n 3: Network out average\n 4: Memory utilization average\n 5: Final target \n")
batch_unit = input('Batch Unit :\n')
batch_size = input('Batch Size :\n')
batch_id = input('Batch ID(starts from 0) :\n')
file_type = input("Type : \n 1: Testing \n 2: Training\n")

no_of_samples = int(batch_unit) * int(batch_size)
initial = int(batch_id) * int(batch_unit)
m = int(batch_id)

if benchmark_type== '1':
    benchmark = str(int(benchmark_type)*int(file_type))
else:
    benchmark = str(int(benchmark_type)+int(file_type))


try:
    df = pd.read_csv(workload_files[benchmark])
    requested_data = df[metric[workload_metric]][initial + 1:no_of_samples + initial + 1]
except:
    print("Enter a valid key please!")
    quit()

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

final = [row[i * int(batch_unit):(i + 1) * int(batch_unit)] for i in
         range((len(row) + int(batch_unit) - 1) // int(batch_unit))]

response = {'RFW ID': rfw_id, 'Last batch ID': initial + int(batch_size) - 1, 'Requested data': row,
            'Analytics': analytics}

json_format = json.dumps(response)

with open('app.json', 'w') as f:
    json.dump(json_format, f)

with open('app.json') as file:
    data = json.load(file)

print(data)

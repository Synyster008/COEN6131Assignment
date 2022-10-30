import requests

r_id = input("RFW ID :\n")
benchmark_type = input(
    'Benchmark type : \n 1: DVD \n 2:NDBench\n ')
workload_metric = input(
    " Workload metric : \n 1: CPU Utilization Average\n 2: Network In Average\n 3: Network Out average\n 4: Memory Utilization Average\n")
batch_unit = input('Batch Unit :\n')
batch_size = input('Batch Size :\n')
batch_id = input('Batch ID(starts from 0) :\n')
file_type = input("Type : \n 1: Testing \n 2: Training\n")

result = requests.get("http://192.168.2.18:5000/fetcher?",
                      json= {"r_id": r_id,
                         "benchmark_type": benchmark_type,
                         "workload_metric": workload_metric,
                         "batch_unit": batch_unit,
                         "batch_id": batch_id,
                         "batch_size": batch_size,
                         "file_type": file_type}, 
                         timeout=600
                      )
if result.status_code == 200:
    print(" RFW_ID: ", result.json()['RFW ID'])
    print(" Last_batch_ID: ", result.json()['Last batch ID'])
    print(" Samples Requested: ", result.json()['Requested data'])
    print(" Analytics: ", result.json()['Analytics'])

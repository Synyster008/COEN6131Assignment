import server_pb2_grpc
import server_pb2
import time
import grpc
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

request_info = server_pb2.RequestInfo()

request_info.r_id = r_id
request_info.benchmark_type = benchmark_type
request_info.workload_metric = workload_metric
request_info.batch_unit = int(batch_unit)
request_info.batch_size = int(batch_size)
request_info.batch_id = int(batch_id)
request_info.file_type = file_type

result = requests.get("http://192.168.2.18:5000/fetcher?",
                      headers={'Content-Type': 'application/protobuf'},
                      data= request_info.SerializeToString())

response = server_pb2.Response.FromString(result.content)
print(response)
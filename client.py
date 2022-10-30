import server_pb2_grpc
import server_pb2
import time
import grpc

def get_client_stream_requests():
    while True:
        request_info = server_pb2.RequestInfo(greeting = "Hello", name = name)
        yield request_info
        time.sleep(1)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.AnalyserStub(channel)
        rfw_id = input("RFW ID :\n")
        benchmark_type = input(
            'Benchmark type : \n 1: DVD testing \n 2: DVD training\n 3: NDBench testing\n 4: NDBench training\n ')
        workload_metric = input(
            " Workload metric : \n 1: Cpu utilization average\n 2: Network in average\n 3: Network out average\n 4: Memory utilization average\n 5: Final target \n")
        batch_unit = input('Batch Unit :\n')
        batch_size = input('Batch Size :\n')
        batch_id = input('Batch ID(starts from 0) :\n')

        responses = stub.SendRequest(get_client_stream_requests())

        for response in responses:
            print("InteractingHello Response Received: ")
            print(response)

if __name__ == "__main__":
    run()
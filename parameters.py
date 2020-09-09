import numpy as np 
import math
import random

num_devices        = 3
packet_size        = 64 # bits
sample_sizes       = packet_size * np.random.randint(1, 5, size=num_devices) # bits
# print(sample_sizes)
packets_per_sample = [math.ceil(x*1.00/packet_size) for x in sample_sizes]
# print(packets_per_sample)

# print(users)
total_packets      = np.sum(packets_per_sample)
sample_priority    = np.array([1,1,1])
number_of_RBs      = 3
modulation_orders = [2,4,6,8]
base_throughput = 1.07 # in Mbps
throughputs = [base_throughput, 2*base_throughput, 3*base_throughput, 4*base_throughput]

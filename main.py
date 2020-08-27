#######################

### The assumptions are listed below - 

# 1. Samples generated by the users are of variable sizes.
# 2. When they are sent to the scheduler, scheduler breaks these samples down into uniform sized packets. So effectively every component may generate different number of packets to transmit.
# 3. Every RB can transmit 1 packet at a time. Bo Zhou's papers and many other follow this.
# 4. If a component has packets from different samples and enough RBs are available to support them, only the packets from the old sample will be transmitted first. The remaining RBs will then be allocated to the next users. So bottomline is that at any time, only packets belonging to the same sample will be considered for transmission.
# 5. A sample is fully transmitted only when all the packets belonging to the sample is delivered. So Age will reduce only the whole sample is transferred completely. First considered in <https://ieeexplore.ieee.org/abstract/document/8761311>
# 6. No packet loss is being considered now - a RB allocated to a packet means that packet will be delivered for sure.

#######################



#!/home/biplav/anaconda3/bin/python
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from parameters import *
import random
import sys 
import pickle



# random.seed(3)

def schedule(data, data_gen_time): 
# data is a dict with key as user and value as number of packets in its current sample, 
# data_gen_time is a dict with key as user and value as generation time of the packets in the current sample, 

    global slot_number # will be incremented by 1 every time the function schedule is called

    slot_number = slot_number + 1 # analagous to current time
    print("\n\nAt slot ", slot_number, ", data is ", data, " and their gen_times are ", data_gen_time)
    for i in device_list:
        # d1[i] = d1[+]
        d2[i] = d2[i] + data[i] # total packets per user updated
        d3[i].append(data[i]) # total packets in the current sample per user appended
        d3_time[i].append(data_gen_time[i])

    print("d2 = ", d2)
    print("current_sample = ", current_sample)
    print("d3 = ", d3)
    print("d3_time = ", d3_time)
    print("receptions = ", receptions)

    RB_used            =  0
    RB_remaining       = number_of_RBs
    delay              = [] 
    PER                = []
    # print(total_packets, "packets as in ", packets_per_sample, " to be scheduled with", number_of_RBs, "RBs")

    for user in data: 
        max_MCS = np.random.randint(10,28) # MCS corresponding to the tx-rx pair based on the MCS
        RB_needed      = d3[user][current_sample[user]]
        print("user ", user,"at slot ", slot_number,"RB_needed = ", RB_needed)


        if (RB_needed == 0): # user has nothng to send
            print("user ", user, " has no packets")
            current_sample[user] = current_sample[user]+1


        if (RB_needed > 0) & (RB_remaining - RB_needed >= 0): # current user's current sample can be fully served
            print("user", user, "'s ", current_sample[user]," sample will be served, max MCS =", max_MCS, ", RB_needed =", RB_needed, " RBs available = ", RB_remaining)
            RB_remaining = RB_remaining - RB_needed
            current_sample_delay = slot_number-current_sample[user]
            print("user", user, "served with delay=", current_sample_delay, "remaining RBs=", RB_remaining)
            delay.append(current_sample_delay)
            receptions[user].append([slot_number, current_sample_delay])
            # d1[user] = 0 # d1 needed ??
            d2[user] = d2[user] - RB_needed # total packets remaining has decremented
            d3[user][current_sample[user]] = d3[user][current_sample[user]] - RB_needed # # total packets of the current sample remaining has decremented
            current_sample[user] = current_sample[user]+1
            print_res("FULL", user)

        
        elif (RB_remaining!=0): # current user's current sample can be partially served
            print("user", user, " will be partially served as RBs needed =", RB_needed, "> RBs remaining =", RB_remaining, ", only", RB_remaining, "packets will be sent")
            d2[user] = d2[user] - RB_remaining # total packets remaining
            d3[user][current_sample[user]] = d3[user][current_sample[user]] - RB_remaining # # total packets of the current sample remaining
            RB_remaining = 0
            delay.append(1000000) # complete transfer pending
            print_res("PARTIAL", user)


        elif (RB_remaining==0):
            print("user", user, " cannot be served as no RBs remaining")
            delay.append(1000000) # complete transfer pending
            print_res("NONE", user)

    
    pickle.dump(slot_number, open("slot_number.pickle", "wb"))
    pickle.dump(device_list, open("device_list.pickle", "wb"))
    pickle.dump(d2, open("d2.pickle", "wb"))
    pickle.dump(current_sample, open("current_sample.pickle", "wb"))
    pickle.dump(d3, open("d3.pickle", "wb"))
    pickle.dump(receptions, open("receptions.pickle", "wb"))
    pickle.dump(d3_time, open("d3_time.pickle", "wb"))


    return (delay, PER)



def print_res(str, user): # str will be either full, partial, none meaning the amount of transfer done

    print("user ", user,"at slot ", slot_number," finished with action ", str, " and the current status is ")
    print("d2 = ", d2)
    print("current_sample = ", current_sample)
    print("d3 = ", d3)
    print("d3_time = ", d3_time)
    print("receptions = ", receptions)




try: # will execute for the all future calls

    # foo = pickle.load(open("var.pickle", "rb"))
    slot_number = pickle.load(open("slot_number.pickle", "wb"))
    device_list =  pickle.load(open("device_list.pickle", "wb"))
    d2 =  pickle.load(open("d2.pickle", "wb"))
    current_sample =  pickle.load(open("current_sample.pickle", "wb"))
    d3 =  pickle.load(open("d3.pickle", "wb"))
    receptions =  pickle.load(open("receptions.pickle", "wb"))
    d3_time =  pickle.load(open("receptions.pickle", "wb"))
except (OSError, IOError) as e: # will execute for the first call
    # foo = 3
# if __name__ == '__main__':

    slot_number = -1
    # initialize dictionaries
    device_list = np.arange(num_devices)
    # d1 = {key:0 for key in device_list} # is d1 needed ?
    d2 = {key:0 for key in device_list} # total packet waiting per user

    current_sample = {key:0 for key in device_list} # 1 value per user will represent the sample being served for that user
    d3 = {key:[] for key in device_list} # packets per sample per function call will be appended, made to 0 on an FCFS basis
    d3_time = {key:[] for key in device_list} # will contain the generation time of the samples corresponding to the same index in dict d3

    receptions = {key:[] for key in device_list} # append the [current_time, delay] for every complete sample reception

# users is a dict with key as user index and value as number of packets in his sample
# for i in range(5):

    # PSCAD_data = {0:2, 1:2, 2:1}
    # PSCAD_data_gen_time = {0:i, 1:i, 2:i}
    # res_delay, res_PER = schedule(PSCAD_data, PSCAD_data_gen_time)
    # print(res_delay, res_PER)

f=open("test.txt","r")
lines=f.readlines()
PSCAD_total_data = [] # both the data and gentime will be put here
PSCAD_data = {}
PSCAD_data_gen_time = {}
for x in lines:
    PSCAD_total_data.append(int(x[0]))
f.close()
# print(PSCAD_total_data)

for i in range(num_devices):
    PSCAD_data[i] = PSCAD_total_data[i]

for i in range(num_devices, len(PSCAD_total_data)):
    PSCAD_data_gen_time[i-num_devices] = PSCAD_total_data[i]

# print("PSCAD_data = ", PSCAD_data, "PSCAD_data_gen_time = ", PSCAD_data_gen_time)
res_delay, res_PER = schedule(PSCAD_data, PSCAD_data_gen_time)
# print(res_delay, res_PER)
print(*res_delay, sep = " ", file = open("result.txt", "w"))
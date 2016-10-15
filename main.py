from sys import argv

script, filename = argv

txt = open(filename)

print txt.read()

with open(filename) as f:
    lines = f.readlines()

data = []

for line in lines:
    if line[0] != '#':
        proc_id, initial_arrival_time, cpu_burst_time, num_bursts, io_time = line.split("|")
        arguments = [proc_id, initial_arrival_time, cpu_burst_time, num_bursts, io_time]
        data.append(arguments)
        print proc_id, initial_arrival_time, cpu_burst_time, num_bursts, io_time

Q = []
FCFS()

Q = []
SJF()

Q = []
RR()

def FCFS():
    pass

def SJF():
    pass

def RR():
    pass
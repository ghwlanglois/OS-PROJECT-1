def FCFS(data):
    time = 0
    print("time 0ms: Simulator started for FCFS [Q empty]")
    while True:
        for process in data:
            if process['state'] == 'READY' and int(process['initial_arrival_time']) == time:
                proc_id = process['process_id']
                Q.append(proc_id)
                name = " ".join(map(str,Q))
                print("time "+str(time)+"ms: Process "+proc_id+" arrived [Q "+name+"]")
            
        
        time += 1
        if time == 10000:
            break
    
def SJF(data):
    time = 0
    print("\ntime 0ms: Simulator started for SJF [Q empty]")

def RR(data):
    time = 0
    print("\ntime 0ms: Simulator started for RR [Q empty]")

n = 1
m = 1
t_cs = 8
t_slice = 84

from sys import argv
script, filename = argv
txt = open(filename)
#print txt.read()
with open(filename) as f:
    lines = f.readlines()

# Copy all of the line data into a nested array of strings containing the values
data = []
for line in lines:
    if line[0] != '#':
        proc_id, initial_arrival_time, cpu_burst_time, num_bursts, io_time = line.split("|")
        process = {
            'process_id': proc_id,
            'initial_arrival_time': initial_arrival_time,
            'cpu_burst_time': cpu_burst_time,
            'num_bursts': num_bursts,
            'io_time': io_time,
            'state': 'READY'
        }
        data.append(process)

Q = []
FCFS(data)

Q = []
SJF(data)

Q = []
RR(data)

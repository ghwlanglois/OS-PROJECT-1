def FCFS():
    global current_process
    global time
    global Q
    
    current_process = None
    time = 0
    Q = []
    
    cs = 1
    total_done = 0
    
    print("time 0ms: Simulator started for FCFS [Q empty]")
    while True:
        for process in data:
            if process['state'] == 'READY' and int(process['initial_arrival_time']) == time:
                Q.append(process)
                print("time "+str(time)+"ms: Process "+process['process_id']+" arrived [Q "+StringQ()+"]")
            if process['state'] == 'BLOCKED':
                if process['io_time_end'] == time:
                    process['state'] = 'READY'
                    Q.append(process)
                    print("time "+str(time)+"ms: Process "+process['process_id']+" completed I/O [Q "+StringQ()+"]")
        
        if cs == 1:
            if total_done == len(data):
                break
            if current_process == None and len(Q)>0:
                current_process = Q[0]
                Q.remove(Q[0])
                current_process['state'] = 'RUNNING'
                #addTime(t_cs/2)
                cs = 4
                current_process['cpu_burst_time_end'] = current_process['cpu_burst_time']+time+cs
                print("time "+str(time+cs)+"ms: Process "+current_process['process_id']+" started using the CPU [Q "+StringQ()+"]")
            
            if current_process != None:
                if current_process['cpu_burst_time_end'] == time:
                    current_process['num_bursts_left'] -= 1
                    #addTime(t_cs/2)
                    cs = 4
                    if current_process['num_bursts_left'] == 0:
                        print("time "+str(time)+"ms: Process "+current_process['process_id']+" terminated [Q "+StringQ()+"]")
                        current_process = None
                        total_done += 1
                        #continue
                    else:
                        current_process['io_time_end'] = current_process['io_time']+time
                        #print process['io_time_end']
                        print("time "+str(time)+"ms: Process "+current_process['process_id']+" completed a CPU burst; "+str(current_process['num_bursts_left'])+" to go [Q "+StringQ()+"]")
                        print("time "+str(time)+"ms: Process "+current_process['process_id']+" blocked on I/O until time "+str(current_process['io_time_end'])+"ms [Q "+StringQ()+"]")
                        current_process['state'] = 'BLOCKED'
                    #addTime(t_cs/2)
                    #cs += 4
                    current_process = None
        else:
            cs -= 1
        
        time += 1
        
    print("time "+str(time)+"ms: Simulator started for SJF [Q empty]")
    
def SJF():
    print("\ntime 0ms: Simulator started for SJF [Q empty]")

def RR():
    print("\ntime 0ms: Simulator started for RR [Q empty]")

def StringQ():
    if len(Q) > 0:
        q = []
        for process in Q:
            proc_id = process['process_id']
            q.append(proc_id)
        return " ".join(map(str,q))
    else:
        return "empty"

def addTime(t):
    global time
    global current_process
    #if t>1:
    #    print "added",t,"ms at time ", time,"ms"
    time += t
    #if current_process != None:
        #current_process['cpu_burst_time_left'] -= t
    for process in data:
        #if process['state'] == 'BLOCKED':
            #process['io_time_left'] -= t
        if process['state'] == 'READY':
            process['wait_time'] += t

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
            'initial_arrival_time': int(initial_arrival_time),
            'cpu_burst_time': int(cpu_burst_time),
            'cpu_burst_time_end': int(cpu_burst_time)+int(initial_arrival_time),
            'num_bursts': int(num_bursts),
            'num_bursts_left': int(num_bursts),
            'io_time': int(io_time),
            'io_time_end': int(io_time)+int(cpu_burst_time)+int(initial_arrival_time),
            'wait_time': 0,
            'state': 'READY'
        }
        data.append(process)

current_process = None
time = 0
Q = []

FCFS()
#SJF()
#RR()

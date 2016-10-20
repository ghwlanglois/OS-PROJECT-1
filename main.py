import sys

def ScheduleProcesses(FCFS,SJF,RR):
    global Q
    global data
    
    current_process = None
    time = 0
    
    cs = 1
    total_done = 0
    
    if FCFS:
        sys.stdout.write("time 0ms: Simulator started for FCFS [Q empty]\n")
    elif SJF:
        sys.stdout.write("\ntime 0ms: Simulator started for SJF [Q empty]\n")
    elif RR:
        sys.stdout.write("\ntime 0ms: Simulator started for RR [Q empty]\n")
    
    while True:
        for process in data:
            # If the process is ready to be initialized in the Q
            if process['state'] == 'READY' and int(process['initial_arrival_time']) == time:
                Q.append(process)
                sys.stdout.write("time "+str(time)+"ms: Process "+process['process_id']+" arrived [Q "+StringQ()+"]\n")
            # Check for I/O completion on blocked processes
            if process['state'] == 'BLOCKED':
                if process['io_time_end'] == time:
                    process['state'] = 'READY'
                    Q.append(process)
                    sys.stdout.write("time "+str(time)+"ms: Process "+process['process_id']+" completed I/O [Q "+StringQ()+"]\n")
        
        # Tally the wait time of each process while it's in the Q
        for process in Q:
            if process['state'] == 'READY':
                process['wait_time'] += 1
        
        # If not in the middle of a context switch
        if cs == 1:
            # Exit the algorithm if all the processes have terminated
            if total_done == n or time > 11349:
                break
            
            if SJF and len(Q)>0:
                Q_SJF = sorted(Q, key=lambda k: k['cpu_burst_time'])
                Q = Q_SJF
            
            # If there isn't currently a process runnning and the Q isn't empty
            # then start the process and remove if from the Q
            if current_process == None and len(Q)>0:
                current_process = Q[0]
                Q.remove(Q[0])
                current_process['state'] = 'RUNNING'
                # Flag for the context switch
                cs = t_cs/2
                if RR:
                    if current_process['cpu_burst_time_left'] <= t_slice:
                        current_process['cpu_burst_time_end'] = current_process['cpu_burst_time_left']+time+cs
                    else:
                        current_process['cpu_burst_time_end'] = t_slice+time+cs
                else:
                    current_process['cpu_burst_time_end'] = current_process['cpu_burst_time']+time+cs
                sys.stdout.write("time "+str(int(time+cs))+"ms: Process "+current_process['process_id']+" started using the CPU [Q "+StringQ()+"]\n")
            
            # If there is already a process running and its CPU burst is over, then block the I/O
            # or terminate the process entirely
            if RR:
                if current_process != None:
                    if current_process['cpu_burst_time_end'] == time:
                        # Flag for the context switch
                        cs = t_cs/2
                        if current_process['cpu_burst_time_left'] <= 0:
                            current_process['num_bursts_left'] -= 1
                            if current_process['num_bursts_left'] == 0:
                                cs += t_cs/2+current_process['cpu_burst_time_left']
                                sys.stdout.write("time "+str(int(time+cs/2))+"ms: Process "+current_process['process_id']+" terminated [Q "+StringQ()+"]\n")
                                current_process = None
                                total_done += 1
                            else:
                                current_process['cpu_burst_time_left'] = current_process['cpu_burst_time']+1
                                current_process['io_time_end'] = current_process['io_time']+time
                                sys.stdout.write("time "+str(time)+"ms: Process "+current_process['process_id']+" completed a CPU burst; "+str(current_process['num_bursts_left'])+" to go [Q "+StringQ()+"]\n")
                                sys.stdout.write("time "+str(time)+"ms: Process "+current_process['process_id']+" blocked on I/O until time "+str(current_process['io_time_end'])+"ms [Q "+StringQ()+"]\n")
                                current_process['state'] = 'BLOCKED'
                            current_process = None
                        elif current_process['cpu_burst_time_left'] > 0:
                            if len(Q)>0:
                                process['state'] = 'READY'
                                Q.append(current_process)
                                time_to_go = current_process['cpu_burst_time_left']
                                sys.stdout.write("time "+str(time)+"ms: Time slice expired; process "+current_process['process_id']+" preempted with "+str(time_to_go)+"ms to go [Q "+StringQ()+"]\n")
                                current_process = None
                            else:
                                sys.stdout.write("time "+str(time)+"ms: Time slice expired; no preemption because ready queue is empty [Q empty]\n")
                                cs -= 3
                                time -= 1
                                current_process['cpu_burst_time_left'] = current_process['cpu_burst_time']+1
                                if current_process['cpu_burst_time_left'] <= t_slice:
                                    current_process['cpu_burst_time_end'] = current_process['cpu_burst_time_left']+time+cs
                                else:
                                    current_process['cpu_burst_time_end'] = t_slice+time+cs
                if current_process != None:
                    current_process['cpu_burst_time_left'] -= 1
            else:
                if current_process != None:
                    if current_process['cpu_burst_time_end'] == time:
                        current_process['num_bursts_left'] -= 1
                        # Flag for the context switch
                        cs = t_cs/2
                        if current_process['num_bursts_left'] == 0:
                            sys.stdout.write("time "+str(time)+"ms: Process "+current_process['process_id']+" terminated [Q "+StringQ()+"]\n")
                            current_process = None
                            total_done += 1
                        else:
                            current_process['io_time_end'] = current_process['io_time']+time
                            sys.stdout.write("time "+str(time)+"ms: Process "+current_process['process_id']+" completed a CPU burst; "+str(current_process['num_bursts_left'])+" to go [Q "+StringQ()+"]\n")
                            sys.stdout.write("time "+str(time)+"ms: Process "+current_process['process_id']+" blocked on I/O until time "+str(current_process['io_time_end'])+"ms [Q "+StringQ()+"]\n")
                            current_process['state'] = 'BLOCKED'
                        current_process = None
        # If in the middle of a context switch
        else:
            cs -= 1
        # Step the program forward
        time += 1
    if FCFS:
        sys.stdout.write("time "+str(time)+"ms: Simulator ended for FCFS\n")
    elif SJF:
        sys.stdout.write("time "+str(time)+"ms: Simulator ended for SJF\n")
    elif RR:
        sys.stdout.write("time "+str(time)+"ms: Simulator ended for RR\n")

# Returns a string that is used to show the user the contents of the Q
def StringQ():
    if len(Q) > 0:
        q = []
        for process in Q:
            proc_id = process['process_id']
            q.append(proc_id)
        return " ".join(map(str,q))
    else:
        return "empty"
        
def ParseInput():
    global lines
    global data
    
    del data[:]
    
    for line in lines:
        if line[0] != '#':
            proc_id, initial_arrival_time, cpu_burst_time, num_bursts, io_time = line.split("|")
            process = {
                'process_id': proc_id,
                'initial_arrival_time': int(initial_arrival_time),
                'cpu_burst_time': int(cpu_burst_time),
                'cpu_burst_time_left': int(cpu_burst_time)+1,
                'cpu_burst_time_end': int(cpu_burst_time)+int(initial_arrival_time),
                'time_slice_end': int(initial_arrival_time)+t_slice,
                'num_bursts': int(num_bursts),
                'num_bursts_left': int(num_bursts),
                'io_time': int(io_time),
                'io_time_end': int(io_time)+int(cpu_burst_time)+int(initial_arrival_time),
                'wait_time': 0,
                'state': 'READY'
            }
            data.append(process)

# Parse input file for the line buy line read
from sys import argv
script, filename, outputfile = argv
try:
    text = open(filename)
except IOError:
    sys.stderr.write('ERROR: Invalid input file format\n')
with text as f:
    lines = f.readlines()

# Number of processors (cores)
m = 1
# Time it takes to make a context switch
t_cs = 8
# Time slice for RR algorithm
t_slice = 84

# Copy all of the line data into a dictionary of processes containing the values
data = []
ParseInput()

# Number of processes to simulate
n = len(data)

Q = []

# FCFS
ScheduleProcesses(True,False,False)
# SJF
data = []
Q = []
ParseInput()
ScheduleProcesses(False,True,False)
# RR
data = []
Q = []
ParseInput()
ScheduleProcesses(False,False,True)
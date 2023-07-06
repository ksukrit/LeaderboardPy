import os

def getTime(timeout="1m",input_args="8 0 0"):
    print( os.system(f"(/usr/bin/time -p timeout {timeout} ./a.out {input_args}) 2> stats.txt"))
    
    s = str()
    with open("stats.txt",'r') as cpu_time:
        s= cpu_time.read()

    s = s.replace("\n"," ")
    l = s.split()
    print(l)
    n = float (float (l[-3])+ float(l[-1]))
    return n
 



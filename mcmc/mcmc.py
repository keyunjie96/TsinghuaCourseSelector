import os
import thread as thread
import random

m = 16 
n = 128 

# Random choose k times


def random_walker(myid, k, n):
    for i in range(k):
        result = random.randint(0, n - 1)
        if appear_or_not[result] == False:
            appear_or_not[result] = True
    thread_exit_lock[myid] = True


for j in range(m, m**2, m):
    pipein,pipeout=os.pipe()
    newid=os.fork()
    if newid==0:
        appear_res_list = list()
        # Running 1000 times for each choose times from 8 to 8*m**2
        for k in range(1000):
            thread_exit_lock = [False] * 16 
            appear_or_not = [False] * n
            for i in range(16):
                thread.start_new_thread(random_walker, (i, j/16, n))
            while False in thread_exit_lock:
                continue
            if (k + 1) % 200 == 0:
                print("Running " + str(k + 1) + "times")
            appear_res_list.append(appear_or_not.count(True))
        output = open(str(j) + ".txt", "w")
        for each in appear_res_list:
            output.write("%3d \n" % each)
        output.close()
        print("Finished for " + str(j) + "\n")
        os.write(pipeout, "0".encode("UTF-8"))
        os._exit(0)
    else:
        ret=os.read(pipein, 32)

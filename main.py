from collections import deque

class CPU:
    def __init__(self, cpu, next_=None):
        self.cpu_time = cpu
        self.next_ = next_


class IO:
    def __init__(self, io, next_=None):
        self.io_time = io
        self.next_ = next_


class Thread:
    def __init__(self):
        self.thread_head = None
        self.thread_tail = None


class Process:
    # Global fields for all processes
    Execution_Flag = False
    Processing_Flag = True
    Execution_time = 0
    CPUutilization = 0
    process_head = None
    process_tail = None

    FcfsAvgCpu = SjfAvgCpu = MlfqAvgCpu = 0
    FcfsAvgTw = SjfAvgTw  = MlfqAvgTw  = 0
    FcfsAvgTtr = SjfAvgTtr  = MlfqAvgTtr  = 0
    FcfsAvgTr = SjfAvgTr  = MlfqAvgTr  = 0
    FcfsTime = SjfTime = MlfqTime = 0

    #  Fields for FCFS
    readyQueue = deque()
    waitingQueue = []
    finishQueue = []
    processing = []

    #  Fields for SJF
    cpuMin = float('inf')
    priorityQueue = deque()

    #  Fields for MFQL
    processingList1 = []  # only one process runs at a time
    processingList2 = []  # only one process runs at a time
    processingList3 = []  # only one process runs at a time
    inWaitingQueue = []  # for processes who are in i/o
    roundRobin1Queue = deque()  # can have multiple processes inside
    roundRobin2Queue = deque()  # can have multiple processes inside
    fcfsQueue = deque()  # can have multiple processes inside

    def __int__(self, Tw=0, Ttr=0, Tr=-1, next_=None, name=''):
        self.pname = ''
        self.cpu_List = []
        self.io_List = []
        self.next_ = next_
        self.Tw = 0
        self.Ttr = 0
        self.Tr = -1
        self.pnum = 1

#  Preconditions
    @staticmethod
    def isReadyQueue():
        return len(Process.readyQueue) == 0

    @staticmethod
    def isPriorityQueue():
        return len(Process.priorityQueue) == 0

    @staticmethod
    def isWaitingQueue():
        return len(Process.waitingQueue) == 0

    @staticmethod
    def isProcessing():
        return len(Process.processing) == 0


    @staticmethod
    def isFinishQueue():
        return len(Process.finishQueue) == 0


#  GETTERS
    @staticmethod
    def getSnapshot(e):
        if e == Process.Execution_time:
            print('------------------------------------------> Snapshot time : ' + str(Process.Execution_time) + 'ms')

            #  Get status on processes in Execution
            if not Process.isProcessing():
                print('-----------------------------------')
                tempPtr3 = Process.processing[0]
                print(tempPtr3.pname + ' in execution (CPU).')
                print('-----------------------------------')
                print('Tw = ' + str(tempPtr3.Tw))
                print('Ttr = ' + str(tempPtr3.Ttr))
                print('Tr = ' + str(tempPtr3.Tr))

                tempCpuPtr3 = tempPtr3.cpu_List.thread_head
                print('Cpu burst list remaining [ ', end='')
                while tempCpuPtr3 is not None:
                    print(str(tempCpuPtr3.cpu_time), end='')
                    tempCpuPtr3 = tempCpuPtr3.next_
                    if tempCpuPtr3 is not None:
                        print(', ', end='')
                print(' ]')

                tempIoPtr3 = tempPtr3.io_List.thread_head
                print('I/O burst list remaining [ ', end='')
                while tempIoPtr3 is not None:
                    print(str(tempIoPtr3.io_time), end=' ')
                    tempIoPtr3 = tempIoPtr3.next_
                    if tempIoPtr3 is not None:
                        print(', ', end='')
                print(']', '\n')

            #  Get status on which processes are in READY QUEUE at this snapshot time from the user
            if not Process.isReadyQueue():
                tempPtr = Process.readyQueue
                for pr in range(len(tempPtr)):
                    print('-----------------------------------')
                    print(tempPtr[pr].pname + ' in Ready Queue (Tw).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr[pr].Tw))
                    print('Ttr = ' + str(tempPtr[pr].Ttr))
                    print('Tr = ' + str(tempPtr[pr].Tr))

                    tempCpuPtr = tempPtr[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr is not None:
                        print(str(tempCpuPtr.cpu_time), end='')
                        tempCpuPtr = tempCpuPtr.next_
                        if tempCpuPtr is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr = tempPtr[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr is not None:
                        print(str(tempIoPtr.io_time), end=' ')
                        tempIoPtr = tempIoPtr.next_
                        if tempIoPtr is not None:
                            print(', ', end='')
                    print(']', '\n')

            #  Get status on which processes are in WAITING QUEUE at this snapshot time from the user
            if not Process.isWaitingQueue():
                tempPtr1 = Process.waitingQueue  # change this
                for pr in range(len(tempPtr1)):
                    print('-----------------------------------')
                    print(tempPtr1[pr].pname + ' in Waiting Queue (I/0).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr1[pr].Tw))
                    print('Ttr = ' + str(tempPtr1[pr].Ttr))
                    print('Tr = ' + str(tempPtr1[pr].Tr))

                    tempCpuPtr1 = tempPtr1[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr1 is not None:
                        print(str(tempCpuPtr1.cpu_time), end='')
                        tempCpuPtr1 = tempCpuPtr1.next_
                        if tempCpuPtr1 is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr1 = tempPtr1[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr1 is not None:
                        print(str(tempIoPtr1.io_time), end=' ')
                        tempIoPtr1 = tempIoPtr1.next_
                        if tempIoPtr1 is not None:
                            print(', ', end='')
                    print(']', '\n')

            #  Get status on which processes are TERMINATED at this snapshot time from the user
            if not Process.isFinishQueue():
                tempPtr2 = Process.finishQueue
                for pr in range(len(Process.finishQueue)):
                    print('-----------------------------------')
                    print(tempPtr2[pr].pname + ' terminated at ' + str(Process.Execution_time) + "/" + '643ms')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr2[pr].Tw))
                    print('Ttr = ' + str(tempPtr2[pr].Tr))
                    print('Tr = ' + str(tempPtr2[pr].Tr))

    @staticmethod
    def getSnapshot1(e):
        if e == Process.Execution_time:
            print('------------------------------------------> Snapshot time : ' + str(Process.Execution_time) + 'ms')

            #  Get status on processes in Execution
            if not Process.isProcessing():
                tempPtr3 = Process.processing[0]
                print('-----------------------------------')
                print(tempPtr3.pname + ' in execution (CPU).')
                print('-----------------------------------')
                print('Tw = ' + str(tempPtr3.Tw))
                print('Ttr = ' + str(tempPtr3.Ttr))
                print('Tr = ' + str(tempPtr3.Tr))

                tempCpuPtr3 = tempPtr3.cpu_List.thread_head
                print('Cpu burst list remaining [ ', end='')
                while tempCpuPtr3 is not None:
                    print(str(tempCpuPtr3.cpu_time), end='')
                    tempCpuPtr3 = tempCpuPtr3.next_
                    if tempCpuPtr3 is not None:
                        print(', ', end='')
                print(' ]')

                tempIoPtr3 = tempPtr3.io_List.thread_head
                print('I/O burst list remaining [ ', end='')
                while tempIoPtr3 is not None:
                    print(str(tempIoPtr3.io_time), end=' ')
                    tempIoPtr3 = tempIoPtr3.next_
                    if tempIoPtr3 is not None:
                        print(', ', end='')
                print(']', '\n')

            #  Get status on which processes are in READY QUEUE at this snapshot time from the user
            if not Process.isPriorityQueue():
                tempPtr = Process.priorityQueue
                for pr in range(len(tempPtr)):
                    print('-----------------------------------')
                    print(tempPtr[pr].pname + ' in Ready Queue (Tw).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr[pr].Tw))
                    print('Ttr = ' + str(tempPtr[pr].Ttr))
                    print('Tr = ' + str(tempPtr[pr].Tr))

                    tempCpuPtr = tempPtr[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr is not None:
                        print(str(tempCpuPtr.cpu_time), end='')
                        tempCpuPtr = tempCpuPtr.next_
                        if tempCpuPtr is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr = tempPtr[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr is not None:
                        print(str(tempIoPtr.io_time), end=' ')
                        tempIoPtr = tempIoPtr.next_
                        if tempIoPtr is not None:
                            print(', ', end='')
                    print(']', '\n')

            #  Get status on which processes are in WAITING QUEUE at this snapshot time from the user
            if not Process.isWaitingQueue():
                tempPtr1 = Process.waitingQueue  # change this
                for pr in range(len(tempPtr1)):
                    print('-----------------------------------')
                    print(tempPtr1[pr].pname + ' in Waiting Queue (I/O).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr1[pr].Tw))
                    print('Ttr = ' + str(tempPtr1[pr].Ttr))
                    print('Tr = ' + str(tempPtr1[pr].Tr))

                    tempCpuPtr1 = tempPtr1[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr1 is not None:
                        print(str(tempCpuPtr1.cpu_time), end='')
                        tempCpuPtr1 = tempCpuPtr1.next_
                        if tempCpuPtr1 is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr1 = tempPtr1[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr1 is not None:
                        print(str(tempIoPtr1.io_time), end=' ')
                        tempIoPtr1 = tempIoPtr1.next_
                        if tempIoPtr1 is not None:
                            print(', ', end='')
                    print(']', '\n')

            #  Get status on which processes are TERMINATED at this snapshot time from the user
            if not Process.isFinishQueue():
                tempPtr2 = Process.finishQueue
                for pr in range(len(Process.finishQueue)):
                    print('-----------------------------------')
                    print(tempPtr2[pr].pname + ' terminated at ' + str(Process.Execution_time) + "/643ms (Ttr)")
                    print('-----------------------------------')
                    print(tempPtr2[pr].pname + ' : Tw = ' + str(tempPtr2[pr].Tw))
                    print(tempPtr2[pr].pname + ' : Ttr = ' + str(tempPtr2[pr].Tr))
                    print(tempPtr2[pr].pname + ' : Tr = ' + str(tempPtr2[pr].Tr), '\n')

    @staticmethod
    def getSnapshot2(e):
        if e == Process.Execution_time:
            print('------------------------------------------> Snapshot time : ' + str(Process.Execution_time) + 'ms')

            #  Get status on processes in Execution
            if Process.processingList1:
                tempPtr3 = Process.processingList1[0]
                print('-----------------------------------')
                print(tempPtr3.pname + ' in roundRobin1 execution (CPU).')
                print('-----------------------------------')
                print('Tw = ' + str(tempPtr3.Tw))
                print('Ttr = ' + str(tempPtr3.Ttr))
                print('Tr = ' + str(tempPtr3.Tr))
                tempCpuPtr3 = tempPtr3.cpu_List.thread_head
                print('Cpu burst list remaining [ ', end='')
                while tempCpuPtr3 is not None:
                    print(str(tempCpuPtr3.cpu_time), end='')
                    tempCpuPtr3 = tempCpuPtr3.next_
                    if tempCpuPtr3 is not None:
                        print(', ', end='')
                print(' ]')

                tempIoPtr3 = tempPtr3.io_List.thread_head
                print('I/O burst list remaining [ ', end='')
                while tempIoPtr3 is not None:
                    print(str(tempIoPtr3.io_time), end=' ')
                    tempIoPtr3 = tempIoPtr3.next_
                    if tempIoPtr3 is not None:
                        print(', ', end='')
                print(']', '\n')

            if Process.processingList2:
                tempPtr3 = Process.processingList2[0]
                print('-----------------------------------')
                print(tempPtr3.pname + ' in roundRobin2 Queue execution (CPU).')
                print('-----------------------------------')
                print('Tw = ' + str(tempPtr3.Tw))
                print('Ttr = ' + str(tempPtr3.Ttr))
                print('Tr = ' + str(tempPtr3.Tr))

                tempCpuPtr3 = tempPtr3.cpu_List.thread_head
                print('Cpu burst list remaining [ ', end='')
                while tempCpuPtr3 is not None:
                    print(str(tempCpuPtr3.cpu_time), end='')
                    tempCpuPtr3 = tempCpuPtr3.next_
                    if tempCpuPtr3 is not None:
                        print(', ', end='')
                print(' ]')

                tempIoPtr3 = tempPtr3.io_List.thread_head
                print('I/O burst list remaining [ ', end='')
                while tempIoPtr3 is not None:
                    print(str(tempIoPtr3.io_time), end=' ')
                    tempIoPtr3 = tempIoPtr3.next_
                    if tempIoPtr3 is not None:
                        print(', ', end='')
                print(']', '\n')

            if Process.processingList3:
                tempPtr3 = Process.processingList3[0]
                print('-----------------------------------')
                print(tempPtr3.pname + ' in FCFS Queue execution (CPU).')
                print('-----------------------------------')
                print('Tw = ' + str(tempPtr3.Tw))
                print('Ttr = ' + str(tempPtr3.Ttr))
                print('Tr = ' + str(tempPtr3.Tr))

                tempCpuPtr3 = tempPtr3.cpu_List.thread_head
                print('Cpu burst list remaining [ ', end='')
                while tempCpuPtr3 is not None:
                    print(str(tempCpuPtr3.cpu_time), end='')
                    tempCpuPtr3 = tempCpuPtr3.next_
                    if tempCpuPtr3 is not None:
                        print(', ', end='')
                print(' ]')

                tempIoPtr3 = tempPtr3.io_List.thread_head
                print('I/O burst list remaining [ ', end='')
                while tempIoPtr3 is not None:
                    print(str(tempIoPtr3.io_time), end=' ')
                    tempIoPtr3 = tempIoPtr3.next_
                    if tempIoPtr3 is not None:
                        print(', ', end='')
                print(']', '\n')

            #  Get status on which processes are in READY QUEUES at this snapshot time from the user
            if Process.roundRobin1Queue:
                tempPtr = Process.roundRobin1Queue
                for pr in range(len(tempPtr)):
                    print('-----------------------------------')
                    print(tempPtr[pr].pname + ' in roundRobin1 Queue (Tw).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr[pr].Tw))
                    print('Ttr = ' + str(tempPtr[pr].Ttr))
                    print('Tr = ' + str(tempPtr[pr].Tr))

                    tempCpuPtr = tempPtr[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr is not None:
                        print(str(tempCpuPtr.cpu_time), end='')
                        tempCpuPtr = tempCpuPtr.next_
                        if tempCpuPtr is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr = tempPtr[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr is not None:
                        print(str(tempIoPtr.io_time), end=' ')
                        tempIoPtr = tempIoPtr.next_
                        if tempIoPtr is not None:
                            print(', ', end='')
                    print(']', '\n')

            if Process.roundRobin2Queue:
                tempPtr = Process.roundRobin2Queue
                for pr in range(len(tempPtr)):
                    print('-----------------------------------')
                    print(tempPtr[pr].pname + ' in roundRobin2 Queue (Tw).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr[pr].Tw))
                    print('Ttr = ' + str(tempPtr[pr].Ttr))
                    print('Tr = ' + str(tempPtr[pr].Tr))

                    tempCpuPtr = tempPtr[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr is not None:
                        print(str(tempCpuPtr.cpu_time), end='')
                        tempCpuPtr = tempCpuPtr.next_
                        if tempCpuPtr is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr = tempPtr[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr is not None:
                        print(str(tempIoPtr.io_time), end=' ')
                        tempIoPtr = tempIoPtr.next_
                        if tempIoPtr is not None:
                            print(', ', end='')
                    print(']', '\n')

            if Process.fcfsQueue:
                tempPtr = Process.fcfsQueue
                for pr in range(len(tempPtr)):
                    print('-----------------------------------')
                    print(tempPtr[pr].pname + ' in FCFS Queue (Tw).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr[pr].Tw))
                    print('Ttr = ' + str(tempPtr[pr].Ttr))
                    print('Tr = ' + str(tempPtr[pr].Tr))

                    tempCpuPtr = tempPtr[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr is not None:
                        print(str(tempCpuPtr.cpu_time), end='')
                        tempCpuPtr = tempCpuPtr.next_
                        if tempCpuPtr is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr = tempPtr[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr is not None:
                        print(str(tempIoPtr.io_time), end=' ')
                        tempIoPtr = tempIoPtr.next_
                        if tempIoPtr is not None:
                            print(', ', end='')
                    print(']', '\n')

            #  Get status on which processes are in WAITING QUEUE at this snapshot time from the user
            if Process.inWaitingQueue:
                tempPtr1 = Process.inWaitingQueue  # change this
                for pr in range(len(tempPtr1)):
                    print('-----------------------------------')
                    print(tempPtr1[pr].pname + ' in Waiting Queue (I/O).')
                    print('-----------------------------------')
                    print('Tw = ' + str(tempPtr1[pr].Tw))
                    print('Ttr = ' + str(tempPtr1[pr].Ttr))
                    print('Tr = ' + str(tempPtr1[pr].Tr))

                    tempCpuPtr1 = tempPtr1[pr].cpu_List.thread_head
                    print('Cpu burst list remaining [ ', end='')
                    while tempCpuPtr1 is not None:
                        print(str(tempCpuPtr1.cpu_time), end='')
                        tempCpuPtr1 = tempCpuPtr1.next_
                        if tempCpuPtr1 is not None:
                            print(', ', end='')
                    print(' ]')

                    tempIoPtr1 = tempPtr1[pr].io_List.thread_head
                    print('I/O burst list remaining [ ', end='')
                    while tempIoPtr1 is not None:
                        print(str(tempIoPtr1.io_time), end=' ')
                        tempIoPtr1 = tempIoPtr1.next_
                        if tempIoPtr1 is not None:
                            print(', ', end='')
                    print(']', '\n')

            #  Get status on which processes are TERMINATED at this snapshot time from the user
            if Process.finishQueue:
                tempPtr2 = Process.finishQueue
                for pr in range(len(Process.finishQueue)):
                    print('-----------------------------------')
                    print(tempPtr2[pr].pname + ' terminated at ' + str(Process.Execution_time) + "/630ms (Ttr)")
                    print('-----------------------------------')
                    print(tempPtr2[pr].pname + ' : Tw = ' + str(tempPtr2[pr].Tw))
                    print(tempPtr2[pr].pname + ' : Ttr = ' + str(tempPtr2[pr].Ttr))
                    print(tempPtr2[pr].pname + ' : Tr = ' + str(tempPtr2[pr].Tr), '\n')

#  RESULTS
    @staticmethod
    def getResults1():
        print('------------------------------------------------')
        print('Process #    |     Tw     |    Ttr   |    Tr   ')

        tempPtr3 = Process.finishQueue
        for pr in range(len(Process.finishQueue)):
            # print(tempPtr3[pr].pname + ' terminated at ' + str(tempPtr3[pr].Ttr) + 'ms/' + str(
            #     Process.Execution_time) + "ms")
            print('------------------------------------------------')
            print(tempPtr3[pr].pname + '    |     ' + str(tempPtr3[pr].Tw) + '    |   ' + str(tempPtr3[pr].Ttr) + '    |   ' + str(tempPtr3[pr].Tr))
            Process.FcfsAvgTw += tempPtr3[pr].Tw
            Process.FcfsAvgTtr += tempPtr3[pr].Ttr
            Process.FcfsAvgTr += tempPtr3[pr].Tr

        Process.FcfsAvgCpu = round(Process.CPUutilization / Process.Execution_time * 100, 2)
        Process.FcfsTime = str(Process.Execution_time)

        print('------------------------------------------------')
        print('Average      |    ' + str(round(Process.FcfsAvgTw / len(Process.finishQueue), 2)) + '   |  ' + str(round(Process.FcfsAvgTtr / len(Process.finishQueue), 2)) +
              '  |  ' + str(round(Process.FcfsAvgTr / len(Process.finishQueue), 2)))
        print('------------------------------------------------')
        print('CPU Utilization: ', str(round(Process.CPUutilization / Process.Execution_time * 100, 2)) + '%')
        print('Total time: ' + str(Process.Execution_time) + 'ms', '\n')

        Process.FcfsAvgTw = str(round(Process.FcfsAvgTw / len(Process.finishQueue), 2))
        Process.FcfsAvgTtr = str(round(Process.FcfsAvgTtr / len(Process.finishQueue), 2))
        Process.FcfsAvgTr = str(round(Process.FcfsAvgTr / len(Process.finishQueue), 2))

    @staticmethod
    def getResults2():
        print('------------------------------------------------')
        print('Process #    |     Tw     |    Ttr   |    Tr   ')

        tempPtr3 = Process.finishQueue
        for pr in range(len(Process.finishQueue)):
            print('------------------------------------------------')
            print(tempPtr3[pr].pname + '    |     ' + str(tempPtr3[pr].Tw) + '    |   ' + str(tempPtr3[pr].Ttr) + '    |   ' + str(tempPtr3[pr].Tr))
            Process.SjfAvgTw += tempPtr3[pr].Tw
            Process.SjfAvgTtr += tempPtr3[pr].Ttr
            Process.SjfAvgTr += tempPtr3[pr].Tr

        Process.SjfAvgCpu = round(Process.CPUutilization / Process.Execution_time * 100, 2)
        Process.SjfTime = str(Process.Execution_time)

        print('------------------------------------------------')
        print('Average      |    ' + str(round(Process.SjfAvgTw / len(Process.finishQueue), 2)) + '   |  ' + str(round(Process.SjfAvgTtr / len(Process.finishQueue), 2)) +
              '  |  ' + str(round(Process.SjfAvgTr / len(Process.finishQueue), 2)))
        print('------------------------------------------------')
        print('CPU Utilization: ', str(round(Process.CPUutilization / Process.Execution_time * 100, 2)) + '%')
        print('Total time: ' + str(Process.Execution_time) + 'ms', '\n')

        Process.SjfAvgTw = str(round(Process.SjfAvgTw / len(Process.finishQueue), 2))
        Process.SjfAvgTtr = str(round(Process.SjfAvgTtr / len(Process.finishQueue), 2))
        Process.SjfAvgTr = str(round(Process.SjfAvgTr / len(Process.finishQueue), 2))

    @staticmethod
    def getResults3():
        print('------------------------------------------------')
        print('Process #    |     Tw     |    Ttr   |    Tr   ')

        tempPtr3 = Process.finishQueue
        for pr in range(len(Process.finishQueue)):
            # print(tempPtr3[pr].pname + ' terminated at ' + str(tempPtr3[pr].Ttr) + 'ms/' + str(
            #     Process.Execution_time) + "ms")
            print('------------------------------------------------')
            print(tempPtr3[pr].pname + '    |     ' + str(tempPtr3[pr].Tw) + '    |   ' + str(tempPtr3[pr].Ttr) + '    |   ' + str(tempPtr3[pr].Tr))
            Process.MlfqAvgTw += tempPtr3[pr].Tw
            Process.MlfqAvgTtr += tempPtr3[pr].Ttr
            Process.MlfqAvgTr += tempPtr3[pr].Tr

        Process.MlfqAvgCpu = round(Process.CPUutilization / Process.Execution_time * 100, 2)
        Process.MlfqTime = str(Process.Execution_time)

        print('------------------------------------------------')
        print('Average      |    ' + str(round(Process.MlfqAvgTw / len(Process.finishQueue), 2)) + '   |  ' + str(round(Process.MlfqAvgTtr / len(Process.finishQueue), 2)) +
              '  |  ' + str(round(Process.MlfqAvgTr / len(Process.finishQueue), 2)))
        print('------------------------------------------------')
        print('CPU Utilization: ', str(round(Process.CPUutilization / Process.Execution_time * 100, 2)) + '%')
        print('Total time: ' + str(Process.Execution_time) + 'ms', '\n')

        Process.MlfqAvgTw = str(round(Process.MlfqAvgTw / len(Process.finishQueue), 2))
        Process.MlfqAvgTtr = str(round(Process.MlfqAvgTtr / len(Process.finishQueue), 2))
        Process.MlfqAvgTr = str(round(Process.MlfqAvgTr / len(Process.finishQueue), 2))

#  FINAL RESULTS
    @staticmethod
    def compare():
        print('--------------------------------> Results Comparison <-----------------------------------------', '\n')
        print('---------------------------------------------------------------------')
        print('| CPU SCHEDULING ALGORITHMS   |      SJF     |    FCFS   |    MLFQ   |')

        print('----------------------------------------------------------------------')
        print('| CPU utilization (%)         |     ' + str(Process.SjfAvgCpu) + '    |    ' + str(Process.FcfsAvgCpu) + '   |   ' + str(Process.MlfqAvgCpu) + '   |')
        print('----------------------------------------------------------------------')
        print('| Avg Waiting time (Tw)       |     ' + str(Process.SjfAvgTw) + '   |   ' + str(Process.FcfsAvgTw) + '   |   ' + str(Process.MlfqAvgTw) + '  |')
        print('----------------------------------------------------------------------')
        print('| Avg Turnaround time (Ttr)   |     ' + str(Process.SjfAvgTtr) + '   |   ' + str(Process.FcfsAvgTtr) + '  |   ' + str(Process.MlfqAvgTtr) + '   |')
        print('----------------------------------------------------------------------')
        print('| Avg Response time (Tr)      |     ' + str(Process.SjfAvgTr) + '    |   ' + str(Process.FcfsAvgTr) + '   |   ' + str(Process.MlfqAvgTr) + '   |')
        print('----------------------------------------------------------------------')
        print('| Total time (ms)             |      ' + str(Process.FcfsTime) + '     |    ' + str(Process.SjfTime)  + '    |    ' + str(Process.MlfqTime) + '    |')
        print('----------------------------------------------------------------------')

#  Increment Tw
    @staticmethod
    def waitingReady():
        if not Process.isReadyQueue():
            readyPtr = Process.readyQueue
            for e in range(len(readyPtr)):
                readyPtr[e].Tw += 1

    @staticmethod
    def waitingReady1():
        if not Process.isPriorityQueue():
            readyPtr = Process.priorityQueue
            for e in range(len(readyPtr)):
                readyPtr[e].Tw += 1

#  Decrement I/O
    @staticmethod
    def runningIO(e):
        #  Decrement each process that is in waitingQueue for I/O execution
        if not Process.isWaitingQueue():
            for pr in Process.waitingQueue:
                # Decrement i/o each process in waitingQueue
                pr.io_List.thread_head.io_time -= 1
                if pr.io_List.thread_head.io_time == 0:
                    #  Point to next I/O in thread
                    if pr.io_List.thread_head.next_ is not None:
                        pr.io_List.thread_head = pr.io_List.thread_head.next_
                    # Add Process back to ready list since its i/o went to 0
                    Process.readyQueue.append(pr)
                    Process.Execution_Flag = True

            for copy in Process.readyQueue:
                if copy in Process.waitingQueue:
                    Process.waitingQueue.remove(copy)

            if not Process.Execution_Flag and Process.isProcessing():
                Process.Execution_time += 1
                Process.getSnapshot(e)

        if Process.isProcessing() and not Process.isReadyQueue():
            Process.processing.append(Process.readyQueue.popleft())
            Process.execution(e)

    @staticmethod
    def runningIO1(e):
        #  Decrement each process that is in waitingQueue for I/O execution
        if not Process.isWaitingQueue():
            for pr in Process.waitingQueue:
                # Give Process its Tr if first time being executed.
                pr.io_List.thread_head.io_time -= 1
                if pr.io_List.thread_head.io_time == 0:
                    #  Point to next I/O in thread
                    if pr.io_List.thread_head.next_ is not None:
                        pr.io_List.thread_head = pr.io_List.thread_head.next_
                    # Add Process back to ready list since its i/o went to 0
                    Process.priorityQueue.append(pr)
                    Process.Execution_Flag = True

            for copy in Process.priorityQueue:
                if copy in Process.waitingQueue:
                    Process.waitingQueue.remove(copy)

            if not Process.Execution_Flag and Process.isProcessing():
                Process.Execution_time += 1
                Process.getSnapshot1(e)

        if Process.isProcessing() and not Process.isPriorityQueue():
            Process.sortPriorityQueue()
            Process.processing.append(Process.priorityQueue.popleft())
            Process.execution1(e)

#  CPU Execution
    @staticmethod
    def execution(e):
        while not Process.isProcessing():
            for p in Process.processing:
                Process.Execution_Flag = True

                if p.Tr == -1:
                    p.Tr = Process.Execution_time

                if p.cpu_List.thread_head.cpu_time == 0:
                    Process.Processing_Flag = True
                    #  Create function to check if this is last cpu in the process AKA FINISHED cpu e
                    if p.cpu_List.thread_head.next_ is None:
                        # Create a List of this process credentials in some sort detail list called finished Queue
                        p.Ttr = Process.Execution_time
                        #  Remove Process runs its cpu thread is NULL
                        Process.finishQueue.append(Process.processing.pop())
                    else:
                        # Move cpu thread pointer to next cpu_list -> cpu_time in this process
                        p.cpu_List.thread_head = p.cpu_List.thread_head.next_
                        #  Put process back in ready queue
                        Process.waitingQueue.append(Process.processing.pop())
                        # Point to next process to be run: example p1 cpu finishes -> run p2 cpu
                        if not Process.isReadyQueue():
                            Process.process_head = Process.readyQueue[0]
                            Process.processing.append(Process.readyQueue.popleft())
                            Process.execution(e)  # <------------------------------------------------------------
                        else:
                            Process.Execution_Flag = False
                else:
                    # -------------------------------------TIME--------------------------------------------------------
                    # Create a function that increments processes Tw that's not currently running that's in ready list
                    if not Process.isWaitingQueue() and not Process.isReadyQueue():
                        Process.waitingReady()
                        Process.runningIO(e)
                    # Create a function that decrements processes i/o that are in waiting list
                    elif not Process.isWaitingQueue():
                        Process.runningIO(e)
                    else:
                        Process.waitingReady()

                    p.cpu_List.thread_head.cpu_time -= 1
                    Process.Execution_time += 1
                    Process.getSnapshot(e)
        Process.Execution_Flag = False

    @staticmethod
    def execution1(e):
        while not Process.isProcessing():
            for p in Process.processing:
                Process.Execution_Flag = True

                if p.Tr == -1:
                    p.Tr = Process.Execution_time

                if p.cpu_List.thread_head.cpu_time == 0:
                    Process.Processing_Flag = True
                    #  Create function to check if this is last cpu in the process AKA FINISHED cpu e
                    if p.cpu_List.thread_head.next_ is None:
                        # Create a List of this process credentials in some sort detail list called finished Queue
                        p.Ttr = Process.Execution_time
                        #  Remove Process runs its cpu thread is NULL
                        Process.finishQueue.append(Process.processing.pop())
                    else:
                        # Move cpu thread pointer to next cpu_list -> cpu_time in this process
                        p.cpu_List.thread_head = p.cpu_List.thread_head.next_
                        #  Put process back in ready queue
                        Process.waitingQueue.append(Process.processing.pop())
                        # Point to next process to be run: example p1 cpu finishes -> run p2 cpu
                        if not Process.isPriorityQueue():
                            Process.sortPriorityQueue()
                            Process.process_head = Process.priorityQueue[0]
                            Process.processing.append(Process.priorityQueue.popleft())
                            Process.execution1(e)  # <------------------------------------------------------------
                        else:
                            Process.Execution_Flag = False
                else:
                    # -------------------------------------TIME--------------------------------------------------------
                    # Create a function that increments processes Tw that's not currently running that's in ready list
                    if not Process.isWaitingQueue() and not Process.isPriorityQueue():
                        Process.waitingReady1()
                        Process.runningIO1(e)
                    # Create a function that decrements processes i/o that are in waiting list
                    elif not Process.isWaitingQueue():
                        Process.runningIO1(e)
                    else:
                        Process.waitingReady1()

                    p.cpu_List.thread_head.cpu_time -= 1
                    Process.Execution_time += 1
                    Process.getSnapshot1(e)
        Process.Execution_Flag = False

    @staticmethod
    def sortPriorityQueue():
        if len(Process.priorityQueue) > 1:
            foundMin = 0
            for i in range(len(Process.priorityQueue)):
                if Process.cpuMin > Process.process_head.priorityQueue[i].cpu_List.thread_head.cpu_time:
                    Process.cpuMin = min(Process.cpuMin,
                                         Process.process_head.priorityQueue[i].cpu_List.thread_head.cpu_time)
                    foundMin = i

            Process.cpuMin = float('inf')

            #  SWAPPING INDEXES
            temp = Process.priorityQueue[foundMin]
            Process.priorityQueue.remove(temp)
            Process.priorityQueue.insert(0, temp)

#   FCFS FUNCTIONS
    @staticmethod
    def runFCFS():

        Process.processing.append(Process.readyQueue.popleft())
        Process.execution(e)

        while Process.readyQueue or Process.waitingQueue:
            Process.runningIO(e)

        if len(Process.readyQueue) == 0 and len(Process.waitingQueue) == 0 and len(Process.finishQueue) == 8 and len(
                Process.processing) == 0:
            print('\n'+"------------------------------> FCFS: FINAL RESULTS <----------------------------------")
            Process.getResults1()
        else:
            # debugging code
            print('error')
            print('Process.readyQueue', len(Process.readyQueue))
            print('Process.waitingQueue', len(Process.waitingQueue))
            print('Process.finishQueue', len(Process.finishQueue))
            print('Process.FCFS', len(Process.processing))

#  SJF FUNCTIONS
    @staticmethod
    def runSJF():
        Process.sortPriorityQueue()
        Process.processing.append(Process.priorityQueue.popleft())
        Process.execution1(e)

        while Process.priorityQueue or Process.waitingQueue:
            Process.runningIO1(e)

        if len(Process.priorityQueue) == 0 and len(Process.waitingQueue) == 0 and len(Process.finishQueue) == 8 and len(
                Process.processing) == 0:
            print('\n' + "------------------------------> SJF: FINAL RESULTS <----------------------------------")
            Process.getResults2()
        else:
            # debugging code
            print('error')
            print('Process.readyQueue', len(Process.priorityQueue))
            print('Process.waitingQueue', len(Process.waitingQueue))
            print('Process.finishQueue', len(Process.finishQueue))
            print('Process.FCFS', len(Process.processing))
        print('\n')

#  MLFQ FUNCTIONS
    @staticmethod
    def runMLFQ():
        while Process.roundRobin1Queue or Process.roundRobin2Queue or Process.fcfsQueue or Process.inWaitingQueue:
            # if roundRobin1Queue is not empty, then run processes from roundRobin1Queue until it's empty
            if Process.roundRobin1Queue:
                Process.processingList1.append(Process.roundRobin1Queue.popleft())
                Process.exe1(e)

            if Process.roundRobin2Queue and not Process.roundRobin1Queue:
                Process.processingList2.append(Process.roundRobin2Queue.popleft())
                Process.exe2(e)

            if Process.fcfsQueue and not Process.roundRobin1Queue and not Process.roundRobin2Queue:
                Process.processingList3.append(Process.fcfsQueue.popleft())
                Process.exe3(e)

            if not Process.fcfsQueue and not Process.roundRobin1Queue and not Process.roundRobin2Queue:
                Process.runIO(e)

        if len(Process.roundRobin1Queue) == 0 and len(Process.roundRobin2Queue) == 0 and len(
                Process.finishQueue) == 8 and len(Process.fcfsQueue) == 0:
            print('\n'+"------------------------------> MLFQ: FINAL RESULTS <----------------------------------")
            Process.getResults3()
        else:
            #debugging code
            print('error', '\n')
            print('Process.roundRobin1Queue', len(Process.roundRobin1Queue))
            print('Process.roundRobin2Queue', len(Process.roundRobin2Queue))
            print('Process.finishQueue', len(Process.finishQueue))
            print('Process.fcfsQueue', len(Process.fcfsQueue))
            print('Process.waiting', len(Process.inWaitingQueue))
            print('Process.processList1', len(Process.processingList1))
            print('Process.processingList2', len(Process.processingList2))
            print('Process.processingList3', len(Process.processingList3))

#  MFQL FUNCTIONS
    @staticmethod
    def runIO(e):
        #  Decrement each process that is in waitingQueue for I/O execution
        if Process.inWaitingQueue:
            for pr in Process.inWaitingQueue:
                pr.io_List.thread_head.io_time -= 1

                if pr.io_List.thread_head.io_time == 0:

                    if pr.io_List.thread_head.next_ is not None:
                        pr.io_List.thread_head = pr.io_List.thread_head.next_
                        Process.roundRobin1Queue.append(pr)
                        Process.Execution_Flag = True
                    else:
                        pr.io_List.thread_head = pr.io_List.thread_head.next_
                        Process.roundRobin1Queue.append(pr)

            for copy in Process.roundRobin1Queue:
                if copy in Process.inWaitingQueue:
                    Process.inWaitingQueue.remove(copy)

            #  if no processes in execution list then i/o will continue the cpu execution CLOCK
            if not Process.processingList1 and not Process.processingList2 and not Process.processingList3:
                Process.Execution_time += 1
                Process.getSnapshot2(e)

    @staticmethod
    def countTw():
        if Process.roundRobin1Queue:
            readyPtr = Process.roundRobin1Queue
            for e in range(len(readyPtr)):
                readyPtr[e].Tw += 1

        if Process.roundRobin2Queue:
            readyPtr1 = Process.roundRobin2Queue
            for e in range(len(readyPtr1)):
                readyPtr1[e].Tw += 1

        if Process.fcfsQueue:
            readyPtr2 = Process.fcfsQueue
            for e in range(len(readyPtr2)):
                readyPtr2[e].Tw += 1

    @staticmethod
    def exe1(e):
        if Process.processingList1:
            if Process.processingList1[0].Tr == -1:
                Process.processingList1[0].Tr = Process.Execution_time

        for i in range(5):
            #  if processingList1 execution is Empty break from loop
            if Process.processingList1:
                if Process.inWaitingQueue and Process.roundRobin1Queue:
                    Process.countTw()
                    Process.runIO(e)
                # Create a function that decrements processes i/o that are in waiting list
                elif Process.inWaitingQueue:
                    Process.runIO(e)
                else:
                    Process.countTw()

                Process.Execution_time += 1
                Process.processingList1[0].cpu_List.thread_head.cpu_time -= 1
                Process.getSnapshot2(e)

                if Process.processingList1[0].cpu_List.thread_head.cpu_time == 0:
                    if Process.processingList1[0].cpu_List.thread_head.next_ is None:
                        Process.processingList1[0].Ttr = Process.Execution_time
                        Process.finishQueue.append(Process.processingList1.pop())
                    else:
                        Process.processingList1[0].cpu_List.thread_head = Process.processingList1[
                            0].cpu_List.thread_head.next_
                        Process.inWaitingQueue.append(Process.processingList1.pop())

        if not Process.processingList1 and Process.roundRobin1Queue:
            Process.processingList1.append(Process.roundRobin1Queue.popleft())
            Process.exe1(e)
        elif Process.processingList1:
            if Process.processingList1[0].cpu_List.thread_head.cpu_time > 0:
                Process.roundRobin2Queue.append(Process.processingList1.pop())

    @staticmethod
    def exe2(e):
        for i in range(10):
            #  if processingList1 execution is Empty break from loop
            if Process.processingList2:
                if Process.inWaitingQueue and Process.roundRobin2Queue:
                    Process.countTw()
                    Process.runIO(e)
                # Create a function that decrements processes i/o that are in waiting list
                elif Process.inWaitingQueue:
                    Process.runIO(e)
                else:
                    Process.countTw()

                Process.Execution_time += 1
                Process.processingList2[0].cpu_List.thread_head.cpu_time -= 1
                Process.getSnapshot2(e)

                if Process.processingList2[0].cpu_List.thread_head.cpu_time == 0:
                    if Process.processingList2[0].cpu_List.thread_head.next_ is None:
                        Process.processingList2[0].Ttr = Process.Execution_time
                        Process.finishQueue.append(Process.processingList2.pop())
                    else:
                        Process.processingList2[0].cpu_List.thread_head = Process.processingList2[
                            0].cpu_List.thread_head.next_
                        Process.inWaitingQueue.append(Process.processingList2.pop())

        if not Process.processingList2 and Process.roundRobin1Queue and not Process.roundRobin2Queue:
            Process.processingList1.append(Process.roundRobin1Queue.popleft())
            Process.exe1(e)
        elif Process.processingList2:
            if Process.processingList2[0].cpu_List.thread_head.cpu_time > 0:
                Process.fcfsQueue.append(Process.processingList2.pop())

    @staticmethod
    def exe3(e):
        while Process.processingList3:
            #  if processingList1 execution is Empty break from loop
            if Process.inWaitingQueue and Process.fcfsQueue:
                Process.countTw()
                Process.runIO(e)
            # Create a function that decrements processes i/o that are in waiting list
            elif Process.inWaitingQueue:
                Process.runIO(e)
            else:
                Process.countTw()

            Process.Execution_time += 1
            Process.processingList3[0].cpu_List.thread_head.cpu_time -= 1
            Process.getSnapshot2(e)

            if Process.processingList3[0].cpu_List.thread_head.cpu_time == 0:
                if Process.processingList3[0].cpu_List.thread_head.next_ is None:
                    Process.processingList3[0].Ttr = Process.Execution_time
                    Process.finishQueue.append(Process.processingList3.pop())
                else:
                    Process.processingList3[0].cpu_List.thread_head = Process.processingList3[
                        0].cpu_List.thread_head.next_
                    Process.inWaitingQueue.append(Process.processingList3.pop())


if __name__ == "__main__":
    pList = []
    p1 = [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4]
    p2 = [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8]
    p3 = [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6]
    p4 = [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3]
    p5 = [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4]
    p6 = [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8]
    p7 = [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10]
    p8 = [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]

    pList.append(p1), pList.append(p2), pList.append(p3), pList.append(p4)
    pList.append(p5), pList.append(p6), pList.append(p7), pList.append(p8)

    cpuList = []
    ioList = []

    nodeList1 = []
    nodeList2 = []

    #  For each process separate the cpu and io burst.
    for i in pList:
        for j in range(1, len(i) + 1):
            if j % 2 == 0:
                ioList.append(i[j - 1])
            else:
                cpuList.append(i[j - 1])

        #  Calculating all cpu burst from each process.
        Process.CPUutilization += sum(cpuList)

        nodeList1.append(cpuList)
        nodeList2.append(ioList)
        cpuList = []
        ioList = []

    objList1 = []
    k = 0
    for node in nodeList1:
        cpuNodes = Thread()
        for c in node:
            if k == 0:
                cpuNodes.thread_head = CPU(c)
                cpuNodes.thread_tail = cpuNodes.thread_head
                k += 1
                continue
            cpuNodes.thread_tail.next_ = CPU(c)
            cpuNodes.thread_tail = cpuNodes.thread_tail.next_
            k += 1
        k = 0
        objList1.append(cpuNodes)

    objList2 = []
    for node in nodeList2:
        ioNodes = Thread()
        for i in node:
            if k == 0:
                ioNodes.thread_head = IO(i)
                ioNodes.thread_tail = ioNodes.thread_head
                k += 1
                continue
            ioNodes.thread_tail.next_ = IO(i)
            ioNodes.thread_tail = ioNodes.thread_tail.next_
            k += 1
        k = 0
        objList2.append(ioNodes)

    for i in range(8):

        p = Process()
        p.cpu_List = objList1[i]
        p.io_List = objList2[i]
        p.Tr = -1
        p.Tw = 0
        p.Ttr = 0
        p.pname = 'Process ' + str(i + 1)
        p.cont = True

        if k == 0:
            Process.process_head = p
            Process.process_tail = p
            Process.readyQueue.append(p)
            k += 1
            continue
        else:
            Process.process_tail.next_ = p
            Process.process_tail = p
            k += 1
        Process.readyQueue.append(p)

    """
    HOW TO ACCESS A PROCESS IN READY QUEUE
    """
    # print(Process.process_head.readyQueue[0].Tr)

    """
    HOW TO TRAVERSE A THREAD
    """
    # print(Process.process_head.readyQueue[2].cpu_List.thread_head.next_.cpu_time)  # traverse a thread

    """
    DONT NOT USE THIS
    """
    # Process.process_tail.next_ = Process.process_head  # circular Queue print
    # Process.process_tail.next_.cpu_List.thread_head.cpu_time)  #  access process head cpu_time from PROCESS
    # circular Queue

    """
    CREATE TEST CASES
    """

    """
    ACCESS QUEUES
    """
    # Process.process_head.readyQueue[0].pname
    # print(Process.process_head.readyQueue[0].cpu_List.thread_head.cpu_time + " cpu burst remaining.")

    print("------------------------------> FCFS <----------------------------------")
    print("Please enter a time for your snapshot! Ex: Enter a number from 0 to 643")
    print('Snapshot at: ', end=' ')
    e = int(input())
    print('\n')
    Process.runFCFS()

    """
    # ------------------------------------------START PHASE 2 -------------------------------------------------------------------
    """
if __name__ == "__main__":
    #  Clear last session
    Process.finishQueue = []
    Process.Execution_time = 0
    Process.Execution_Flag = False
    Process.Processing_Flag = True
    Process.CPUutilization = 0

    pList = []
    p1 = [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4]
    p2 = [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8]
    p3 = [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6]
    p4 = [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3]
    p5 = [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4]
    p6 = [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8]
    p7 = [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10]
    p8 = [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]

    pList.append(p1), pList.append(p2), pList.append(p3), pList.append(p4)
    pList.append(p5), pList.append(p6), pList.append(p7), pList.append(p8)

    cpuList = []
    ioList = []

    nodeList1 = []
    nodeList2 = []

    #  For each process separate the cpu and io burst.
    for i in pList:
        for j in range(1, len(i) + 1):
            if j % 2 == 0:
                ioList.append(i[j - 1])
            else:
                cpuList.append(i[j - 1])

        #  Calculating all cpu burst from each process.
        Process.CPUutilization += sum(cpuList)

        nodeList1.append(cpuList)
        nodeList2.append(ioList)
        cpuList = []
        ioList = []

    objList1 = []
    k = 0
    for node in nodeList1:
        cpuNodes = Thread()
        for c in node:
            if k == 0:
                cpuNodes.thread_head = CPU(c)
                cpuNodes.thread_tail = cpuNodes.thread_head
                k += 1
                continue
            cpuNodes.thread_tail.next_ = CPU(c)
            cpuNodes.thread_tail = cpuNodes.thread_tail.next_
            k += 1
        k = 0
        objList1.append(cpuNodes)

    objList2 = []
    for node in nodeList2:
        ioNodes = Thread()
        for i in node:
            if k == 0:
                ioNodes.thread_head = IO(i)
                ioNodes.thread_tail = ioNodes.thread_head
                k += 1
                continue
            ioNodes.thread_tail.next_ = IO(i)
            ioNodes.thread_tail = ioNodes.thread_tail.next_
            k += 1
        k = 0
        objList2.append(ioNodes)

    for i in range(8):

        p = Process()
        p.cpu_List = objList1[i]
        p.io_List = objList2[i]
        p.Tr = -1
        p.Tw = 0
        p.Ttr = 0
        p.pname = 'Process ' + str(i + 1)
        p.cont = True

        if k == 0:
            Process.process_head = p
            Process.process_tail = p
            Process.priorityQueue.append(p)
            k += 1
            continue
        else:
            Process.process_tail.next_ = p
            Process.process_tail = p
            k += 1
        Process.priorityQueue.append(p)

    print("------------------------------> SJF <----------------------------------")
    print("Please enter a time for your snapshot! Ex: Enter a number from 0 to 643")
    print('Snapshot at: ', end=' ')
    e = int(input())
    print('\n')
    Process.runSJF()
if __name__ == "__main__":
    #  Clear last session
    Process.finishQueue = []
    Process.Execution_time = 0
    Process.Execution_Flag = False
    Process.Processing_Flag = True
    Process.CPUutilization = 0

    pList = []
    p1 = [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4]
    p2 = [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8]
    p3 = [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6]
    p4 = [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3]
    p5 = [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4]
    p6 = [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8]
    p7 = [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10]
    p8 = [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]

    pList.append(p1), pList.append(p2), pList.append(p3), pList.append(p4)
    pList.append(p5), pList.append(p6), pList.append(p7), pList.append(p8)

    cpuList = []
    ioList = []

    nodeList1 = []
    nodeList2 = []

    #  For each process separate the cpu and io burst.
    for i in pList:
        for j in range(1, len(i) + 1):
            if j % 2 == 0:
                ioList.append(i[j - 1])
            else:
                cpuList.append(i[j - 1])

        #  Calculating all cpu burst from each process.
        Process.CPUutilization += sum(cpuList)

        nodeList1.append(cpuList)
        nodeList2.append(ioList)
        cpuList = []
        ioList = []

    objList1 = []
    k = 0
    for node in nodeList1:
        cpuNodes = Thread()
        for c in node:
            if k == 0:
                cpuNodes.thread_head = CPU(c)
                cpuNodes.thread_tail = cpuNodes.thread_head
                k += 1
                continue
            cpuNodes.thread_tail.next_ = CPU(c)
            cpuNodes.thread_tail = cpuNodes.thread_tail.next_
            k += 1
        k = 0
        objList1.append(cpuNodes)

    objList2 = []
    for node in nodeList2:
        ioNodes = Thread()
        for i in node:
            if k == 0:
                ioNodes.thread_head = IO(i)
                ioNodes.thread_tail = ioNodes.thread_head
                k += 1
                continue
            ioNodes.thread_tail.next_ = IO(i)
            ioNodes.thread_tail = ioNodes.thread_tail.next_
            k += 1
        k = 0
        objList2.append(ioNodes)

    for i in range(8):

        p = Process()
        p.cpu_List = objList1[i]
        p.io_List = objList2[i]
        p.Tr = -1
        p.Tw = 0
        p.Ttr = 0
        p.pname = 'Process ' + str(i + 1)
        pnum = 1

        if k == 0:
            Process.process_head1 = p
            Process.process_tail1 = p
            Process.roundRobin1Queue.append(p)
            k += 1
            continue
        else:
            Process.process_tail1.next_ = p
            Process.process_tail1 = p
            k += 1
        Process.roundRobin1Queue.append(p)

    print("------------------------------> MLFQ <----------------------------------")
    print("Please enter a time for your snapshot! Ex: Enter a number from 0 to 630")
    print('Snapshot at: ', end=' ')
    e = int(input())
    print('\n')
    Process.runMLFQ()

    Process.compare()


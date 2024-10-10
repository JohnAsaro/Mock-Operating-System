from pathfinder import filefinder

#Scheduler class
#This class will handle the scheduling of the PCBs

class scheduler:

    #Every time a PCB is added add it to CPU schedulers prority queues, the queue can be based on arrival time for SJF, and CPU required for FCFS
    #When we add a new PCB, we automatically call the scheduler to organize it, scheduler has two methods to change the way the prority queue is organized
    #Each time a PCB is removed from memory, we call the scheduler to remove it from the queue and reorganize memory
    
    def __init__(self, pcb_list):
        self.pcb_list = pcb_list #List of PCBs to be scheduled
        mode = "FCFS" #String value represents the scheduling mode, can be FCFS or SJF
        self.organize_pcb_list() #Organize the PCB list based on the scheduling info

    #Method to add a PCB to the scheduler
    def add_single_pcb(self, pcb):
        self.pcb_list.append(pcb)
        self.organize_pcb_list()

    #Method to remove a PCB from the scheduler
    def remove_pcb(self, pcb):
        self.pcb_list.remove(pcb)
        self.organize_pcb_list()
    
    #Method to organize the PCB list based on the scheduling info
    def organize_pcb_list(self):
        if(self.mode == "FCFS"):
            self.pcb_list.sort(key=lambda x: x.cpu_required) #This wont work because PCB list is not a dictonary so we need to change later
        elif(self.mode == "SJF"):
            self.pcb_list.sort(key=lambda x: x.arrival_time) #This wont work because PCB list is not a dictonary so we need to change later
    
    #Method to change the scheduling mode
    def change_mode(self, mode):
        if(mode != "FCFS" and mode != "SJF"):
            print("Invalid mode. Please enter either 'FCFS' or 'SJF'.")
        else:
            self.mode = mode
        self.organize_pcb_list()
    
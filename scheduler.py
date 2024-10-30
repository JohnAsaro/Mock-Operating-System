from pathfinder import filefinder

#Scheduler class
#This class will handle the scheduling of the PCBs

class scheduler:

    #Every time a PCB is added add it to CPU schedulers prority queues, the queue can be based on arrival time for SJF, and CPU required for FCFS
    #When we add a new PCB, we automatically call the scheduler to organize it, scheduler has two methods to change the way the prority queue is organized
    #Each time a PCB is removed from memory, we call the scheduler to remove it from the queue and reorganize memory
    
    def __init__(self, pcb_list):
        """ 
        Scheduler class to schedule PCBs in the OS
        Args: 
            pcb_list (list): List of PCBs to be scheduled
        """
        self.pcb_list = pcb_list #List of PCBs to be scheduled
        self.schedule_mode = "FCFS" #String value represents the scheduling mode, can be FCFS, SJF, or RR
        self.preemptive_or_non = "Preemptive" #String value represents the scheduling mode, can be Non-preemptive or Preemptive
        self.organize_pcb_list() #Organize the PCB list based on the scheduling info

        def __str__(self): #String representation of the scheduler, if printed is a lot cleaner than if this wasn't here
            return f"Scheduler(Scheduling mode: {self.preemptive_or_non} {self.schedule_mode})\n PCB List: {self.pcb_list}"

    #Method to add a PCB to the scheduler
    def add_single_pcb(self, pcb):
        """ 
        Add a single PCB to the scheduler
        Args:
            pcb (PCB): PCB to be added to the scheduler
        """
        self.pcb_list.append(pcb)
        self.organize_pcb_list()

    #Method to remove a PCB from the scheduler
    def remove_pcb(self, pcb):
        """ 
        Remove a PCB from the scheduler
        Args:
            pcb (PCB): PCB to be removed from the scheduler
        """
        self.pcb_list.remove(pcb)
        self.organize_pcb_list()
    
    #Method to organize the PCB list based on the scheduling info
    def organize_pcb_list(self):
        if self.schedule_mode in ["FCFS", "RR"]:
            #Sort by Arrival Time (First Come, First Serve), and then by p_id to break ties (lower PID first), RR without considering the quantum is just FCFS, so we initially set up our list in FCFS order, considering the quantum when we run the PCBS
            self.pcb_list.sort(key=lambda pcb: (pcb.arrival_time, pcb.p_id))
        elif self.schedule_mode == "SJF":
            #Sort by CPU required (Shortest Job First), and then by p_id to break ties (lower PID first)
            self.pcb_list.sort(key=lambda pcb: (pcb.cpu_required, pcb.p_id))
        
    #Method to change the scheduling mode
    def change_schedule_mode(self, schedule_mode):
        """ 
        Change the scheduling mode of the scheduler
        Args:
            schedule_mode (str): Scheduling mode to change to, any mode contained within "valid_modes"
        """
        valid_modes = ["FCFS", "SJF", "RR"]
        if schedule_mode not in valid_modes:
            print('Invalid mode. Please enter either "FCFS", "SJF" or "RR".')
        else:
            self.schedule_mode = schedule_mode
        self.organize_pcb_list()

    #Method to change between preemptive and non-preemptive scheduling
    def switch_pre_non_pre(self, mode):
        """
        Change the scheduling method of the scheduler
        Args:
            mode (str): Scheduling mode to change to, can be "Preemptive" or "Non-Preemptive"
        """
        if(mode != "Preemptive" and mode != "Non-Preemptive"):
            print('Invalid mode. Please enter either "Preemptive" or "Non-Preemptive".')
        else:
            self.preemptive_or_non = mode
        self.organize_pcb_list()

    #Method to get the PCB list
    def print_pcb_list(self):
        for pcb in self.pcb_list:
            print(pcb)
    
    #Method to quickly swap the PCB list
    def swap_pcb_list(self, new_pcb_list):
        """
        Quickly swap the PCB list with a new list
        Args:
            new_pcb_list (list): New list of PCBs to replace the current list
        """
        self.pcb_list = new_pcb_list
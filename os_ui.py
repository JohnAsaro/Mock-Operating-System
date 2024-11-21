from pathfinder import filefinder
from pcb import PCB, read_pcb_data, display_pcbs, validate_pcb_data
from scheduler import scheduler
from memory_manager import MemoryManager
import time

def boot(): #Display a welcome message and call menu function
    print("Welcome to John-OS!", end="\n")
    print("        __      __                ____  _____", end="\n")
    print("       / /___  / /_  ____        / __ \/ ___/", end="\n")
    print("  __  / / __ \/ __ \/ __ \______/ / / /\__ \ ", end="\n")
    print(" / /_/ / /_/ / / / / / / /_____/ /_/ /___/ /", end="\n") 
    print(" \____/\____/_/ /_/_/ /_/      \____//____/", end="\n\n")
    
    os_scheduler = scheduler(read_pcb_data(filefinder("os_pcbs.txt"))) #Create a scheduler object with the PCBs from os_pcbs.txt, which simulates the pcbs stored in memory
    os_MM = MemoryManager(15000) #Create a memory manager object with 15000 locations
    menu(os_scheduler, os_MM)  #Call the menu function with the scheduler object as an argument

def menu(os_scheduler, os_MM): 
    """
    Display menu options and call the appropriate function based on the user's choice.

    Args:
        os_scheduler (scheduler): The scheduler object to be used in the menu.
    """

    print("What is your choice?", end="\n")
    print("[1] Read PCB data from a file", end="\n")
    print("[2] Validate data for a PCB/list of PCBs", end="\n")
    print("[3] Create a new PCB from UI", end="\n")
    print("[4] Display all stored PCBs (in the order they are scheduled to be run)", end="\n")
    print("[5] Run PCBs from memory", end="\n")
    print("[6] Change scheduling algorithm", end="\n")
    print("[7] Switch between preempetive and non-preemptive scheduling", end="\n")
    print("[8] Change memory manager algorithm", end="\n")
    print("[9] Exit", end="\n")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == "1":
        pcb_data_file = filefinder(input("Enter the name of the file: "))
        pcb_list = read_pcb_data(pcb_data_file)
        display_pcbs(pcb_list)
        
    elif choice == "2":
       
        PCB_2_choice = input("Would you like to validate the list of stored PCBs [1], or another list of PCBs stored in a file [2]?: ")
        while PCB_2_choice != "1" and PCB_2_choice != "2":
            PCB_2_choice = input("Invalid input. Please enter '1' or '2': ").upper()
        if PCB_2_choice == "1":
            pcb_list = read_pcb_data(filefinder("os_pcbs.txt"))
        elif PCB_2_choice == "2":
            pcb_list = read_pcb_data(filefinder(input("Enter the name of the file: ")))

        if(validate_pcb_data(pcb_list) == True):
            print("All PCB data is valid")
        else:
            print("Some PCB data is invalid")

    elif choice == "3": #One problem that exists rn is that a PID X's child is not updated when a new PCB Y is created with a parent PID X

        valid = False
        file_path = filefinder("os_pcbs.txt")
        pcb_list = read_pcb_data(file_path) #Read the existing PCBs from the file

        while valid == False:    #Loop until valid PCB data is entered
            NEW_PCB = PCB(
            int(input("Enter PID (Process Identifier (PID), should be some unique integer): ")), 
            int(input("Enter CPU_State (Initial CPU state, should be 0 when initialized): ")),
            int(input("Enter Memory (Should be some integer representing the amount of bytes the process requires): ")),
            int(input("Enter Scheduling Info (Should be some integer corresponding to how high priority this process is, the lower the number the higher the priority): ")),
            int(input("Enter Accounting Info (Should be some integer representing how much time this process needs to run): ")),
            input("Enter Process State (Should be a string representing the state of the process, should be initialized as 'NEW'): "),
            None if (parent_input := input("Enter Parent PID (Should be the PID of the parent process or None if there is no parent): ")) == "None" else int(parent_input),
            None if (child_input := input("Enter Child PID (Should be the PID of the child process or None if there is no parent): ")) == "None" else int(child_input),          
            input("Enter Other Resources (Should be a string of any other system resources needed by the process): "),
            int(input("Enter Arrival Time (Should be an integer >= 0 representing the time at which the process arrives in the system): ")),
            int(input("Enter CPU Required (Should be an integer > 0 representing the amount of clock cycles required by the process): ")),
            int(input("Enter Quantum (Should be an integer > 0 representing the amount of clock cycles the process can run before context switching in round robin scheduling): ")),
            int(input("Enter Context Switch Penalty (Should be an integer >= 0 representing the penalty for a context switch): "))
            )
                        
            print("\n")
            
            #Check if the new PID is already in the list of existing PCBs
            newlist = pcb_list.copy()
            newlist.append(NEW_PCB)
            existing_pids = {pcb.p_id for pcb in pcb_list}
            if NEW_PCB.p_id in existing_pids:
                print(f"Error: PID {NEW_PCB.p_id} already exists. Please enter a unique PID.")
            elif not validate_pcb_data(newlist): #Check if the new PCB is valid
                print("Invalid PCB data. Please try again.")
            else:
                valid = True  #The new PCB is valid and can be added to the list of PCBs
        
        PCB_3_choice = input("New PCB created, would you like to store it in a file? (Y/N): ").upper()
        while PCB_3_choice != "Y" and PCB_3_choice != "N":
            PCB_3_choice = input("Invalid input. Please enter 'Y' or 'N': ").upper()

        if PCB_3_choice == "Y":
            with open(file_path, "a") as file: #Write the PCB to the file
                file.write(f"{NEW_PCB.p_id} {NEW_PCB.cpu_state} {NEW_PCB.memory} {NEW_PCB.scheduling_info} {NEW_PCB.accounting_info} {NEW_PCB.process_state} {NEW_PCB.parent} {NEW_PCB.children} {NEW_PCB.other_resources} {NEW_PCB.arrival_time} {NEW_PCB.cpu_required} {NEW_PCB.quantum} {NEW_PCB.context_switch_penalty}\n")
                print("Your PCB has been stored in the file 'os_pcbs.txt'.")
        else:
            PCB_3_choice_2 = input("Are you sure? Your PCB will be discarded? (Y/N): ").upper()
            while PCB_3_choice_2 != "Y" and PCB_3_choice_2 != "N":
                PCB_3_choice_2 = input("Invalid input. Please enter 'Y' or 'N': ").upper()
            if PCB_3_choice_2 == "Y":
                print("Your PCB has been discarded")
            elif PCB_3_choice_2 == "N":
                with open(file_path, "a") as file: #Write the PCB to the file
                    file.write(f"{NEW_PCB.p_id} {NEW_PCB.cpu_state} {NEW_PCB.memory} {NEW_PCB.scheduling_info} {NEW_PCB.accounting_info} {NEW_PCB.process_state} {NEW_PCB.parent} {NEW_PCB.children} {NEW_PCB.other_resources} {NEW_PCB.arrival_time} {NEW_PCB.cpu_required} {NEW_PCB.quantum} {NEW_PCB.context_switch_penalty}\n")
                    print("Your PCB has been stored in the file 'os_pcbs.txt'.")
    
    elif choice == "4":
        
        clock_cycle = 0 #Initialize the clock cycle to 0
        pcb_list = os_scheduler.pcb_list
        number_of_pcbs = len(pcb_list) #Get the number of PCBs in memory
        did_something = False #To see if we did something this clock cycle
        cycles_waiting = 0 #To keep track of how many clock cycles we have waited for a PCB to arrive
        last_pid = None #To keep track of the last PID that was printed

        if number_of_pcbs == 0: #If there are no PCBs in memory
            print("There are no PCBs stored in memory.")
            time.sleep(1) #Sleep for 1 second to give the user time to read the message
        else:
            while pcb_list: #While there are still PCBs in memory
                if os_scheduler.preemptive_or_non == "Preemptive": #If the scheduling is preemptive, we evaluate the PCBs at each clock cycle                    
                    if os_scheduler.schedule_mode == "RR": #If we are doing round robin scheduling
                        for pcb in pcb_list:
                            if pcb.arrival_time <= clock_cycle: #If the PCB has arrived
                                did_something = True
                                if cycles_waiting > 0: #If we have waited for PCBs to arrive
                                    print(f"We wait for {cycles_waiting} clock cycles for a PCB to arrive.")
                                    cycles_waiting = 0 #Reset the cycles_waiting counter
                              
                                if pcb.p_id != last_pid: #If the PID is different from the last PID printed
                                    print(pcb)
                                    last_pid = pcb.p_id

                                if pcb.cpu_required > 0: #If the PCB has more clock cycles remaining
                                    for _ in range(0, pcb.quantum): #Run the process for the quantum
                                        pcb.cpu_required -= 1 #Run the process for one clock cycle
                                        clock_cycle += 1 #Increment the clock cycle
                                        if pcb.cpu_required == 0:
                                            pcb_list.remove(pcb)
                                            break       
                    else:
                        for pcb in pcb_list:
                            if pcb.arrival_time <= clock_cycle: #If the PCB has arrived
                                did_something = True
                                if cycles_waiting > 0: #If we have waited for PCBs to arrive
                                    print(f"We wait for {cycles_waiting} clock cycles for a PCB to arrive.")
                                    cycles_waiting = 0 #Reset the cycles_waiting counter
                                
                                if pcb.p_id != last_pid: #If the PID is different from the last PID printed
                                    print(pcb)
                                    last_pid = pcb.p_id
                                 
                                pcb.cpu_required -= 1 #Run the process for one clock cycle
                                clock_cycle += 1 #Increment the clock cycle
                                
                                if pcb.cpu_required == 0:
                                    pcb_list.remove(pcb) #Remove the PCB from memory
                                
                                os_scheduler.organize_pcb_list() #Reorganize the PCB list based on the scheduling info                            
                                break #Move on to the next PCB
                    
                    if did_something == False: #If we didint do anything this clock cycle, we must wait for more PCBs to arrive
                        clock_cycle += 1 #Increment the clock cycle
                        cycles_waiting += 1 #Increment the cycles_waiting counter  
                    did_something = False

                if os_scheduler.preemptive_or_non == "Non-Preemptive": #If the scheduling is non-preemptive, we run each process until completion
                    for pcb in pcb_list:
                        if pcb.arrival_time <= clock_cycle: #If the PCB has arrived
                            did_something = True
                            if cycles_waiting > 0:
                                print(f"We wait for {cycles_waiting} clock cycles for a PCB to arrive.")
                                cycles_waiting = 0

                            if pcb.p_id != last_pid: #If the PID is different from the last PID printed
                                print(pcb)
                                last_pid = pcb.p_id
                            
                            while pcb.cpu_required > 0: #Run the process until it is complete
                                pcb.cpu_required -= 1 #Run the process for one clock cycle
                                clock_cycle += 1 #Increment the clock cycle

                            pcb_list.remove(pcb) #Remove the PCB from memory

                            break #Move on to the next PCB
                            #No need to reschedule the PCBs as each PCB is run to completion, no need to ever update context switchs because we never switch with non premptive
                    
                    if did_something == False: #If we didint do anything this clock cycle, we must wait for more PCBs to arrive
                        clock_cycle += 1 #Increment the clock cycle
                        cycles_waiting += 1 #Increment the cycles_waiting counter
                    
                    did_something = False

                #Restore the PCBs from the backup
                os_scheduler.swap_pcb_list(read_pcb_data(filefinder("os_pcbs.txt"))) #Restore the PCB list from the memory

        time.sleep(3) #Sleep for 3 seconds so reader can see output


    elif choice == "5":
        print("Running PCBs from memory...")
        
        clock_cycle = 0 #Initialize the clock cycle to 0
        pcb_list = os_scheduler.pcb_list
        number_of_pcbs = len(pcb_list) #Get the number of PCBs in memory (used to calculate average turnaround time)
        total_turnaround_time = 0 #Initialize the total turnaround time to 0
        context_switches = 0 #We start with 0 context switches
        context_switch_score = 0 #We start with 0 context switch score
        did_something = False #To see if we did something this clock cycle
        current_pcb = None #To keep track of the current PCB being run
        output_list = [] #To keep track of the output for each clock cycle
        started_pcbs = [] #To keep track of the PCBs that have started running

        if number_of_pcbs == 0: #If there are no PCBs in memory
            print("There are no PCBs stored in memory.")
            time.sleep(1) #Sleep for 1 second to give the user time to read the message
        else:
            while pcb_list: #While there are still PCBs in memory
                if os_scheduler.preemptive_or_non == "Preemptive": #If the scheduling is preemptive, we evaluate the PCBs at each clock cycle                    
                    if os_scheduler.schedule_mode == "RR": #If we are doing round robin scheduling
                        for pcb in pcb_list:
                            if pcb.arrival_time <= clock_cycle: #If the PCB has arrived
                                did_something = True
                                print(f"Running PCB {pcb.p_id} at clock cycle {clock_cycle}...")
                                
                                clock_cycle += 1 #Increment the clock cycle
                            
                                if pcb not in started_pcbs: #If the PCB is not yet running
                                    if os_MM.allocate_memory(pcb) == False: #If we can allocate memory for the PCB
                                        #Begin compaction
                                        print(f"Memory allocation failed at clock cycle {clock_cycle}. Compacting memory...")
                                        time.sleep(0.5) #Sleep for half of a second to give the user time to read the message
                                        os_MM.compact_memory() 
                                        if os_MM.allocate_memory(pcb) == False: #If memory compaction does not help
                                            print("Memory allocation failed after compacting memory. Moving on to next PCB.")
                                            time.sleep(0.5) #Sleep for half of a second to give the user time to read the message
                                            continue #Move on to the next PCB, continue instead of break to move to the next pcb in line instead of restarting
                                        else:
                                            started_pcbs.append(pcb) #Add the PCB to the list of started PCBs
                                    else:
                                        started_pcbs.append(pcb) #Add the PCB to the list of started PCBs
                                
                                pcb.cpu_state = 1 #Set the CPU state to 1 (running)

                                if pcb.cpu_required > 0: #If the PCB has more clock cycles remaining
                                    for _ in range(0, pcb.quantum): #Run the process for the quantum
                                        print(f"PCB {pcb.p_id} has {pcb.cpu_required} clock cycles remaining.")
                                        pcb.cpu_required -= 1 #Run the process for one clock cycle
                                        output_list.append(f"P{pcb.p_id}") #Add the PCB to the output list
                                        time.sleep(0.5) #Sleep for half a second to simulate the clock cycle, clock cycles are faster in real life most of the time but this is easier to read as opposed to a lot of information coming at you at once
                                        if pcb.cpu_required == 0:
                                            pcb.cpu_state = 0 #Set the CPU state to 0 (not running)
                                            pcb_list.remove(pcb)
                                            turnaround_time = clock_cycle - pcb.arrival_time #Calculate the turnaround time for the PCB
                                            total_turnaround_time += turnaround_time
                                            print(f"PCB {pcb.p_id} has finished running with at clock cycle {clock_cycle} turnaround time of {turnaround_time} clock cycles.")
                                            os_MM.deallocate_memory(pcb) #Deallocate memory for the PCB
                                            break
                            context_switches += 1 #Increment the context switch counter
                            context_switch_score += 1*pcb.context_switch_penalty #Add to the context switch score
                            #Move on to next PCB        

                    else: #Preemptive SJF Scheduling
                        for pcb in pcb_list:
                            if pcb.arrival_time <= clock_cycle: #If the PCB has arrived
                                did_something = True
                                if current_pcb != None and current_pcb != pcb: #If the current PCB is not the same as the PCB we are evaluating
                                    print(f"Running PCB {pcb.p_id} at clock cycle {clock_cycle}...")
                                    context_switches += 1 #We did a context switch
                                    context_switch_score += 1*current_pcb.context_switch_penalty #Penalty for switching from the previous PCB
                                elif current_pcb == None:
                                    print(f"Running PCB {pcb.p_id} at clock cycle {clock_cycle}...")
                                current_pcb = pcb

                                if pcb.cpu_required > 0: #If the PCB has more clock cycles remaining
                                    print(f"PCB {pcb.p_id} has {pcb.cpu_required} clock cycles remaining.")

                                clock_cycle += 1 #Increment the clock cycle

                                if pcb not in started_pcbs: #If the PCB is not yet running
                                    if os_MM.allocate_memory(pcb) == False: #If we can allocate memory for the PCB
                                        #Begin compaction
                                        print(f"Memory allocation failed at clock cycle {clock_cycle}. Compacting memory...")
                                        time.sleep(0.5) #Sleep for half of a second to give the user time to read the message
                                        os_MM.compact_memory() 
                                        if os_MM.allocate_memory(pcb) == False: #If memory compaction does not help
                                            print("Memory allocation failed after compacting memory. Moving on to next PCB.")
                                            time.sleep(0.5) #Sleep for half of a second to give the user time to read the message
                                            continue #Move on to the next PCB
                                        else:
                                            started_pcbs.append(pcb) #Add the PCB to the list of started PCBs
                                    else:
                                        started_pcbs.append(pcb) #Add the PCB to the list of started PCBs

                                pcb.cpu_state = 1 #Set the CPU state to 1 (running)

                                pcb.cpu_required -= 1 #Run the process for one clock cycle
                                output_list.append(f"P{pcb.p_id}") #Add the PCB to the output list

                                if pcb.cpu_required == 0:
                                    pcb.cpu_state = 0 #Set the CPU state to 0 (not running)
                                    pcb_list.remove(pcb) #Remove the PCB from memory
                                    turnaround_time = clock_cycle - pcb.arrival_time #Calculate the turnaround time for the PCB
                                    total_turnaround_time += turnaround_time #Add to total turnaround time
                                    print(f"PCB {pcb.p_id} has finished running with at clock cycle {clock_cycle} turnaround time of {turnaround_time} clock cycles.")
                                    os_MM.deallocate_memory(pcb) #Deallocate memory for the PCB
                                time.sleep(.5) #Sleep for half a second to simulate the clock cycle, clock cycles are faster in real life most of the time but this is easier to read as opposed to a lot of information coming at you at once
                                break #Move on to the next PCB
                        
                        os_scheduler.organize_pcb_list() #Reorganize the PCB list based on the scheduling info                            

                    
                    if did_something == False: #If we didint do anything this clock cycle, we must wait for more PCBs to arrive
                        print(f"No PCBs available for clock cycle {clock_cycle}, moving on to next clock cycle.")
                        clock_cycle += 1 #Increment the clock cycle
                        output_list.append("_") #Add the gap to the output list
                        time.sleep(0.5) #Sleep for half a second to simulate the clock cycle, clock cycles are faster in real life most of the time but this is easier to read as opposed to a lot of information coming at you at once
                    
                    did_something = False

                if os_scheduler.preemptive_or_non == "Non-Preemptive": #If the scheduling is non-preemptive, we run each process until completion
                    for pcb in pcb_list:
                        if pcb.arrival_time <= clock_cycle: #If the PCB has arrived
                            did_something = True
                            print(f"Running PCB {pcb.p_id} at clock cycle {clock_cycle}...")
                            if current_pcb != None and current_pcb != pcb: #If the current PCB is not the same as the PCB we are evaluating
                                    print(f"Running PCB {pcb.p_id}...")
                                    context_switches += 1 #We did a context switch
                                    context_switch_score += 1*current_pcb.context_switch_penalty #Penalty for switching from the previous PCB
                            elif current_pcb == None:
                                print(f"Running PCB {pcb.p_id} at clock cycle {clock_cycle}...")

                            current_pcb = pcb

                            if pcb not in started_pcbs: #If the PCB is not yet running
                                if os_MM.allocate_memory(pcb) == False: #If we can allocate memory for the PCB
                                    #Begin compaction
                                    print(f"Memory allocation failed at clock cycle {clock_cycle}. Compacting memory...")
                                    time.sleep(0.5) #Sleep for half of a second to give the user time to read the message
                                    os_MM.compact_memory() 
                                    if os_MM.allocate_memory(pcb) == False: #If memory compaction does not help
                                        print("Memory allocation failed after compacting memory. Moving on to next PCB.")
                                        time.sleep(0.5) #Sleep for half of a second to give the user time to read the message
                                        clock_cycle += 1 #Increment the clock cycle
                                        continue #Move on to the next PCB
                                    else:
                                        started_pcbs.append(pcb) #Add the PCB to the list of started PCBs
                                else:
                                    started_pcbs.append(pcb) #Add the PCB to the list of started PCBs

                            pcb.cpu_state = 1 #Set the CPU state to 1 (running)

                            while pcb.cpu_required > 0: #Run the process until it is complete
                                print(f"PCB {pcb.p_id} has {pcb.cpu_required} clock cycles remaining.")
        
                                pcb.cpu_required -= 1 #Run the process for one clock cycle
                                clock_cycle += 1 #Increment the clock cycle
                                output_list.append(f"P{pcb.p_id}") #Add the PCB to the output list

                            turnaround_time = clock_cycle - pcb.arrival_time #Calculate the turnaround time for the PCB
                            total_turnaround_time += turnaround_time #Add to total turnaround time
                            print(f"PCB {pcb.p_id} has finished running with at clock cycle {clock_cycle} turnaround time of {turnaround_time} clock cycles.")    
                            os_MM.deallocate_memory(pcb) #Deallocate memory for the PCB
                            pcb.cpu_state = 0 #Set the CPU state to 0 (not running)
                            pcb_list.remove(pcb) #Remove the PCB from memory

                            time.sleep(0.5) #Sleep for half a second to simulate the clock cycle, clock cycles are faster in real life most of the time but this is easier to read as opposed to a lot of information coming at you at once
                            break #Move on to the next PCB
                            #No need to reschedule the PCBs as each PCB is run to completion, no need to ever update context switchs because we never switch with non premptive
                    
                    if did_something == False: #If we didint do anything this clock cycle, we must wait for more PCBs to arrive
                        print(f"No PCBs available for clock cycle {clock_cycle}, moving on to next clock cycle.")
                        clock_cycle += 1 #Increment the clock cycle
                        output_list.append("_") #Add the gap to the output list
                        time.sleep(0.5) #Sleep for half a second to simulate the clock cycle, clock cycles are faster in real life most of the time but this is easier to read as opposed to a lot of information coming at you at once
                    
                    did_something = False

            average_turnaround_time = total_turnaround_time / number_of_pcbs #Calculate the average turnaround time
            print(f"Average turnaround time: {average_turnaround_time} clock cycles.")
            print(f"Total context switches: {context_switches}, Context switch score: {context_switch_score}.")
            print("All PCBs have been run from memory.")

            #Convert output_list to a string
            output_string = ''.join(map(str, output_list))
            print(f"Scheduling order: {output_string}")

            #Ask the user if they want to clear the PCBs or restore them
            PCB_5_choice = input("Would you like to clear os_pcbs.txt [1] or would you like to restore the PCB list to its previous state [2]? ")

            while PCB_5_choice != "1" and PCB_5_choice != "2":
                PCB_5_choice = input("Invalid input. Please enter '1' or '2': ")

            if PCB_5_choice == "1":
                print("Warning, this action is destructive and will overwrite the current PCBs in memory. The contents will be saved to backup_os_pcbs.txt.")
                PCB_5_choice_2 = input("Do you wish to continue? (Y/N): ").upper()

                while PCB_5_choice_2 != "Y" and PCB_5_choice_2 != "N":
                    PCB_5_choice_2 = input("Invalid input. Please enter 'Y' or 'N': ").upper()

                if PCB_5_choice_2 == "Y":
                    original_file_path = filefinder("os_pcbs.txt")
                    backup_file_path = filefinder("backup_os_pcbs.txt")
                    
                    #Backup current os_pcbs.txt to backup_os_pcbs.txt
                    with open(original_file_path, "r") as original_file:
                        data = original_file.read()
                    with open(backup_file_path, "w") as backup_file:
                        backup_file.write(data)
                    print("os_pcbs.txt has been backed up to backup_os_pcbs.txt.")

                    #Clear os_pcbs.txt
                    with open(original_file_path, "w") as file:
                        file.write("#PCBs stored in the memory of the OS\n\n") #Template for the memory file with header
                    print("os_pcbs.txt has been cleared.")
                else: #if PCB_5_choice_2 == "N"
                    #Restore the PCBs from the backup if the user chooses not to clear them
                    os_scheduler.swap_pcb_list(read_pcb_data(filefinder("os_pcbs.txt"))) #Restore the PCB list from the memory
                    print("Your PCB list has been restored.")

            else: #if PCB_5_choice == "2"
                #Restore the PCBs from the backup if the user chooses not to clear them
                os_scheduler.swap_pcb_list(read_pcb_data(filefinder("os_pcbs.txt"))) #Restore the PCB list from the memory
                print("Your PCB list has been restored.")
        time.sleep(1) #Sleep for 1 second to give the user time to read the message

    elif choice == "6":
        valid_modes = ["FCFS", "SJF", "RR"]
        print("The scheduling algorithm choices are FCFS (First Come, First Serve) SJF (Shortest Job First) and Rount Robin (RR).")
        print(f"The current scheduling algorithm is {os_scheduler.schedule_mode}.")
        
        newmode = input(f"Would you like to change the scheduling algorithm? (Input new scheduling algorithm acronym, ie: FCFS, SJF, RR): ").upper()
        while newmode not in valid_modes:
            newmode = input("Invalid input. Please enter a valid algorithm: ").upper()
        
        if newmode != os_scheduler.schedule_mode: #If the new mode is different from the current mode
            os_scheduler.change_schedule_mode(newmode)
            print(f"Scheduling algorithm changed to {newmode}.")
        else:
            print(f"Scheduling algorithm remains as {os_scheduler.schedule_mode}.")
        time.sleep(1) #Sleep for 1 second to give the user time to read the message


    elif choice == "7":
        print("The scheduling choices are Preemptive and Non-Preemptive.")
        print(f"The current scheduling is {os_scheduler.preemptive_or_non}.")

        if(os_scheduler.preemptive_or_non == "Preemptive"):
            newmode = "Non-Preemptive" #If the current mode is Preemptive, the new mode will be Non-Preemptive
        else:
            newmode = "Preemptive" #If the current mode is Non-Preemptive, the new mode will be Preemptive

        PCB_7_choice = input(f"Would you like to change the scheduling to {newmode}? (Y/N): ").upper()
        while PCB_7_choice != "Y" and PCB_7_choice != "N":
            PCB_7_choice = input("Invalid input. Please enter (Y/N): ").upper()
        
        if PCB_7_choice == "Y":
            os_scheduler.switch_pre_non_pre(newmode)
            print(f"Scheduling changed to {newmode}.")
        else:
            print(f"Scheduling remains as {os_scheduler.preemptive_or_non}.")
        time.sleep(1) #Sleep for 1 second to give the user time to read the message

    elif choice == "8":
        print("The memory manager algorithm choices are First-Fit and Worst-Fit.")
        print(f"The current memory manager algorithm is {os_MM.algorithm}.")
        
        if(os_MM.algorithm == "First-Fit"): #Switch to the algorithm not currently being used
            newmode = "Worst-Fit"
        else: 
            newmode = "First-Fit" 

        PCB_8_choice = input(f"Would you like to change the memory manager algorithm to {newmode}? (Y/N): ").upper()
        while PCB_8_choice != "Y" and PCB_8_choice != "N":
            PCB_8_choice = input("Invalid input. Please enter Y or N: ").capitalize()
        
        if PCB_8_choice == "Y": #If the user wants to change the algorithm
            os_MM.change_memory_algorithm(newmode) #Swap to alternative algorithm
            print(f"Memory manager algorithm changed to {newmode}.")
        else:
            print(f"Memory manager algorithm remains as {os_MM.algorithm}.") #Otherwise stay the same

    elif choice == "9":
        print("Goodbye!")
        exit()
    
    else:
        print("Invalid input. Please enter a number between 1 and 9.")
    
    menu(os_scheduler, os_MM)

#Call the boot function when the program is run
if __name__ == "__main__": 
    boot()
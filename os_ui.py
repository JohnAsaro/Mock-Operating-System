from pathfinder import filefinder
from pcb import PCB, read_pcb_data, display_pcbs, validate_pcb_data

def boot(): #Display a welcome message and call menu function
    print("Welcome to John-OS!", end="\n")
    print("        __      __                ____  _____", end="\n")
    print("       / /___  / /_  ____        / __ \/ ___/", end="\n")
    print("  __  / / __ \/ __ \/ __ \______/ / / /\__ \ ", end="\n")
    print(" / /_/ / /_/ / / / / / / /_____/ /_/ /___/ /", end="\n") 
    print(" \____/\____/_/ /_/_/ /_/      \____//____/", end="\n\n")
    menu()

def menu(): #Display menu options
    print("What is your choice?", end="\n")
    print("[1] Read PCB data from a file", end="\n")
    print("[2] Validate data for a PCB/list of PCB's", end="\n")
    print("[3] Create a new PCB from UI", end="\n")
    print("[4] Display all stored PCBs", end="\n")
    print("[5] Exit", end="\n")

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
            input("Enter Parent PID (Should be the PID of the parent process or None if there is no parent): "),
            input("Enter Children PID (Should be the PID of the child process or None if there are no children): "),
            input("Enter Other Resources (Should be a string of any other system resources needed by the process): "),
            int(input("Enter Arrival Time (Should be an integer >= 0 representing the time at which the process arrives in the system): ")),
            int(input("Enter CPU Required (Should be an integer > 0 representing the amount of CPU time required by the process): "))
            )
                        
            print("\n")
            
            #Check if the new PID is already in the list of existing PCBs
            existing_pids = {pcb.p_id for pcb in pcb_list}
            if NEW_PCB.p_id in existing_pids:
                print(f"Error: PID {NEW_PCB.p_id} already exists. Please enter a unique PID.")
            elif not validate_pcb_data([NEW_PCB]):
                print("Invalid PCB data. Please try again.")
            else:
                valid = True  #The new PCB is valid and can be added to the list of PCBs
        


        PCB_3_choice = input("New PCB created, would you like to store it in a file? (Y/N): ").upper()
        while PCB_3_choice != "Y" and PCB_3_choice != "N":
            PCB_3_choice = input("Invalid input. Please enter 'Y' or 'N': ").upper()

        if PCB_3_choice == "Y":
            with open(file_path, "a") as file: #Write the PCB to the file
                file.write(f"{NEW_PCB.p_id} {NEW_PCB.cpu_state} {NEW_PCB.memory} {NEW_PCB.scheduling_info} {NEW_PCB.accounting_info} {NEW_PCB.process_state} {NEW_PCB.parent} {NEW_PCB.children} {NEW_PCB.other_resources} {NEW_PCB.arrival_time} {NEW_PCB.cpu_required}\n")
                print("Your PCB has been stored in the file 'os_pcbs.txt'.")
        else:
            PCB_3_choice_2 = input("Are you sure? Your PCB will be discared? (Y/N): ").upper()
            while PCB_3_choice_2 != "Y" and PCB_3_choice_2 != "N":
                PCB_3_choice_2 = input("Invalid input. Please enter 'Y' or 'N': ").upper()
            if PCB_3_choice_2 == "Y":
                print("Your PCB has been discarded")
            elif PCB_3_choice_2 == "N":
                with open(file_path, "a") as file: #Write the PCB to the file
                    file.write(f"{NEW_PCB.p_id} {NEW_PCB.cpu_state} {NEW_PCB.memory} {NEW_PCB.scheduling_info} {NEW_PCB.accounting_info} {NEW_PCB.process_state} {NEW_PCB.parent} {NEW_PCB.children} {NEW_PCB.other_resources} {NEW_PCB.arrival_time} {NEW_PCB.cpu_required}\n")
                    print("Your PCB has been stored in the file 'os_pcbs.txt'.")
    
    elif choice == "4":
        pcb_data_file = filefinder("os_pcbs.txt")
        pcb_list = read_pcb_data(pcb_data_file)
        display_pcbs(pcb_list)
    
    elif choice == "5":
        print("Goodbye!")
        exit()
    
    else:
        print("Invalid input. Please enter a number between 1 and 5.")
        menu()
    
    menu()

#Call the boot function when the program is run
if __name__ == "__main__": 
    boot()
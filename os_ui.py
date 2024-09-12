from pathfinder import filefinder
from pcb import PCB, read_pcb_data, display_pcbs, validate_pcb_data

def boot(): #Display a welcome message and call menu function
    print("Welcome to the OS!", end="\n")
    print("   ___     ___   ", end="\n")
    print("  / _ \   / __|  ", end="\n")
    print(" | (_) |  \__ \  ", end="\n")
    print("  \___/   |___/  ", end="\n\n") 
    menu()

def menu(): #Display menu options
    print("What is your choice?", end="\n")
    print("[1] Read PCB data from a file", end="\n")
    print("[2] Validate data in input for each stored PCB", end="\n")
    print("[3] Create a new PCB from UI", end="\n")
    print("[4] Add a new PCB from file", end="\n")    
    print("[5] Display all stored PCBs", end="\n")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == "1":
        pcb_data_file = filefinder(input("Enter the name of the file: "))
        pcb_list = read_pcb_data(pcb_data_file)
        display_pcbs(pcb_list)
    elif choice == "2":
        pcb_list = read_pcb_data(filefinder("os_pcb_memory.txt"))
        if(validate_pcb_data(pcb_list) == True):
            print("All PCB data is valid")
        else:
            print("Some PCB data is invalid")
    
def main(): #Usage example
    pcb_data_file = filefinder("example_pcb_data.txt")
    pcb_list = read_pcb_data(pcb_data_file)
    display_pcbs(pcb_list)

#Test function
if __name__ == "__main__": 
    boot()
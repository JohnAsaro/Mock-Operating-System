from pathfinder import filefinder

#PCB class
class PCB:
    def __init__(self, p_id, cpu_state, memory, scheduling_info, accounting_info, process_state, parent, children, other_resources, arrival_time, cpu_required, quantum, context_switch_penalty, open_files = None):
        """
        PCB class to represent a process control block.
     
           Args:
            p_id (int): Process Identifier (PID), should be some unique integer.
            cpu_state (int): Inital CPU state, should be 0 when initalized.
            memory (int): Memory required by the process, should be some integer representing the amount of bytes the process requires.
            scheduling_info (int): Should be some interger corresponding to how high priority this process is, the lower the number the higher the priority.
            accounting_info (int): Should be some integer corresponding to how much time this process needs to run.
            process_state (str): Should be some string corresponding to the state of the process, should be initalized as "NEW".
            parent (PID): Pointer to/p_id of the parent process, should be None if this process has no parent.
            children (PID): Pointer to/p_id of the child process, should be None if this process has no children.
            other_resources (str): String of the other system resources needed by the process.
            arrival_time (int): Should be some integer >= 0 time at which the process arrives in the system.
            cpu_required (int): Should be some integer > 0 amount of CPU time required by the process.
            quantum (int): Should be some integer > 0 size of the quantum,  should be the same for all PCBs in memory.
            context_switch_penalty (int): Should be some integer > 0 cost of switching to a specific process,  should be the same for all PCBs in memory.
            open_files (file): Used with open_file as a pointer to the file handler, starts as None as no file is open initally.
        """
        
        self.p_id = p_id #INT, Process Identifier (PID), should be some unique integer
        self.cpu_state = cpu_state #INT, Inital CPU state, should be 0 when initalized
        self.memory = memory #INT, Memory required by the process, should be some integer
        self.scheduling_info = scheduling_info #INT, should be some interger corresponding to how high priority this process is, the lower the number the higher the priority
        self.accounting_info = accounting_info #INT, should be some integer corresponding to how much time this process needs to run
        self.process_state = process_state #STRING, should be some string corresponding to the state of the process, should be initalized as "NEW"
        self.parent = parent #p_id, pointer to/p_id of the parent process, should be None if this process has no parent
        self.children = children #p_id, pointer to/p_id of the child process, should be None if this process has no children
        self.other_resources = other_resources #STRING, string of the other system resources needed by the process
        self.arrival_time = arrival_time  #INT, should be some integer >= 0 time at which the process arrives in the system
        self.cpu_required = cpu_required #INT, should be some integer > 0, the amount of clock cycles the process needs to run
        self.quantum = quantum  #INT, should be some integer > 0 size of the quantum, the size should be the same for all processes, should be the same for all PCBs in memory
        self.context_switch_penalty = context_switch_penalty #INT, should be some integer > 0 cost of switching to a specific process, should be the same for all PCBs in memory
        self.open_files = open_files #Used with open_file as a pointer to the file handler
        

    def __str__(self): #String representation of the PCB, if printed is a lot cleaner than if this wasn't here
        return f"PCB({self.p_id}, {self.cpu_state}, {self.memory}, {self.scheduling_info}, {self.accounting_info}, {self.process_state}, {self.parent}, {self.children}, {self.open_files}, {self.other_resources}, {self.arrival_time}, {self.cpu_required}, {self.quantum}, {self.context_switch_penalty})"
    
    def open_file(self, file_path, mode='r'): #Open a file and set the open_files attribute to the file handler
        """
        Opens a file and set the open_files attribute to the file handler.
        
        Args:
            file_path (str): The path to the file to open.
            mode (str): The mode in which to open the file. Defaults to 'r' (read).
        """
        self.open_files = open(file_path, mode) 

    def close_file(self): #Close the file and set the open_files attribute to None
        """ Close the open file. """
        if self.open_files:
            self.open_files.close()
            self.open_files = None    

def read_pcb_data(file_path):
    """
    Reads PCB data from a given file and returns a list of PCB objects.

    Args:
        file_path (str): The path to the file containing PCB data.

    Returns:
        list: A list of PCB objects representing each process.

    Raises:
        ValueError: If the file contains data that cannot be parsed into the expected PCB format.
        FileNotFoundError: If the specified file does not exist.
    """
    pcb_list = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                #Skip empty lines, lines that start with 'Data Set', and lines that start with '#', as they are comments
                if line.strip() and not line.startswith("Data Set")  and not line.startswith("#"):
                    data = line.strip().split()

                    #Validate that the data line has the correct number of fields
                    if len(data) != 13:
                        raise ValueError(f"Incorrect data format in line: {line.strip()}")
                    
                    #Parse the data into appropriate types
                    p_id = int(data[0])
                    cpu_state = int(data[1])
                    memory = int(data[2])
                    scheduling_info = int(data[3])
                    accounting_info = int(data[4])
                    process_state = data[5]
                    parent = None if data[6] == "None" else int(data[6])
                    children = None if data[7] == "None" else int(data[7])
                    other_resources = data[8]
                    arrival_time = int(data[9])
                    cpu_required = int(data[10])
                    quantum = int(data[11])
                    context_switch_penalty = int(data[12]) 
                    #open_files, initally set to None, is not parsed from the file

                    #Create a new PCB object with the parsed data
                    pcb = PCB(
                        p_id=p_id,
                        cpu_state=cpu_state,
                        memory=memory,
                        scheduling_info=scheduling_info,
                        accounting_info=accounting_info,
                        process_state=process_state,
                        parent=parent,
                        children=children,
                        other_resources=other_resources,
                        arrival_time=arrival_time,
                        cpu_required=cpu_required,
                        quantum=quantum,
                        context_switch_penalty=context_switch_penalty
                    )

                    #Append the created PCB object to the list
                    pcb_list.append(pcb)

    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e

    except ValueError as e:
        print(f"Error: {e}")
        raise e

    return pcb_list

def display_pcbs(pcb_list): 
    """
    Display the PCBs in a list.

    Args:
       pcb_list: The list of PCB objects to display.
    """
    if not pcb_list:
        print("No PCBs to display.")
    for pcb in pcb_list:
        print(pcb)

def validate_pcb_data(pcb_list): #Check to see if the data in the PCBs is valid
    """
    Check to see if all of the PCB data is valid.

    Args:
       pcbs: The list of PCB objects to check.

    Returns:
        bool: True if all data is valid, False otherwise.
    """

    valid = True #Assume the data is valid until proven otherwise

    #Collect all valid p_id values from the PCB list
    valid_pids = {pcb.p_id for pcb in pcb_list}

    #Check for duplicate p_id values
    seen_pids = set()
    for pcb in pcb_list:
        if pcb.p_id in seen_pids:
            print(f"Error: Duplicate PID found for PCB with ID {pcb.p_id}")
            valid = False
        seen_pids.add(pcb.p_id)

    for pcb in pcb_list:
        if isinstance(pcb.p_id, int) == False:
            print(f"Error: Invalid PID for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.cpu_state, int) == False:
            print(f"Error: Invalid CPU state for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.memory, int) == False:
            print(f"Error: Invalid memory value for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.scheduling_info, int) == False:
            print(f"Error: Invalid scheduling info for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.accounting_info, int) == False:
            print(f"Error: Invalid accounting info for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.process_state, str) == False:
            print(f"Error: Invalid process state for PCB with ID {pcb.p_id}")
            valid = False

        #Validate parent and children against the list of valid PIDs
        if pcb.parent is not None and (not isinstance(pcb.parent, int) or pcb.parent not in valid_pids):
            print(f"Error: Invalid parent for PCB with ID {pcb.p_id}")
            valid = False
        if pcb.children is not None and (not isinstance(pcb.children, int) or pcb.children not in valid_pids):
            print(f"Error: Invalid children for PCB with ID {pcb.p_id}")
            valid = False
            
        if isinstance(pcb.other_resources, str) == False:
            print(f"Error: Invalid other resources for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.arrival_time, int) == False:
            print(f"Error: Invalid arrival time for PCB with ID {pcb.p_id}")
            valid = False
        if isinstance(pcb.cpu_required, int) == False:
            print(f"Error: Invalid CPU required for PCB with ID {pcb.p_id}")
            valid = False
        #For now I am not going to bother checking the values of quantum or context_switch_penalty as they are hardcoded in the PCB class,
        #but I will add some sort of check if I make them changable later
    return valid
       
        



#def main(): #Usage example
#    pcb_data_file = filefinder("example_pcb_data.txt")
#    pcb_list = read_pcb_data(pcb_data_file)
#    display_pcbs(pcb_list)
#    validate_pcb_data(pcb_list)

#Test function
#if __name__ == "__main__":
#    main()
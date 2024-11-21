class MemoryManager:

    #Memory Manager class 
    #Used to manage memory allocation and deallocationm, defaults to First-Fit algorithm
    
    def __init__(self, total_memory):
        """Initialize the memory manager.
        Args:
            total_memory (int): The total memory available in the system.
        """

        self.total_memory = total_memory #Total memory available in the system
        self.holes = [(0, total_memory)]  #Free memory blocks as (start, size)
        self.allocated_blocks = []  #Allocated memory blocks as (start, size, pcb_id)
        self.algorithm = "First-Fit"  #Memory allocation algorithm ("First-Fit" or "Worst-Fit"), default is First-Fit

    def __str__(self):
        """Return a string representation of the memory manager."""
        return f"MemoryManager(total_memory={self.total_memory}, holes={self.holes}, allocated_blocks={self.allocated_blocks})"
    
    def change_memory_algorithm(self, algorithm):
        """Change the memory allocation algorithm.
        Args:
            algorithm (str): The algorithm to use ("First-Fit" or "Worst-Fit").
        """
        self.algorithm = algorithm

    def allocate_memory(self, pcb, algorithm="First-Fit"):
        """
        Allocate memory to a process using the specified algorithm.
        Args:
            pcb (PCB): The PCB requesting memory.
            algorithm (str): The algorithm to use ("First-Fit" or "Worst-Fit").
        Returns:
            bool: True if allocation succeeded, False otherwise.
        """
        if algorithm == "First-Fit":
            for i, (start, size) in enumerate(self.holes): #Iterate through holes, the hole ranges from start to size, it can represented as (start, size)
                if size >= pcb.memory: #Enough space to allocate memory
                    #Allocate memory
                    self.holes.pop(i) #Remove hole
                    if size > pcb.memory: #Split hole if there is extra space
                        self.holes.insert(i, (start + pcb.memory, size - pcb.memory)) #Insert new hole if there is extra space
                    self.allocated_blocks.append((start, pcb.memory, pcb.p_id)) #Add to allocated blocks
                    print(f"PCB {pcb.p_id} allocated memory at address {start} with size {pcb.memory}.")
                    return True #We have found a hole to allocate memory, return True to confirm this to the OS
            return False #Memory allocation failed

        elif algorithm == "Worst-Fit":  
            largest_hole_index = -1 #Index of the largest hole
            largest_hole_size = -1 #Size of the largest hole
            for i, (start, size) in enumerate(self.holes): #Iterate through holes, the hole ranges from start to size, it can represented as (start, size)
                if size >= pcb.memory and size > largest_hole_size: #Enough space to allocate memory and larger than the current largest hole found
                    largest_hole_index = i
                    largest_hole_size = size 
            if largest_hole_index == -1: 
                print("Memory allocation failed.") #No hole found to allocate memory
                return False #Return False to indicate memory allocation failed to the OS
            start, size = self.holes.pop(largest_hole_index) #Retrieve the largest hole
            if size > pcb.memory: #If we can fit the process in the hole
                self.holes.insert(largest_hole_index, (start + pcb.memory, size - pcb.memory)) #Insert new hole if there is extra space
            self.allocated_blocks.append((start, pcb.memory, pcb.p_id)) #Add to allocated blocks
            print(f"PCB {pcb.p_id} allocated memory at address {start} with size {pcb.memory}.")
            return True #We have found a hole to allocate memory, return True to confirm this to the OS

    def deallocate_memory(self, pcb): #Deallocate memory for a block that has been processed
        """Free memory allocated to a process.
        Args:
            pcb (PCB): The PCB to deallocate memory for.
        """
        for block in self.allocated_blocks: #Iterate through allocated blocks
            if block[2] == pcb.p_id: #If the PCB ID matches the PCB ID of the block
                self.allocated_blocks.remove(block) #Remove the block
                self.holes.append((block[0], block[1])) #Add a hole where the block was
                self.holes.sort()  #Keep holes sorted by start address
                break

    def compact_memory(self): #Compact memory when fragmentation occurs

        #PROBLEM, THIS ERASES ALL HOLES, NEED TO FIX

        """Combine fragmented memory into one large block."""
        self.holes.sort() #Sort holes by start address
        combined_start = self.holes[0][0] #Retrieve the start address of the first hole
        combined_size = sum(size for _, size in self.holes) #Sum the sizes of all holes
        self.holes = [(combined_start, combined_size)] #Combine all holes into one large hole
        #print("Memory compaction performed.")

    #COMPACT ADJACENT HOLES METHOD

    
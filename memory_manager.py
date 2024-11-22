class MemoryManager:

    #Memory Manager class 
    #Used to manage memory allocation and deallocation, defaults to First-Fit algorithm
    
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

    def allocate_memory(self, pcb):
        """
        Allocate memory to a process using the specified algorithm.
        Args:
            pcb (PCB): The PCB requesting memory.
        Returns:
            bool: True if allocation succeeded, False otherwise.
        """
        #print(self.holes) #Print for troubleshooting

        if self.algorithm == "First-Fit":
            
            #print("First-Fit algorithm selected.") #Print for troubleshooting

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

        if self.algorithm == "Worst-Fit":  
            
            #print("Worst-Fit algorithm selected.") #Print for troubleshooting

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
            self.allocated_blocks.append((start, pcb.memory, pcb.p_id)) #Add to allocated blocks
            if size > pcb.memory: #If we can fit the process in the hole
                self.holes.insert(largest_hole_index, (start + pcb.memory, size - pcb.memory)) #Insert new hole if there is extra space
                self.holes.sort() #Keep holes sorted by start address
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

    def compact_memory(self):
        """Consolidate free memory while respecting allocated blocks."""
        
        self.consolidate_adjacent_holes() #Consolidate adjacent holes first
        self.holes.sort() #Sort holes by start address      
        
        total_hole_size = sum([hole[1] for hole in self.holes]) #Total size of all holes
        self.holes = [(0, total_hole_size)] #Create a single hole that spans the entire free memory

        new_allocation_start = total_hole_size #Start address for new allocations, all allocated blocks are after the consolidated hole
        moved_blocks = [] #List to store blocks that have been moved

        for block in self.allocated_blocks: #Iterate through allocated blocks
            start, size, pcb_id = block #Unpack the block
            moved_blocks.append((new_allocation_start, size, pcb_id)) #Add the block to moved blocks list with the new start address
            print(f"PCB {pcb_id} moved from address {start} to address {new_allocation_start} with size {size}.") #Show the user where the block has been moved
            new_allocation_start += size #Increment the start address for the next block allocation

        
        self.allocated_blocks = moved_blocks #Update the allocated blocks list

        print(f"Memory compaction complete. New compacted memory block: {self.holes[0]}, Allocated blocks: {self.allocated_blocks}") #Show the user the new hole that spans the entire free memory and the new allocated blocks


    def consolidate_adjacent_holes(self):
        """Combine adjacent holes into one large hole, done before compaction."""

        print("Consolidating adjacent holes...")
        self.holes.sort() #Sort holes by start address
        if len(self.holes) == 1: #If there is only one hole
            return #No need to consolidate
        
        newholes = [self.holes[0]] #List to store new (consolidated) holes, start with the first hole

        for hole in self.holes[1:]: #Iterate through the remaining holes
            if hole[0] == newholes[-1][0] + newholes[-1][1]: #If the last addition to newholes is adjacent to the current hole, combine them
                newholes[-1] = (newholes[-1][0], newholes[-1][1] + hole[1]) #Replace that last addition with a new hole that is the sum of the two
            else:
                newholes.append(hole) #Otherwise, add the hole to newholes
        self.holes = newholes
        #print("Adjacent holes consolidated.")
    
    
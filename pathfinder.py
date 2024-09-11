#Use this to construct file paths directly from the root of the repository, not actually part of the mock operating system per sey, just super convienent

import os

def filefinder(filename):

    current_dir = os.getcwd() #Get the current working directory

    while not os.path.exists(os.path.join(current_dir, ".git")): #Go back to root
        current_dir = os.path.dirname(current_dir)

    relative_path = ("Files\\") 
    file_path = os.path.join(current_dir, relative_path) #Construct the relative path to the CSV file from the root of the repository
    file_path = os.path.join(file_path, filename) #Add file name to end of path

    return file_path
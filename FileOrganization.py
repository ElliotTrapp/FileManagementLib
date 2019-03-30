'''
FileOrganization.py
Elliot Trapp
18/11/15

Utilities to automate file organization. Pulled from the git repo linked below. Find more documentation there.

SOURCE: https://gist.github.com/TutorialDoctor/5834bbefb9c9d795518e
This is a modified script from TutorialDoctor's GitHub linked below. All credit should go to them
'''

import os,os.path,shutil,fnmatch
from Libraries.FileManagementLib.FileUtilities import ListFullPaths

root_directory = os.getcwd()
directory_files = os.listdir(root_directory) # This is how you get all of the files and folders in a directory


def organize_files_by_letter(first_letter):
    for File in directory_files:
        # If the first letter in the file name is equal to the first_letter parameter...
        if str(File[0]).capitalize() == first_letter.capitalize():
            # Print the file (will print as a string)...
            print (File)
            # And print if it is a file or not (This step and the prior is nor really needed)
            print (os.path.isfile(File))
            print 
            # If the file is truly a file...
            if os.path.isfile(File):
                try:
                    # Make a directory with the first letter of the file name...
                    os.makedirs(first_letter)
                except:
                    None
                # Copy that file to the directory with that letter
                shutil.copy(File,first_letter)


def organize_files_by_extension(ext, root_directory=root_directory, recursive=False):
    fullExt = str(".", ext)
    # Organizing the files within this directory
    for File in ListFullPaths(root_directory):
        if (os.path.isfile(File)) and (File.endswith(fullExt)):
            print ("File: ", File, " matches the extension: ", fullExt)
            # If the file is a file and ends with . + ext
            try:
                # Make a directory with the keyword name...
                os.makedirs(os.path.join(root_directory,ext))
            except:
                print("Failed to make directory in:", root_directory, "!")
            # Copy that file to the directory with that keyword name
            shutil.move(File,os.path.join(root_directory,ext))
        elif (os.path.isdir(File)) and (recursive):
            print ("Recursively processing directory: ", File)
            # If the file is a directory and recursive is set to true
            organize_files_by_extension(File, ext, recursive)
                
                

def organize_files_by_keyword(keyword, root_directory=root_directory, recursive=False):
    # Organizing the files within this directory
    for File in ListFullPaths(root_directory):
        print ("Processing file: ", File)
        
        if (os.path.isfile(File)) and (keyword in File):
            # If the file is a file and contains the keyword
            try:
                print("making dir in: ", root_directory)
                # Make a directory with the keyword name...
                os.makedirs(os.path.join(root_directory,keyword))
            except:
                print("Failed to make directory in:", root_directory)
            # Copy that file to the directory with that keyword name
            print("copying")
            shutil.move(File,os.path.join(root_directory,keyword))

        elif (os.path.isdir(File)) and (recursive):
            # If the file is a directory and recursive is set to true
            print("Recursive call:", File)
            organize_files_by_keyword(File, keyword, recursive)
                
                
def organize_folders_by_letter(first_letter):
    for File in directory_files:
        if str(File[0]).capitalize() == first_letter.capitalize():
            # If the file is truly a directory...
            if os.path.isdir(File):
                try:
                    # Move the directory to the directory with the first_letter
                    shutil.move(File,first_letter)                    
                except:
                    None

                    
# Untested, but it should work
def organize_folders_by_keyword(keyword):
    for File in directory_files:
        # If the name of the file contains a keyword
        if fnmatch.fnmatch(File,'*' + keyword + '*'):
            # If the file is truly a folder/directory...
            if os.path.isdir(File):
                try:
                    # Move the directory to the directory with that keyword name
                    shutil.move(File,keyword)                    
                except:
                    None
#------------------------------------------------------------------------------

    
# IMPLEMENTATION
#------------------------------------------------------------------------------
#organize_files_by_letter("a", ".", True) # This is how you use it for one letter
#organize_files_by_letter('0', ".", True)
#organize_files_by_letter('o', ".", True)
#organize_files_by_letter('b', ".", True)
#organize_files_by_extension('txt', ".", True)
#organize_folders_by_letter('a', ".", True)
#organize_files_by_keyword('music', ".", True)
#------------------------------------------------------------------------------


def organize(option, recursive=False):
    if option == 1:
        # To organize files starting with all letters or numbers you can do this:
        for letter_or_number in 'abcdefghijklmnopqrstuvwxyz0123456789':
            organize_files_by_letter(letter_or_number, recursive)
    
    if option == 2:
        for folder in 'abcdefghijklmnopqrstuvwxyz0123456789':
            organize_folders_by_letter(folder, recursive)
    
    if option == 3:
        for ext in ['jpg','png','bmp','jpeg','JPG']:
            organize_files_by_extension(ext, recursive)
    
    if option == 4:
        for keyword in ['music','art','screenshot','sound','image']:
            organize_files_by_keyword(keyword, recursive)
    
    if option == 5:
        for keyword in ['music','art','social']:
            organize_folders_by_keyword(keyword, recursive)


# EXTRA STUFF
#------------------------------------------------------------------------------
            

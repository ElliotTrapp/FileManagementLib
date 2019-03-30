'''
Utilities.py
Elliot Trapp
18/11/15

Random assortment of utilities to support file management
'''

import os,os.path,shutil,fnmatch
import time, datetime
from numpy import genfromtxt, array, asarray
from Libraries.FileManagementLib.FileIO import WriteCSV

def GetCurrentTimeStamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d')
    return st

def MatchFiles(ext, directory_files):
    'Prints files with extension ext'
    for File in directory_files:
        if fnmatch.fnmatch(File,'*' + ext):
            print (File)
    # * matches everything
    # ? matches any single character
    # [seq] matches any character in seq
    # [!seq] matches any character not in seq

def ListFullPaths(path):
    'Returns the contents of a directory with entire path'
    for file in os.listdir(path):
        yield os.path.join(path, file)

def ListCSVFiles(path):
    'Returns the CSVs of a directory with entire path'
    for File in ListFullPaths(path):
        if '.csv' in File: yield File

def GetFilesByKeyword(input_files, keyword, recursive=False):
    """
    Return an array of all files with a keyword in their title in the list of directories
    in input_files
    @parameter input_files: a list of directories and files to iterate over
    @parameter extension: the extension to match the files with
    @returns the array of files
    """

    list_of_files = []

    for File in ListFullPaths(input_files):
        if (os.path.isdir(File)) and (recursive):
            if len(os.listdir(File)) == 0: print( "{0} is empty!".format(File)); continue
            list_of_files.extend(GetFilesByKeyword(File, keyword, recursive))
        elif (os.path.isfile(File)) and (keyword in File):
            list_of_files.append(File)

    return list_of_files


def GetFilesByExtension(input_files, extension='.csv', recursive=False):
    """
    Return an array of all files with a matching extension in the list of directories
    in input_files
    @parameter input_files: a list of directories and files to iterate over
    @parameter extension: the extension to match the files with
    @returns the array of files
    """

    list_of_files = []

    for File in ListFullPaths(input_files):
        if (os.path.isdir(File)) and (recursive):
            if len(os.listdir(File)) == 0: print( "{0} is empty!".format(File)); continue
            list_of_files.extend(GetFilesByExtension(File, extension, recursive))
        elif File in ListFullPaths(File):
            if (os.path.isfile(File)) and (File.endswith(extension)):
                list_of_files.append(File)
            
    return asarray(list_of_files)

def MergeListOfPaths(list_of_paths, output_directory=None):
    """
    Concatenate all files in a list of paths
    @parameter list_of_paths: a list of paths to iterate over
    @parameter output_directory: a single file location where to store the concatenated file
    @returns the concatenated file as a numpy array
    """

    combined_array = []

    for path in list_of_paths:
        data = pd.read_csv(path, skiprows=[0], delimiter=",", usecols=[3,4])
        #data = FileToRawData(path, skiprows=[0], delimiter=",", usecols=[3,4])
        combined_array.append(data)

    if output_directory is not None:
        WriteCSV(combined_array, output_directory)
    
    return combined_array


def MergeFilesWithKeyword(input_directory, keyword, output_directory=None, recursive=False):
    """
    Concatenate all files with a matching keyword in the list of directories in input_directories
    If output_directory is not None, write to output directory
    @parameter input_directories: a list of directories to iterate over
    @parameter output_directory: a single file location where to store the concatenated file
    @parameter extension: the extension to match the files with
    @returns the concatenated file as a numpy array
    """

    combined_array = []
    matching_files = []

    for File in ListFullPaths(input_directory):
        matching_files.extend(GetFilesByKeyword(File, keyword, recursive=recursive))

        combined_array.extend(MergeListOfPaths(matching_files))

    if output_directory is not None:
        WriteCSV(combined_array, output_directory)
    
    return combined_array

def MergeFilesWithExtension(input_drectory, extension='.csv', output_directory=None, recursive=False):
    """
    Concatenate all files with a matching extension in the list of directories in input_directories
    If output_directory is not None, write to output directory
    @parameter input_directories: a list of directories to iterate over
    @parameter output_directory: a single file location where to store the concatenated file
    @parameter extension: the extension to match the files with
    @returns the concatenated file as a numpy array
    """

    combined_array = []
    matching_files = []

    for File in input_drectory:
        matching_files.extend(GetFilesByExtension(File, extension, recursive=recursive))

        combined_array.extend(MergeListOfPaths(matching_files))

    if output_directory is not None:
        WriteCSV(array(combined_array), output_directory)
    
    return asarray(combined_array)
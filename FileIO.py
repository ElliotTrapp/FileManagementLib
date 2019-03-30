'''
FileIO.py
Elliot Trapp
18/11/15

Utilities to streamline download, extracting, and preparing files to be passed to the DataPreprocessingLib 
Contains a set of constant file paths. If you change the file structure of the repo, you might have to update
the constants below. All other code pulls the file paths from here, so you should only need to change it here.
'''

import os
import shutil
import urllib.request
import zipfile
import numpy as np
from numpy import genfromtxt, array
from logging import error
from pandas import read_csv
import pandas as pd
from numpy import savetxt, asarray, transpose, reshape
from pandas import DataFrame
import Libraries.DataProcessingLib.TransformData as Trans

# Filestructure Constants 
# Training Data
postprocessed_train_dir = r'.\Data\TrainData\PostProcessed\\'
compiled_train_dir = r'.\Data\TrainData\CompiledData\\'
raw_train_dir = r'.\Data\TrainData\RawData\\'

# Predict Data
postprocessed_predict_dir = r'.\Data\PredictData\PostProcessed\\'
compiled_predict_dir = r'.\Data\PredictData\CompiledData\\'
raw_predict_dir = r'.\Data\PredictData\RawData\\'

train_data_filename = r'181106_train_data'
train_labels_filename = r'181106_train_labels'

plot_dir = r'./Plots/'


def UnzipData(ZippedFile):
    """Extract all the content of a zipped file to the data directory.
    
    Arguments:
        ZippedFile {[string]} -- [The path/name of the zipped file.]
    """
    print("Extracting data from the zip file.\n")
    with zipfile.ZipFile(ZippedFile, 'r') as FileToExtract:
        FileToExtract.extractall("../Data")

def DownloadData(Url="http://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip"):
    """Downloads the data from the provided URL. Default is the LPW dataset.
    
    Keyword Arguments:
        Url {str} -- [The URL to download data from] (default: {"http://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip"})
    """

    # Try to download the data from the link provided.
    try:
        FileName = '../Data/' + Url.split('/')[-1]
        with urllib.request.urlopen(Url) as Response, open(FileName, 'wb') as OutFile:
            print("Downloading the dataset.\n")
            shutil.copyfileobj(Response, OutFile)
            print("\n Done downloading the data.\n")
    except urllib.error.HTTPError as ErrorCode:
        error('HTTPError = ' + str(ErrorCode.code))
    except urllib.error.URLError as ErrorCode:
        error('URLError = ' + str(ErrorCode.reason))
    except Exception:
        import traceback
        error('generic exception: ' + traceback.format_exc())
    
    # If the FileName is a zip file, then call UnzipData() 
    if (".zip" in FileName):
        UnzipData(FileName)
        # Delete the original zip file
        print("Deleting original file...\n")
        os.remove(FileName)

def Write3DArray(out_filename, out_data):
        # Write the array to disk
        with open(out_filename, 'w') as outfile:
            # I'm writing a header here just for the sake of readability
            # Any line starting with "#" will be ignored by numpy.loadtxt
            outfile.write('# Array shape: {0}\n'.format(out_data.shape))

            # Iterating through a ndimensional array produces slices along
            # the last axis. This is equivalent to data[i,:,:] in this case
            for data_slice in out_data:

                # The formatting string indicates that I'm writing out
                # the values in left-justified columns 7 characters in width
                # with 2 decimal places.  
                np.savetxt(outfile, data_slice, fmt='%-7.8f')

                # Writing out a break to indicate different slices...
                outfile.write('# New slice\n')


def Read3DArray(in_filename, in_shape):
    # Read the array from disk
    in_data = np.loadtxt(in_filename)

    # Note that this returned a 2D array!
    print ("Pre-reshaped csv array:\n",in_data.shape)

    # However, going back to 3D is easy if we know the 
    # original shape of the array
    in_data = in_data.reshape(in_shape)

    return in_data


def ReadCSV(in_filename, delimiter=",", usecols=None, skiprows=None):
    in_data = read_csv(in_filename,delimiter=delimiter,usecols=usecols,skiprows=skiprows,header=None)
    return in_data.values

def WriteCSV(out_filename, out_data, delimiter=",", add_index=False):
    df = pd.DataFrame(out_data)
    df.to_csv(out_filename,index=add_index,header=False,sep=delimiter)


def LoadData(train_dir=postprocessed_train_dir,
data_filename=train_data_filename,
labels_filename=train_labels_filename,
data_shape=(436788, 400, 2)):

    # Load data
    #in_csv_data = Read3DArray(str(train_dir + data_filename + r'.csv'), data_shape)
    in_npy_data = np.load(str(train_dir + data_filename + r'.npy'))
    
    # Load labels
    #in_csv_labels = ReadCSV(str(train_dir + labels_filename + r'.csv'))
    in_npy_labels = np.load(str(train_dir + labels_filename + r'.npy'))

    # Just to check that they're the same...
    # assert (in_npy_data.all() == in_csv_data.all())
    # assert (in_npy_labels.all() == in_csv_labels.all())
    
    # Use .npy file as train_data and train_labels
    train_data = in_npy_data
    train_labels = in_npy_labels

    assert(len(train_data) == len(train_labels))

    # One-hot encoding
    train_labels = np.array(Trans.OneHotEncoder1D(train_labels))
    train_data = np.array(train_data)

    print("train_data shape",train_data.shape)
    print("train_labels shape",train_labels.shape)
   
    assert(len(train_data) == len(train_labels))
    
    return train_data, train_labels
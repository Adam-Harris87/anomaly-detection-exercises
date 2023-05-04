# import data manipulation tools
import numpy as np
import pandas as pd
# import file access tools
import os

# -----------------------------------------------

def acquire_web_traffic():
    '''
    this will read in the codeup web traffic log from txt file in the local directory
    '''
    # set file name
    filename = 'anonymized-curriculum-access.txt'
    # check if file exists in local directory
    if os.path.exists(filename):
        # read in the file to a dataframe
        traffic = pd.read_csv(filename, sep=' ', header=None)
    # if the file doesn't exist
    else:
        # print an error
        print(f'file {filename} not found in local directory')
    # return the dataframe
    return traffic

# -----------------------------------------------

def prepare_web_traffic(traffic):
    '''
    this will prepare the codeup web traffic dataframe for use
    '''
    # set column names
    traffic = traffic.rename(columns={
        0:'date', 1:'time', 2:'page', 3:'user_id', 4:'cohort', 5:'ip'})
    # combine the date and time into one varaible
    traffic['datetime'] = traffic.date + ' ' + traffic.time
    # change the new datetime column to datetime type
    traffic.datetime = pd.to_datetime(traffic.datetime)
    # drop the redundant date and time columns and set datetime as the index
    traffic = traffic.drop(columns=['date', 'time']).set_index('datetime')
    # return the prepared dataframe
    return traffic

# -----------------------------------------------

def wrangle_web_traffic():
    '''
    this will perform both acquire and preparation steps in one command
    '''
    # acquire and prepare data
    return prepare_web_traffic(acquire_web_traffic())
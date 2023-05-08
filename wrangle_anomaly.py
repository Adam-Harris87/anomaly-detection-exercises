# import data manipulation tools
import numpy as np
import pandas as pd
# import file access tools
import os
import env

# -----------------------------------------------

def acquire_web_traffic():
    '''
    this will read in the codeup web traffic log from csv file in the local directory,
    if one does not exist, it will download the data via sql from the codeup server
    '''
    # set file name
    filename = 'curriculum_logs.csv'
    # check if file exists in local directory
    if os.path.exists(filename):
        print('opening file from local directory')
        # read in the file to a dataframe
        traffic = pd.read_csv(filename, index_col=0)
    # if the file doesn't exist
    else:
        # print an error
        print(f'file {filename} not found in local directory, downloading via SQL')
        # download dataset from codeup server
        # set database we are looking at
        database = 'curriculum_logs'
        # create sql connectioni
        connection = env.get_db_url(database)
        # create sql query
        query = '''
select l.date, l.time, l.path, l.user_id, l.cohort_id,
	l.ip, c.name as cohort_name, c.start_date, c.end_date, c.program_id
from logs l
left join cohorts c
	on l.cohort_id = c.id
;
        '''
        # query server via sql
        traffic = pd.read_sql(query, connection)
        # cache the data to local csv file
        traffic.to_csv(filename)
    # return the dataframe
    return traffic

# -----------------------------------------------

def prepare_web_traffic(traffic):
    '''
    this will prepare the codeup web traffic dataframe for use
    '''
    # combine the date and time into one varaible
    traffic['datetime'] = traffic.date + ' ' + traffic.time
    # change the new datetime column to datetime type
    traffic.datetime = pd.to_datetime(traffic.datetime)
    # drop the redundant date and time columns and set datetime as the index
    traffic = traffic.drop(columns=['date', 'time']).set_index('datetime')
    # drop null rows (there's only 1)
    traffic = traffic.dropna()
    # convert first part of website path into column called lesson
    # create an empty list
    page_list=[]
    # split the webpage path by '/'
    pages = traffic.path.str.split('/')
    # go through all of the pages
    for i in range(len(pages)):
        # make a list of the first part of the paths
        page_list.append(pages[i][0])
    # create a new column with the first part of the path
    traffic['lesson'] = page_list
    # return the prepared dataframe
    return traffic

# -----------------------------------------------

def wrangle_web_traffic():
    '''
    this will perform both acquire and preparation steps in one command
    '''
    # acquire and prepare data
    return prepare_web_traffic(acquire_web_traffic())
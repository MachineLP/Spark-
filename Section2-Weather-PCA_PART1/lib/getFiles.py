"""A function for getting the files for weather analysis from s3"""

import os.path as path
from shutil import rmtree
from subprocess import call
from os import system
from os.path import isfile,isdir

def exec(command):
    print(command)
    os.system(command)
def get_weather_files(state,data_dir):
    """
    get (using curl) the files needed for analyzing the weather of a US state
    """
    #read raw data
    tarname=state+'.tgz'
    parquet=state+'.parquet'
    if not isdir(data_dir+'/'+parquet):
        exec("curl https://mas-dse-open.s3.amazonaws.com/Weather/by_state_2/%s > %s/%s"%(tarname,data_dir,tarname))
        exec("tar -xzf %s/%s -C %s"%(data_dir,tarname,data_dir))
        exec("rm %s/%s"%(data_dir,tarname))
    
    #read statistics
    pickle='STAT_%s.pickle'%state
    pickle_gz = pickle+'.gz'
    if not isfile(data_dir+'/'+pickle):
        exec("curl https://mas-dse-open.s3.amazonaws.com/Weather/by_state_2/%s > %s/%s"%(pickle_gz,data_dir,pickle_gz))
        exec("gunzip %s/%s"%(data_dir,pickle_gz))

    #read  Stations info
    tarname='Weather_Stations.tgz'
    stations_parquet='stations.parquet'
    if not isdir(data_dir+'/'+stations_parquet):
        exec("curl https://mas-dse-open.s3.amazonaws.com/Weather/%s > %s/%s"%(tarname,data_dir,tarname))
        exec("tar -xzf %s/%s -C %s"%(data_dir,tarname,data_dir))
        exec("rm %s/%s"%(data_dir,tarname))

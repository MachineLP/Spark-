from Tester import *
import re 
import os
from urllib.request import urlretrieve

def get_data():
    data_dir='../../Data'
    if not os.path.isfile(data_dir+'/Moby-Dick.txt'):
        
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        filename='Moby-Dick.txt'
        f = urlretrieve("https://mas-dse-open.s3.amazonaws.com/"+filename, data_dir+'/'+filename)

def getkmers(text_file, l,k, map_kmers, count_kmers, sort_counts):
    # text_file: the text_file RDD read above
    # l: will print the l most common 3mers
    def removePunctuation(text):
        return re.sub("[^0-9a-zA-Z ]", " ", text)
    text = text_file.map(removePunctuation)\
                    .map(lambda x: x.lower())
    singles=map_kmers(text,k)
    count=count_kmers(singles)
    sorted_counts=sort_counts(count)
    return sorted_counts
    
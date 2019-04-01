import numpy as np
"""Code for packing and unpacking a numpy array into a byte array.
   the array is flattened if it is not 1D.
   This is intended to be used as the interface for storing 
   
   This code is intended to be used to store numpy array as fields in a dataframe and then store the 
   dataframes in a parquet file.
"""

def packArray(a):
    """
    pack a numpy array into a bytearray that can be stored as a single 
    field in a spark DataFrame

    :param a: a numpy ndarray 
    :returns: a bytearray
    :rtype:

    """
    if type(a)!=np.ndarray:
        raise Exception("input to packArray should be numpy.ndarray. It is instead "+str(type(a)))
    return bytearray(a.tobytes())


def unpackArray(x,data_type=np.int16):
    """
    unpack a bytearray into a numpy.ndarray

    :param x: a bytearray
    :param data_type: The dtype of the array. This is important because if determines how many bytes go into each entry in the array.
    :returns: a numpy array
    :rtype: a numpy ndarray of dtype data_type.

    """
    return np.frombuffer(x,dtype=data_type)
import numpy as np
def binary_search(array, target):
    """
    array is assumed to be sorted in increasing values
    Find the location i in the array such that array[i-1] <= target < array[i-1]
       """
    lower = 0
    upper = len(array)
    while lower < upper:   # use < instead of <=
        x = lower + (upper - lower) // 2
        val = array[x]
        if target == val:
            lower=x
            upper=x+1
            break
        elif target > val:
            if lower == x:
                break 
            lower = x
        elif target < val:
            upper = x
    return lower
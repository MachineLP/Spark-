import numpy as np
from numpy.random import rand
import time

def measureRandomAccess(size,filename='',k=1000):
    """Measure the distribution of random accesses in computer memory.

    :param size: size of memory block.
    :param filename: a file that is used as an external buffer. If filename=='' then everything is done in memory.
    :param k: number of times that the experiment is repeated.
    :returns: (mean,std,T):
              mean = the mean of T
              std = the std of T
              T = a list the contains the times of all k experiments
    :rtype: tuple

    """
    # Prepare buffer.
    if filename == '':
        inmem=True
        A=bytearray(size)
    else:
        inmem=False
        file=open(filename,'r+')
        
    # Read and write k times from/to buffer.
    sum=0; sum2=0
    T=np.zeros(k)

    try:
        for i in range(k):
            if (i%10000==0): print('\r',i, end=' ')
            loc=int(rand()*(size-0.00001))
            if size==0:
                t=time.time()
                d=time.time()-t
            elif inmem:
                t=time.time()
                x=A[loc]
                A[loc]=22
                d=time.time()-t
            else:
                t=time.time()
                file.seek(loc)
                poke=file.read(1)
                file.write("X")
                d=time.time()-t
            T[i]=d
            sum += d
            sum2 += d*d
        mean=sum/k; var=(sum2/k)-mean**2; std=np.sqrt(var)
        if not inmem:
            file.close()
        return (mean,std,T)
    except:
        print('bad loc',size,len(A),loc)


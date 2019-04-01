import time

stat=open('stats.txt','w')

def tee(line):
    print(line)
    stat.write(line+'\n')
    
def create_file(n,m,filename='DataBlock'):
    """Create a scratch file of a given size

    :param n: size of block
    :param m: number of blocks
    :param filename: desired filename
    :returns: time to allocate block of size n, time to write a file of size m*n
    :rtype: tuple

    """
    t1=time.time()
    A=bytearray(n)
    t2=time.time()
    file=open(filename,'wb')
    for i in range(m):
        file.write(str(A))
        if i % 100 == 0:
            print('\r',i,",", end=' ')
    file.close()
    t3=time.time()
    tee('\r              \ncreating %d byte block: %f sec, writing %d blocks %f sec' % (n,t2-t1,m,t3-t2))
    return (t2-t1,t3-t2)
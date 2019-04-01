from numpy import arange
from matplotlib.pylab import loglog,grid,plot
from scipy.special import erf,erfinv
from math import sqrt

def NormalCDF(x):
    return (1+erf(x/sqrt(2)))/2.0

def PlotTime(Tsorted,Mean,Std,Color='b',LS='-',Legend='',m_i=1,LogLog=True):
    """ plot distribution of times on a log-log scale

    :param Tsorted: a sorted sample of latencies 
    :param Mean: The main of the sample
    :param Std: The STD of the sample
    :param Color: The desired color either a tuple of 4 colors , or a single color, which is copied 4 times
    :param LS: LineStyle
    :param Legend: The name for this set of lines in the plot legend
    :param m_i: The number of blocks in the array
    """
    
    #print('PlotTime(',Tsorted,Mean,Std,Color,LS,Legend,m_i)
    
    if type(Color)==str:
        Color=[Color]*4
    if type(LS)==str:
        LS=[LS]*4
    
    if LogLog:
        _plt=loglog
    else:
        _plt=plot
            
    P=arange(1,0,-1.0/len(Tsorted))    # probability 
    _plt(Tsorted,P,color=Color[0],label=Legend,linestyle=LS[0])       # plot log-log of 1-CDF 
    

    _plt([Mean,Mean],[1,0.0001],color=Color[1],linestyle=LS[1])       # vert line at mean
    Y=0.1**((m_i+1.)/2.)
    _plt([Mean,min(Mean+Std,1)],[Y,Y],color=Color[2],linestyle=LS[2]) # horiz line from mean to mean + std
        
    x=arange(Mean,Mean+sqrt(2)*Std*erfinv(1.0-1.0/len(Tsorted)),Std/100)  # normal distribution 
    _plt(x,1-NormalCDF((x-Mean)/Std),color=Color[3],linestyle=LS[3])
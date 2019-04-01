from datetime import date
from numpy import shape
from matplotlib.dates import MonthLocator, DateFormatter
class YearPlotter:
    def __init__(self):
        start=365*1+1
        self.dates=[date.fromordinal(i) for i in range(start,start+365)]
        self.monthsFmt = DateFormatter("%b")
        self.months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
        #self.i=0

    def plot(self,T,fig,ax,label='',labels=None,title=None):
        #print(self.i,'fig=',fig,'ax=',ax)
        #self.i+=1
        shp=shape(T)
        if shp[0] != 365:
            raise ValueError("First dimension of T should be 365. Shape(T)="+str(shape(T)))
        if len(shp)==1:
            #print('one')
            ax.plot(self.dates,T,label=label);
        else:
            #print('more than 1')
            if labels is None:
                labels=[str(i) for i in range(shp[1])]
            for i in range(shp[1]):
                ax.plot(self.dates,T[:,i],label=labels[i])
        ax.xaxis.set_major_locator(self.months)
        ax.xaxis.set_major_formatter(self.monthsFmt)
        if not title is None:
            ax.set_title(title)
        #rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        ax.grid()
        ax.legend()
       
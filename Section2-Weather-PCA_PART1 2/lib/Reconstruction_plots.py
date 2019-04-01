import numpy as np
import pylab as plt

from lib.numpy_pack import packArray,unpackArray
from lib.decomposer import *
from lib.YearPlotter import YearPlotter
import matplotlib.pyplot as plt

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

class recon_plot:
    """A class for creating an interactive demonstration of approximating 
    a function with an orthonormal set of function"""
    def __init__(self,eigen_decomp,year_axis=False,fig=None,ax=None,interactive=False,Title=None,figsize=(6,4)):
        """ 
        Initialize the plot widget
        :param: eigen_decomp: An Eigen_Decomp object
        :param: year_axis: set to true if X axis should correspond to the months of the year.

        """
        self.eigen_decomp=eigen_decomp
        self.interactive=interactive
        self.fig=fig
        self.ax=ax
        #print('in recon_plot.__init__',ax)
        self.Title=Title
        self.figsize=figsize
        self.i=0
        
        self.year_axis=year_axis
        self.yearPlotter=None
        if year_axis:
            self.yearPlotter=YearPlotter()
        if not self.interactive:
            self.plot_combination(**self.eigen_decomp.coeff)

        return None

    def get_Interactive(self):
        widge_list,widge_dict = self.get_widgets()
        w=interactive(self.plot_combination, **widge_dict);
        #self.Title='Best reconstruction'
        #self.plot_combination(**self.eigen_decomp.coeff)
        self.Title='Interactive reconstruction'
        return widgets.VBox([widgets.HBox(widge_list),w.children[-1]])

    def get_widgets(self):
        """return the slider widget that are to be used

        :returns: widget_list: the list of widgets in order
                  widget_dict: a dictionary of the widget to be used in `interact

        :todo: make the sliders smaller: http://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Styling.html
        """
        coeff=self.eigen_decomp.C
        widge_dict={}
        widge_list=[]
        for i in range(self.eigen_decomp.n):
            if coeff[i]>0:
                r=[0,coeff[i]]
            else:
                r=[coeff[i],0]

            widge_list.append(widgets.FloatSlider(min=r[0],max=r[1],step=(r[1]-r[0])/10.,\
                                                  value=0,orientation='vertical',decription='v'+str(i)))
            widge_dict['c'+str(i)]=widge_list[-1]

        return widge_list,widge_dict

    def plot(self,y,label=''):
        if self.year_axis:
            self.yearPlotter.plot(y,self.fig,self.ax,label=label)
        else:
            self.ax.plot(self.eigen_decomp.x,y,label=label);

    def plot_combination(self,**coeff):
        """the plotting function that is called by `interactive`
           generates the plot according the the parameters set by the sliders

        :returns: None
        """
        
        #print(self.i,coeff)
        #self.i+=1
        #return None
        
        if self.interactive or self.fig is None:
            #print('setting axis in plot_combination')
            self.fig=plt.figure(figsize=self.figsize)
            self.ax=self.fig.add_axes([0,0,1,1])

        A=self.eigen_decomp.mean
        self.plot(A,label='mean')

        for i in range(self.eigen_decomp.n):
            #print('in plot_combinations, U.shape=',self.eigen_decomp.U.shape)
            g=self.eigen_decomp.U[:,i]*coeff['c'+str(i)]
            A=A+g
            self.plot(A,label='c'+str(i))
        self.plot(self.eigen_decomp.f,label='target')
        self.ax.grid(figure=self.fig)        
        self.ax.legend()
        self.ax.set_title(self.Title)
        if self.interactive:
            plt.show()  # This hack was found by trial and error.  I
                        # don't know why it works! But using the same
                        # "show" for both interactive and
                        # non-interactive creates problems.
        else:
            self.fig.show()
        return None

def plot_decomp(row,Mean,EigVec,fig=None,ax=None,Title=None,interactive=False):
    """Plot a single reconstruction with an informative title

    :param row: SparkSQL Row that contains the measurements for a particular station, year and measurement. 
    :param Mean: The mean vector of all measurements of a given type
    :param v: eigen-vectors for the distribution of measurements.
    :param fig: a matplotlib figure in which to place the plot
    :param ax: a matplotlib axis in which to place the plot
    :param Title: A plot title over-ride.
    :param interactive: A flag that indicates whether or not this is an interactive plot (widget-driven)
    :returns: a plotter returned by recon_plot initialization
    :rtype: recon_plot

    """
    target=np.array(unpackArray(row.Values,np.float16),dtype=np.float64)
    if Title is None:
        Title='%s / %d    %s'%(row['station'],row['year'],row['measurement'])
    eigen_decomp=Eigen_decomp(range(1,366),target,Mean,EigVec)
    plotter=recon_plot(eigen_decomp,year_axis=True,fig=fig,ax=ax,interactive=interactive,Title=Title)
    return plotter

def plot_recon_grid(rows,Mean,EigVec,column_n=4, row_n=3, figsize=(15,10),header='c2=%3.2f,r2=%3.2f',params=('coeff_2','res_2')):
    """plot a grid of reconstruction plots

    :param rows: Data rows (as extracted from the measurements data-frame
    :param Mean: A vector defining the mean
    :param EigVec: The top k eigen-vectors
    :param column_n: number of columns
    :param row_n:  number of rows
    :param figsize: Size of figure
    :param header: the format of the header that appears above each graph. (default: 'c2=%3.2f,r2=%3.2f)
    :param params: the names of the columns whose value will appear in the header. (default: params=('coeff_2','res_2'))
    :returns: None
    :rtype: 

    """
    fig,axes=plt.subplots(row_n,column_n, sharex='col', sharey='row',figsize=figsize);
    k=0
    for i in range(row_n):
        for j in range(column_n):
            row=rows[k]
            k+=1
            P=tuple([row[p] for p in params])
            _title=header%P
            plot_decomp(row,Mean,EigVec,fig=fig,ax=axes[i,j],Title=_title,interactive=False)
    return None
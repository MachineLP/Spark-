from matplotlib.pylab import subplots,axis
def plot_pair(pair,func):
    """
    Create two side-by-side plots:
    pair
    """
    j=0
    fig,X=subplots(1,2,figsize=(16,6))
    axes=X.reshape(2)
    for m in pair:
        axis = axes[j]
        j+=1
        func(m,fig,axis)

def plot_single(element,func,filename):
    fig,axis=subplots(1,1,figsize=(8,6))
    func(element,fig,axis)
    fig.savefig(filename)

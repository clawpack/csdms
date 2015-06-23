"""
Fetch topo files needed for this example:
    
Call functions with makeplots==True to create plots of topo, slip, and dtopo.
"""

import os,sys

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")


def get_topo(makeplots=False):
    """
    Retrieve the topo file from the GeoClaw repository.
    """
    from clawpack.geoclaw import topotools, util
    topo_fname = 'etopo1-230250035050.asc'
    url = 'http://www.geoclaw.org/topo/etopo/' + topo_fname
    util.get_remote_file(url, output_dir='.', file_name=topo_fname,
            verbose=True)

    if makeplots:
        from matplotlib import pyplot as plt
        topo = topotools.Topography(topo_fname, topo_type=2)
        topo.plot()
        fname = os.path.splitext(topo_fname)[0] + '.png'
        plt.savefig(fname)
        print "Created ",fname


if __name__=='__main__':
    get_topo(True)

#!/usr/bin/env python

from clawpack.geoclaw import dtopotools
import yaml

def okada_make_dtopo(sift_slips,dx_in,buffer_size_in,times_in):
    fault = dtopotools.SiftFault()
    fault.set_subfaults(sift_slips)
    x,y = fault.create_dtopo_xy(dx=dx_in, buffer_size=buffer_size_in)
    dtopo = fault.create_dtopography(x,y,times=times_in)
    return (dtopo.X,dtopo.Y,dtopo.dZ)
    
def read_params_from_file(fname):
    # Read model parameters from a file.
    with open(fname, 'r') as fp:
        params = yaml.load(fp)
    params['dx'] = eval(params['dx'])
    params.setdefault('sift_slips', {'acszb65':1.})
    params.setdefault('dx', 1./60.)
    params.setdefault('buffer_size', 0.5)
    params.setdefault('times', [1.])

    return params

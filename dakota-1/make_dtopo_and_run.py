
from pylab import *
import os,sys
from clawpack.geoclaw import dtopotools, topotools
from clawpack.geoclaw import interptools_new as interptools
from clawpack.visclaw import colormaps

sf1 = 'acszb65'; sf2 = 'acsza65'; sf3 = 'acszb64'; sf4 = 'acsza64'
fault = dtopotools.SiftFault()


def plot_fault_dtopo(fault,dtopo):
    fig = figure(figsize=(14,6))
    ax1 = subplot(121)
    fault.plot_subfaults(axes=ax1,slip_color=True,\
                         cmax_slip=20,cmap_slip=colormaps.white_red)
    topo_fname = 'etopo1-230250035050.asc'
    topo = topotools.Topography(topo_fname, topo_type=2)
    contour(topo.X, topo.Y, topo.Z, [0], colors='g')
    axis([233,237,40,43])
    plot([235.80917],[41.74111],'go')
    
    ax2 = subplot(122)
    dtopo.plot_dZ_colors(t=1., axes=ax2)
    contour(topo.X, topo.Y, topo.Z, [0], colors='g')
    axis([233,237,40,43])
    plot([235.80917],[41.74111],'go')

    fname = 'dtopo.png'
    savefig(fname)
    print "Created", fname

    dz_CC = interptools.interp(235.80917,41.74111,\
                dtopo.X, dtopo.Y, dtopo.dZ[-1,:,:])
    print "dz at CC: ",dz_CC
    return dz_CC

def make_dtopo(z1,z2):

    A1 = 10. - z1 - z2
    A2 = 10. + z1 - z2
    A3 = 10. - z1 + z2
    A4 = 10. + z1 + z2
    print "Amplitudes: ",A1,A2,A3,A4

    sift_slips = {sf1:A1, sf2:A2, sf3:A3, sf4:A4}
    fault.set_subfaults(sift_slips)
    x,y = fault.create_dtopo_xy(dx = 1./60., buffer_size=0.5)
    dtopo = fault.create_dtopography(x,y,times=[1.])

    print "Mw = %4.2f" % fault.Mw()

    # rundir = 'run_%s_%s' % (str(i).zfill(2), str(j).zfill(2))
    #os.system('mkdir -p %s' % rundir)

    filename = 'dtopo.tt3'
    dtopo.write(filename)
    print "Created ",filename

    if 1:
        dz_CC = plot_fault_dtopo(fault,dtopo)


def run_geoclaw():
    os.system('make data')
    print "Running GeoClaw..."
    os.system('make output > output.txt')

def make_output_for_dakota():
    from clawpack.visclaw.data import ClawPlotData
    plotdata = ClawPlotData()
    plotdata.outdir = '_output'   # set to the proper output directory
    gaugeno = 34                  # gauge number to examine
    g = plotdata.getgauge(gaugeno)
    gauge_max = g.q[3,:].max()
    print "Maximum elevation observed at gauge %s: %6.2f meters" \
        % (gaugeno, gauge_max)
    fname = 'results.out'
    f = open(fname,'w')
    f.write("%6.2f\n" % gauge_max)
    f.close()
    print "Created ",fname

    if 1:
        figure()
        plot(g.t, g.q[3,:])
        title("Gauge %s" % gaugeno)
        ylabel('Elevation (meters)')
        xlabel('time (seconds)')
        fname = 'gauge.png'
        savefig(fname)
        print 'Created ',fname

if __name__=='__main__':
    z1 = float(sys.argv[1])
    z2 = float(sys.argv[2])
    make_dtopo(z1, z2)
    run_geoclaw()
    make_output_for_dakota()


#! /usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt

from okada_utils import okada_make_dtopo,read_params_from_file

class Okada_model(object):
    # immutable variables here
    _name = 'Okada Model in GeoCLAW'
    _input_var_names = ('sift_slips','dx','buffer_size','times')  
    _output_var_names = ('X','Y','dZ')

    def __init__(self):
        self._sift_slips = {'acszb65':1.}
        self._dx = 1./60.
        self._dy = 1./60.
        self._buffer_size = .5
        self._times = [1.]
        self._var_grid = {}
        self._grid_type = {}
        self._grid_shape = {}
        self._grid_origin = {}
        self._grid_spacing = {}
        self._values = {}

    def initialize(self, fname):
        params = read_params_from_file('input.yaml')
        self.X = None
        self.Y = None
        self.dZ = None

        sift_slips = params['sift_slips']
        dx = params['dx']
        buffer_size = params['buffer_size']
        times = params['times']
        
        self._sift_slips = sift_slips
        self._dx = dx              # current geoclaw Okada uses square grids
        self._dy = dx
        self._var_grid = { 
            'x': 0,
            'y': 1
        }
        self._grid_type = {
            0: 'uniform_rectilinear_grid',
            1: 'uniform_rectilinear_grid'
        }
        self._grid_spacing[0] = self._dx
        self._grid_spacing[1] = self._dx
        self._grid_origin[0] = np.min(self.X)
        self._grid_origin[1] = np.min(self.Y)
        self._buffer_size = buffer_size
        self._times = times
        self.time = times[0]
        self.time_tick = 0
        self.end_time = times[-1] 
        self._var_units = {'X': 'degree',
                           'Y': 'degree',
                           'dZ': 'm'}

    def update(self):
        # only one "time-step" is taken (currently instantaneous rise)
        self.X,self.Y,self.dZ = okada_make_dtopo(self._sift_slips,self._dx,\
                                                self._buffer_size,
                                                self._times)
        self._grid_shape[0] = np.shape(self.X)[0]
        self._grid_shape[1] = np.shape(self.Y)[1]
        self._values['X'] = self.X
        self._values['Y'] = self.Y
        self._values['dZ'] = self.dZ
        self.time = self._times[-1]

    def finalize(self):
        """Finalize model."""
        self._model = None

    # getters and setters

    def get_input_var_names(self):
        """Get names of input variables."""
        return self._input_var_names

    def get_output_var_names(self, var_val):
        """Get names of output variables."""
        var_val = self._output_var_names
        return True

    def get_var_grid(self, var_name, var_val):
        """Grid id for a variable.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        Returns
        -------
        int
            Grid id.
        """
        var_val = self._var_grid[var_name]
        return True

    def get_var_nbytes(self, var_name):
        """Get units of variable.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        Returns
        -------
        int
            Size of data array in bytes.
        """
        return self.get_value_ref(var_name).nbytes

    def get_var_type(self, var_name):
        """Data type of variable.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        Returns
        -------
        str
            Data type.
        """
        return str(self.get_value_ref(var_name).dtype)

    def get_var_units(self, var_name, var_val):
        """Get units of variable.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        Returns
        -------
        str
            Variable units.
        """
        var_val = self._var_units[var_name]
        return True

    def set_value(self, var_name, src):
        """Set model values.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        src : array_like
            Array of new values.
        """
        val = self.get_value_ref(var_name)
        val[:] = src

    def get_component_name(self):
        """Name of the component."""
        return self._name

    def get_grid_type(self, grid_id, grid):
        """Type of grid."""
        grid = self._grid_type[grid_id]
        return True

    def get_grid_shape(self, grid_id, grid_shape):
        """Number of rows and columns of uniform rectilinear grid."""
        grid_shape = self._grid_shape[grid_id]
        return True

    def get_grid_shape(self, grid_id):
        """Number of rows and columns of uniform rectilinear grid."""
        return self._grid_shape[grid_id].copy()

    def get_grid_spacing(self, grid_id, grid_spacing):
        """Spacing of rows and columns of uniform rectilinear grid."""
        grid_spacing = self._grid_spacing[grid_id]

    def get_grid_origin(self, grid_id, grid_origin):
        """Origin of uniform rectilinear grid."""
        grid_origin = self._grid_origin[grid_id]
        return True

    # is passing on an empty variables the right thing?
    # 
    #def get_value(self, var_name, var_val):
    #    """Copy of values.
    #    Parameters
    #    ----------
    #    var_name : str
    #        Name of variable as CSDMS Standard Name.
    #    Returns
    #    -------
    #    array_like
    #        Copy of values.
    #    """
    #    var_val = self._values[var_name]
    #    return True

    def get_value(self, var_name):
        """Copy of values.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        Returns
        -------
        array_like
            Copy of values.
        """
        return self.get_value_ref(var_name).copy()

    def get_value_ref(self, var_name):
        """Reference to values.
        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        Returns
        -------
        array_like
            Value array.
        """
        return self._values[var_name]

    def get_current_time(self):
        """Current time of model."""
        return self.time

    def get_grid_rank(self, grid_id):
        """Rank of grid.
        Parameters
        ----------
        grid_id : int
            Identifier of a grid.
        Returns
        -------
        int
            Rank of grid.
        """
        return len(self.get_grid_shape(grid_id))


def main():
    model = Okada_model()
    model.initialize('input.yaml')

    print('Running Okada Model...')
    model.update()

    model.finalize()

    print(model.get_value('dZ'))


if __name__ == '__main__':
    main()

# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Integration tests for the `iris.experimental.geovista.cube_to_polydata` function."""

import numpy as np

from iris import load_cube
from iris.experimental.geovista import cube_to_polydata
from iris.experimental.ugrid import PARSE_UGRID_ON_LOAD
from iris.tests import get_data_path


def test_integration_2d():
    file_path = get_data_path(
        [
            "NetCDF",
            "ORCA2",
            "votemper.nc",
        ]
    )
    with PARSE_UGRID_ON_LOAD:
        global_cube = load_cube(file_path, "votemper")

    polydata = cube_to_polydata(global_cube[0, 1, :])
    # This is a known good output, we have plotted the result and checked it.
    assert polydata.GetNumberOfCells() == 26640
    assert polydata.GetNumberOfPoints() == 26969


def test_integration_1d():
    file_path = get_data_path(
        [
            "NetCDF",
            "global",
            "xyt",
            "SMALL_hires_wind_u_for_ipcc4.nc",
        ]
    )
    with PARSE_UGRID_ON_LOAD:
        global_cube = load_cube(file_path)

    polydata = cube_to_polydata(global_cube[0, :])
    # This is a known good output, we have plotted the result and checked it.
    assert polydata.GetNumberOfCells() == 51200
    assert polydata.GetNumberOfPoints() == 51681


def test_integration_mesh():
    file_path = get_data_path(
        [
            "NetCDF",
            "unstructured_grid",
            "lfric_ngvat_2D_72t_face_half_levels_main_conv_rain.nc",
        ]
    )

    with PARSE_UGRID_ON_LOAD.context():
        global_cube = load_cube(file_path, "conv_rain")

    polydata = cube_to_polydata(global_cube[0, :])
    # This is a known good output, we have plotted the result and checked it.
    assert polydata.GetNumberOfCells() == 864
    assert polydata.GetNumberOfPoints() == 866
    np.testing.assert_array_equal(polydata.active_scalars, global_cube[0, :].data)

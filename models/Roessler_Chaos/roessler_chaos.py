"""
Python model 'roessler_chaos.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.0.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 0.03125,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(name="a", comp_type="Constant", comp_subtype="Normal")
def a():
    return 0.2


@component.add(name="b", comp_type="Constant", comp_subtype="Normal")
def b():
    return 0.2


@component.add(name="c", comp_type="Constant", comp_subtype="Normal")
def c():
    return 5.7


@component.add(
    name="dxdt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"y": 1, "z": 1},
)
def dxdt():
    return -y() - z()


@component.add(
    name="dydt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"x": 1, "a": 1, "y": 1},
)
def dydt():
    return x() + a() * y()


@component.add(
    name="dzdt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"b": 1, "c": 1, "x": 1, "z": 1},
)
def dzdt():
    return b() + z() * (x() - c())


@component.add(
    name="x",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_x": 1},
    other_deps={"_integ_x": {"initial": {}, "step": {"dxdt": 1}}},
)
def x():
    return _integ_x()


_integ_x = Integ(lambda: dxdt(), lambda: 0.5, "_integ_x")


@component.add(
    name="y",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_y": 1},
    other_deps={"_integ_y": {"initial": {}, "step": {"dydt": 1}}},
)
def y():
    return _integ_y()


_integ_y = Integ(lambda: dydt(), lambda: 0.5, "_integ_y")


@component.add(
    name="z",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_z": 1},
    other_deps={"_integ_z": {"initial": {}, "step": {"dzdt": 1}}},
)
def z():
    return _integ_z()


_integ_z = Integ(lambda: dzdt(), lambda: 0.4, "_integ_z")

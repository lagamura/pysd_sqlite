"""
Python model 'First_Order_Delay.py'
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
    "time_step": lambda: 1,
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


@component.add(
    name="Input",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"test_input": 1},
)
def input_1():
    return test_input()


@component.add(name="test input", comp_type="Constant", comp_subtype="Normal")
def test_input():
    return 5


@component.add(name="Delay", comp_type="Constant", comp_subtype="Normal")
def delay():
    return 3


@component.add(
    name="Delay Buffer",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_delay_buffer": 1},
    other_deps={
        "_integ_delay_buffer": {
            "initial": {"input_1": 1, "delay": 1},
            "step": {"input_1": 1, "output": 1},
        }
    },
)
def delay_buffer():
    return _integ_delay_buffer()


_integ_delay_buffer = Integ(
    lambda: input_1() - output(), lambda: input_1() * delay(), "_integ_delay_buffer"
)


@component.add(
    name="Output",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"delay_buffer": 1, "delay": 1},
)
def output():
    return delay_buffer() / delay()

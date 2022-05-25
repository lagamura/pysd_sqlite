"""
Python model 'penny_jar.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import pulse
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
    "initial_time": lambda: 1930,
    "final_time": lambda: 2014,
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
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
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
    units="Year",
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
    name="Entering Circulation",
    units="Penny/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"post_production": 1, "entry_rate": 1},
)
def entering_circulation():
    return post_production() * entry_rate()


@component.add(
    name="Entry Rate",
    units="Penny/Penny/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def entry_rate():
    return 0.1


@component.add(
    name="In Circulation",
    units="Penny",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_in_circulation": 1},
    other_deps={
        "_integ_in_circulation": {
            "initial": {},
            "step": {"entering_circulation": 1, "loss": 1},
        }
    },
)
def in_circulation():
    return _integ_in_circulation()


_integ_in_circulation = Integ(
    lambda: entering_circulation() - loss(), lambda: 0, "_integ_in_circulation"
)


@component.add(
    name="Loss",
    units="Penny/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"in_circulation": 1, "loss_rate": 1},
)
def loss():
    return in_circulation() * loss_rate()


@component.add(
    name="Loss Rate",
    units="Penny/Penny/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def loss_rate():
    return 0.05


@component.add(
    name="Post Production",
    units="Penny",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_post_production": 1},
    other_deps={
        "_integ_post_production": {
            "initial": {},
            "step": {"production": 1, "entering_circulation": 1},
        }
    },
)
def post_production():
    return _integ_post_production()


_integ_post_production = Integ(
    lambda: production() - entering_circulation(), lambda: 0, "_integ_post_production"
)


@component.add(
    name="Production",
    units="Penny/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"production_year": 1, "time": 1, "production_volume": 1},
)
def production():
    return pulse(__data["time"], production_year(), width=1) * production_volume()


@component.add(
    name="Production Volume",
    units="Penny/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def production_volume():
    return 10000


@component.add(
    name="Production Year", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def production_year():
    return 1935

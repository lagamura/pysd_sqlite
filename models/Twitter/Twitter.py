"""
Python model 'Twitter.py'
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
    name="Displacement",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"posts_on_timeline": 1, "displacement_timescale": 1},
)
def displacement():
    return posts_on_timeline() / displacement_timescale()


@component.add(
    name="Displacement Timescale", comp_type="Constant", comp_subtype="Normal"
)
def displacement_timescale():
    return 3600


@component.add(
    name="Posts on Timeline",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_posts_on_timeline": 1},
    other_deps={
        "_integ_posts_on_timeline": {
            "initial": {},
            "step": {"tweeting": 1, "displacement": 1},
        }
    },
)
def posts_on_timeline():
    return _integ_posts_on_timeline()


_integ_posts_on_timeline = Integ(
    lambda: tweeting() - displacement(), lambda: 0, "_integ_posts_on_timeline"
)


@component.add(name="Tweeting", comp_type="Constant", comp_subtype="Normal")
def tweeting():
    return 4

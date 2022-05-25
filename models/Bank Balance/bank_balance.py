"""
Python model 'bank_balance.py'
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
    name="FINAL TIME", units="Day", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Day", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Day",
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
    units="Day",
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
    name="Balance",
    units="Dollars",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_balance": 1},
    other_deps={"_integ_balance": {"initial": {}, "step": {"income": 1}}},
)
def balance():
    return _integ_balance()


_integ_balance = Integ(lambda: income(), lambda: 100, "_integ_balance")


@component.add(
    name="Deposits", units="Dollars/Day", comp_type="Constant", comp_subtype="Normal"
)
def deposits():
    return 5


@component.add(
    name="Income",
    units="Dollars/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"deposits": 1, "interest": 1},
)
def income():
    return deposits() + interest()


@component.add(
    name="Interest",
    units="Dollars/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"balance": 1, "interest_rate": 1},
)
def interest():
    return balance() * interest_rate()


@component.add(
    name="Interest Rate",
    units="Dollars/Dollar/Day",
    comp_type="Constant",
    comp_subtype="Normal",
)
def interest_rate():
    return 0.001

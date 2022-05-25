"""
Python model 'SIR_Simple.py'
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
    "time_step": lambda: 0.5,
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
    name="cumulative cases",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_cases": 1},
    other_deps={"_integ_cumulative_cases": {"initial": {}, "step": {"report_case": 1}}},
)
def cumulative_cases():
    return _integ_cumulative_cases()


_integ_cumulative_cases = Integ(
    lambda: report_case(), lambda: 0, "_integ_cumulative_cases"
)


@component.add(
    name="report case",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infect": 1},
)
def report_case():
    return infect()


@component.add(
    name="infect",
    units="Persons/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "susceptible": 1,
        "total_population": 1,
        "infectious": 1,
        "contact_infectivity": 1,
    },
)
def infect():
    return susceptible() * (infectious() / total_population()) * contact_infectivity()


@component.add(
    name="contact infectivity",
    units="Persons/Persons/Day",
    comp_type="Constant",
    comp_subtype="Normal",
)
def contact_infectivity():
    """
    A joint parameter listing both how many people you contact, and how likely you are to give them the disease.
    """
    return 0.7


@component.add(
    name="recovery period", units="Days", comp_type="Constant", comp_subtype="Normal"
)
def recovery_period():
    """
    How long are you infectious for?
    """
    return 5


@component.add(
    name="infectious",
    units="Persons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious": 1},
    other_deps={
        "_integ_infectious": {"initial": {}, "step": {"infect": 1, "recover": 1}}
    },
)
def infectious():
    """
    The population with the disease, manifesting symptoms, and able to transmit it to other people.
    """
    return _integ_infectious()


_integ_infectious = Integ(lambda: infect() - recover(), lambda: 5, "_integ_infectious")


@component.add(
    name="recovered",
    units="Persons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_recovered": 1},
    other_deps={"_integ_recovered": {"initial": {}, "step": {"recover": 1}}},
)
def recovered():
    """
    These people have recovered from the disease. Yay! Nobody dies in this model.
    """
    return _integ_recovered()


_integ_recovered = Integ(lambda: recover(), lambda: 0, "_integ_recovered")


@component.add(
    name="recover",
    units="Persons/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious": 1, "recovery_period": 1},
)
def recover():
    return infectious() / recovery_period()


@component.add(
    name="susceptible",
    units="Persons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_susceptible": 1},
    other_deps={
        "_integ_susceptible": {
            "initial": {"total_population": 1},
            "step": {"infect": 1},
        }
    },
)
def susceptible():
    """
    The population that has not yet been infected.
    """
    return _integ_susceptible()


_integ_susceptible = Integ(
    lambda: -infect(), lambda: total_population(), "_integ_susceptible"
)


@component.add(
    name="total population",
    units="Persons",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_population():
    """
    This is just a simplification to make it easer to track how many folks there are without having to sum up all the stocks.
    """
    return 1000

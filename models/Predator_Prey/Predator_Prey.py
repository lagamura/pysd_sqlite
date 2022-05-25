"""
Python model 'Predator_Prey.py'
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
    "final_time": lambda: 50,
    "time_step": lambda: 0.015625,
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
    name="Prey Births",
    units="Prey/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"prey_fertility": 1, "prey_population": 1},
)
def prey_births():
    return prey_fertility() * prey_population()


@component.add(
    name="Predation Rate",
    units="Prey/Day/Prey/Predator",
    limits=(0.0, 0.0001, 1e-05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def predation_rate():
    return 0.0001


@component.add(
    name="Prey Deaths",
    units="Prey/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predation_rate": 1, "prey_population": 1, "predator_population": 1},
)
def prey_deaths():
    return predation_rate() * prey_population() * predator_population()


@component.add(
    name="Prey Fertility",
    units="Prey/Day/Prey",
    limits=(0.0, 10.0, 0.1),
    comp_type="Constant",
    comp_subtype="Normal",
)
def prey_fertility():
    return 2


@component.add(
    name="Prey Population",
    units="Prey",
    limits=(0.0, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_prey_population": 1},
    other_deps={
        "_integ_prey_population": {
            "initial": {},
            "step": {"prey_births": 1, "prey_deaths": 1},
        }
    },
)
def prey_population():
    return _integ_prey_population()


_integ_prey_population = Integ(
    lambda: prey_births() - prey_deaths(), lambda: 250, "_integ_prey_population"
)


@component.add(
    name="Predator Births",
    units="Predator/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "predator_food_driven_fertility": 1,
        "prey_population": 1,
        "predator_population": 1,
    },
)
def predator_births():
    return predator_food_driven_fertility() * prey_population() * predator_population()


@component.add(
    name="Predator Deaths",
    units="Predator/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predator_mortality": 1, "predator_population": 1},
)
def predator_deaths():
    return predator_mortality() * predator_population()


@component.add(
    name="Predator Food Driven Fertility",
    units="Predators/Day/Predator/Prey",
    limits=(0.0, 0.0001, 1e-06),
    comp_type="Constant",
    comp_subtype="Normal",
)
def predator_food_driven_fertility():
    return 0.001


@component.add(
    name="Predator Mortality",
    units="Predator/Day/Predator",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def predator_mortality():
    return 0.01


@component.add(
    name="Predator Population",
    units="Predators",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_predator_population": 1},
    other_deps={
        "_integ_predator_population": {
            "initial": {},
            "step": {"predator_births": 1, "predator_deaths": 1},
        }
    },
)
def predator_population():
    return _integ_predator_population()


_integ_predator_population = Integ(
    lambda: predator_births() - predator_deaths(),
    lambda: 100,
    "_integ_predator_population",
)

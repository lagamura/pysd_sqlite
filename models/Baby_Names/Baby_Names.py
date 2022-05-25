"""
Python model 'Baby_Names.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import incomplete
from pysd import Component

__pysd_version__ = "3.0.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1880,
    "final_time": lambda: 1013,
    "time_step": lambda: 0.0625,
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
    name="Adjusting Perceptions",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_prevalence": 1, "name_prevalence": 1},
)
def adjusting_perceptions():
    return incomplete(expected_prevalence(), name_prevalence())


@component.add(name="Adjustment Rate", comp_type="Constant", comp_subtype="Normal")
def adjustment_rate():
    return incomplete()


@component.add(name="All Births", comp_type="Constant", comp_subtype="Normal")
def all_births():
    return incomplete()


@component.add(name="All Deaths", comp_type="Constant", comp_subtype="Normal")
def all_deaths():
    return incomplete()


@component.add(
    name="Becoming Aware",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"name_prevalence": 1, "people_unaware_of_name": 1},
)
def becoming_aware():
    return incomplete(name_prevalence(), people_unaware_of_name())


@component.add(
    name="Christenings",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"people_aware_of_name": 1, "perception_of_name_freshness": 1},
)
def christenings():
    return incomplete(people_aware_of_name(), perception_of_name_freshness())


@component.add(
    name="Deaths",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"life_expectancy": 1, "name_prevalence": 1},
)
def deaths():
    return incomplete(life_expectancy(), name_prevalence())


@component.add(name="Expected Prevalence", comp_type="Constant", comp_subtype="Normal")
def expected_prevalence():
    return incomplete()


@component.add(name="Life Expectancy", comp_type="Constant", comp_subtype="Normal")
def life_expectancy():
    return incomplete()


@component.add(
    name="Name Prevalence",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"christenings": 1, "deaths": 1},
)
def name_prevalence():
    return incomplete(christenings(), -deaths())


@component.add(
    name="People Aware of Name",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"all_deaths": 1, "becoming_aware": 1},
)
def people_aware_of_name():
    return incomplete(-all_deaths(), becoming_aware())


@component.add(
    name="People Unaware of Name",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"all_births": 1, "becoming_aware": 1},
)
def people_unaware_of_name():
    return incomplete(all_births(), -becoming_aware())


@component.add(
    name="Perception of Name Freshness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adjusting_perceptions": 1},
)
def perception_of_name_freshness():
    return incomplete(adjusting_perceptions())

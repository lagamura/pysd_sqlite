"""
Python model 'SI Model.py'
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
    "final_time": lambda: 35,
    "time_step": lambda: 0.125,
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
    name="FINAL TIME", units="Week", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Week", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Week",
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
    units="Week",
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
    name="New Reported Cases",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infection_rate": 1},
)
def new_reported_cases():
    return infection_rate()


@component.add(
    name="Population Infected with Ebola",
    units="Persons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_population_infected_with_ebola": 1},
    other_deps={
        "_integ_population_infected_with_ebola": {
            "initial": {},
            "step": {"infection_rate": 1},
        }
    },
)
def population_infected_with_ebola():
    return _integ_population_infected_with_ebola()


_integ_population_infected_with_ebola = Integ(
    lambda: infection_rate(), lambda: 1, "_integ_population_infected_with_ebola"
)


@component.add(
    name="Population Susceptible to Ebola",
    units="Persons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_population_susceptible_to_ebola": 1},
    other_deps={
        "_integ_population_susceptible_to_ebola": {
            "initial": {"total_population": 1},
            "step": {"infection_rate": 1},
        }
    },
)
def population_susceptible_to_ebola():
    """
    The Population Susceptible to Ebola is the equal to the population susceptible prior to the onset of the disease less all of those that have contracted it. It is initialized to the Total Effective Population.
    """
    return _integ_population_susceptible_to_ebola()


_integ_population_susceptible_to_ebola = Integ(
    lambda: -infection_rate(),
    lambda: total_population(),
    "_integ_population_susceptible_to_ebola",
)


@component.add(
    name="Contact Frequency",
    units="Persons/Person/Week",
    comp_type="Constant",
    comp_subtype="Normal",
)
def contact_frequency():
    return 7


@component.add(
    name="Contacts Between Infected and Uninfected Persons",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "probability_of_contact_with_infected_person": 1,
        "susceptible_contacts": 1,
    },
)
def contacts_between_infected_and_uninfected_persons():
    return probability_of_contact_with_infected_person() * susceptible_contacts()


@component.add(
    name="Cumulative Reported Cases",
    units="Persons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_reported_cases": 1},
    other_deps={
        "_integ_cumulative_reported_cases": {
            "initial": {},
            "step": {"new_reported_cases": 1},
        }
    },
)
def cumulative_reported_cases():
    return _integ_cumulative_reported_cases()


_integ_cumulative_reported_cases = Integ(
    lambda: new_reported_cases(), lambda: 0, "_integ_cumulative_reported_cases"
)


@component.add(
    name="Infection Rate",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "contacts_between_infected_and_uninfected_persons": 1,
        "infectivity": 1,
    },
)
def infection_rate():
    """
    The infection rate is determined by the total number of contacts between infected and uninfected people each week (Contacts Between Infected and Uninfected Persons), and the probability that each such contact results in transmission from the infected to uninfected person (Infectivity).
    """
    return contacts_between_infected_and_uninfected_persons() * infectivity()


@component.add(
    name="Infectivity",
    units="Dmnl",
    limits=(-1.0, 1.0, 0.001),
    comp_type="Constant",
    comp_subtype="Normal",
)
def infectivity():
    return 0.05


@component.add(
    name="Probability of Contact with Infected Person",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_infected_with_ebola": 1, "total_population": 1},
)
def probability_of_contact_with_infected_person():
    return population_infected_with_ebola() / total_population()


@component.add(
    name="Susceptible Contacts",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contact_frequency": 1, "population_susceptible_to_ebola": 1},
)
def susceptible_contacts():
    return contact_frequency() * population_susceptible_to_ebola()


@component.add(
    name="Total Population",
    units="Persons",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_population():
    return 7150

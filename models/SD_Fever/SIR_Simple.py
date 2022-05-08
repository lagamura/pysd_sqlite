"""
Python model 'SIR_Simple.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ

__pysd_version__ = "2.2.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "cumulative cases": "cumulative_cases",
    "report case": "report_case",
    "infect": "infect",
    "contact infectivity": "contact_infectivity",
    "recovery period": "recovery_period",
    "infectious": "infectious",
    "recovered": "recovered",
    "recover": "recover",
    "susceptible": "susceptible",
    "total population": "total_population",
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

_dependencies = {
    "cumulative_cases": {"_integ_cumulative_cases": 1},
    "report_case": {"infect": 1},
    "infect": {
        "susceptible": 1,
        "infectious": 1,
        "total_population": 1,
        "contact_infectivity": 1,
    },
    "contact_infectivity": {},
    "recovery_period": {},
    "infectious": {"_integ_infectious": 1},
    "recovered": {"_integ_recovered": 1},
    "recover": {"infectious": 1, "recovery_period": 1},
    "susceptible": {"_integ_susceptible": 1},
    "total_population": {},
    "final_time": {},
    "initial_time": {},
    "saveper": {"time_step": 1},
    "time_step": {},
    "_integ_cumulative_cases": {"initial": {}, "step": {"report_case": 1}},
    "_integ_infectious": {"initial": {}, "step": {"infect": 1, "recover": 1}},
    "_integ_recovered": {"initial": {}, "step": {"recover": 1}},
    "_integ_susceptible": {"initial": {"total_population": 1}, "step": {"infect": 1}},
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 0.5,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 100
    Units: Day
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return __data["time"].final_time()


def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: Day
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return __data["time"].initial_time()


def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Day
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return __data["time"].saveper()


def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 0.5
    Units: Day
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return __data["time"].time_step()


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################


def cumulative_cases():
    """
    Real Name: cumulative cases
    Original Eqn: INTEG ( report case, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_cumulative_cases()


def report_case():
    """
    Real Name: report case
    Original Eqn: infect
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return infect()


def infect():
    """
    Real Name: infect
    Original Eqn: susceptible*(infectious/total population) * contact infectivity
    Units: Persons/Day
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return susceptible() * (infectious() / total_population()) * contact_infectivity()


def contact_infectivity():
    """
    Real Name: contact infectivity
    Original Eqn: 0.7
    Units: Persons/Persons/Day
    Limits: (None, None)
    Type: constant
    Subs: None

    A joint parameter listing both how many people you contact, and how likely
        you are to give them the disease.
    """
    return 0.7


def recovery_period():
    """
    Real Name: recovery period
    Original Eqn: 5
    Units: Days
    Limits: (None, None)
    Type: constant
    Subs: None

    How long are you infectious for?
    """
    return 5


def infectious():
    """
    Real Name: infectious
    Original Eqn: INTEG ( infect-recover, 5)
    Units: Persons
    Limits: (None, None)
    Type: component
    Subs: None

    The population with the disease, manifesting symptoms, and able to
        transmit it to other people.
    """
    return _integ_infectious()


def recovered():
    """
    Real Name: recovered
    Original Eqn: INTEG ( recover, 0)
    Units: Persons
    Limits: (None, None)
    Type: component
    Subs: None

    These people have recovered from the disease. Yay! Nobody dies in this
        model.
    """
    return _integ_recovered()


def recover():
    """
    Real Name: recover
    Original Eqn: infectious/recovery period
    Units: Persons/Day
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return infectious() / recovery_period()


def susceptible():
    """
    Real Name: susceptible
    Original Eqn: INTEG ( -infect, total population)
    Units: Persons
    Limits: (None, None)
    Type: component
    Subs: None

    The population that has not yet been infected.
    """
    return _integ_susceptible()


def total_population():
    """
    Real Name: total population
    Original Eqn: 1000
    Units: Persons
    Limits: (None, None)
    Type: constant
    Subs: None

    This is just a simplification to make it easer to track how many folks
        there are without having to sum up all the stocks.
    """
    return 1000


_integ_cumulative_cases = Integ(
    lambda: report_case(), lambda: 0, "_integ_cumulative_cases"
)


_integ_infectious = Integ(lambda: infect() - recover(), lambda: 5, "_integ_infectious")


_integ_recovered = Integ(lambda: recover(), lambda: 0, "_integ_recovered")


_integ_susceptible = Integ(
    lambda: -infect(), lambda: total_population(), "_integ_susceptible"
)

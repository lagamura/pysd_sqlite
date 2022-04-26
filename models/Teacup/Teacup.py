"""
Python model 'Teacup.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ

__pysd_version__ = "2.2.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "Characteristic Time": "characteristic_time",
    "Heat Loss to Room": "heat_loss_to_room",
    "Room Temperature": "room_temperature",
    "Teacup Temperature": "teacup_temperature",
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

_dependencies = {
    "characteristic_time": {},
    "heat_loss_to_room": {
        "teacup_temperature": 1,
        "room_temperature": 1,
        "characteristic_time": 1,
    },
    "room_temperature": {},
    "teacup_temperature": {"_integ_teacup_temperature": 1},
    "final_time": {},
    "initial_time": {},
    "saveper": {"time_step": 1},
    "time_step": {},
    "_integ_teacup_temperature": {"initial": {}, "step": {"heat_loss_to_room": 1}},
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 30,
    "time_step": lambda: 0.125,
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
    Original Eqn: 30
    Units: Minute
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
    Units: Minute
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
    Units: Minute
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return __data["time"].saveper()


def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 0.125
    Units: Minute
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return __data["time"].time_step()


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################


def characteristic_time():
    """
    Real Name: Characteristic Time
    Original Eqn: 10
    Units: Minutes
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 10


def heat_loss_to_room():
    """
    Real Name: Heat Loss to Room
    Original Eqn: (Teacup Temperature - Room Temperature) / Characteristic Time
    Units: Degrees/Minute
    Limits: (None, None)
    Type: component
    Subs: None

    This is the rate at which heat flows from the cup into the room. We can
        ignore it at this point.
    """
    return (teacup_temperature() - room_temperature()) / characteristic_time()


def room_temperature():
    """
    Real Name: Room Temperature
    Original Eqn: 70
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 70


def teacup_temperature():
    """
    Real Name: Teacup Temperature
    Original Eqn: INTEG ( -Heat Loss to Room, 180)
    Units: Degrees
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_teacup_temperature()


_integ_teacup_temperature = Integ(
    lambda: -heat_loss_to_room(), lambda: 180, "_integ_teacup_temperature"
)

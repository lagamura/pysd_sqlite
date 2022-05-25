"""
Python model 'Emails_in_2_fixed_categories.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import pulse
from pysd.py_backend.statefuls import DelayN, Integ
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


@component.add(name="Total Emails", comp_type="Constant", comp_subtype="Normal")
def total_emails():
    return 1000


@component.add(
    name="Easy Email Volume",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_emails": 1, "easy_fraction": 1},
)
def easy_email_volume():
    return total_emails() * easy_fraction()


@component.add(name="Easy Fraction", comp_type="Constant", comp_subtype="Normal")
def easy_fraction():
    return 0.5


@component.add(
    name="Easy Reply",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delayn_easy_reply": 1},
    other_deps={
        "_delayn_easy_reply": {
            "initial": {"easy_reply_time": 1},
            "step": {"easy_arrival": 1, "easy_reply_time": 1},
        }
    },
)
def easy_reply():
    return _delayn_easy_reply()


_delayn_easy_reply = DelayN(
    lambda: easy_arrival(),
    lambda: easy_reply_time(),
    lambda: 0,
    lambda: 1,
    time_step,
    "_delayn_easy_reply",
)


@component.add(
    name="Hard Email Volume",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_emails": 1, "easy_fraction": 1},
)
def hard_email_volume():
    return total_emails() * (1 - easy_fraction())


@component.add(
    name="Net Email Output",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"easy_reply": 1, "hard_reply": 1},
)
def net_email_output():
    return easy_reply() + hard_reply()


@component.add(name="Easy Reply Time", comp_type="Constant", comp_subtype="Normal")
def easy_reply_time():
    return 1


@component.add(
    name="Hard Reply",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delayn_hard_reply": 1},
    other_deps={
        "_delayn_hard_reply": {
            "initial": {"hard_reply_time": 1},
            "step": {"hard_arrival": 1, "hard_reply_time": 1},
        }
    },
)
def hard_reply():
    return _delayn_hard_reply()


_delayn_hard_reply = DelayN(
    lambda: hard_arrival(),
    lambda: hard_reply_time(),
    lambda: 0,
    lambda: 3,
    time_step,
    "_delayn_hard_reply",
)


@component.add(name="Hard Reply Time", comp_type="Constant", comp_subtype="Normal")
def hard_reply_time():
    return 4


@component.add(
    name="Easy Arrival",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"easy_email_volume": 1, "time_step": 2, "time": 1},
)
def easy_arrival():
    return (
        easy_email_volume() / time_step() * pulse(__data["time"], 0, width=time_step())
    )


@component.add(
    name="Hard Arrival",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hard_email_volume": 1, "time_step": 2, "time": 1},
)
def hard_arrival():
    return (
        hard_email_volume() / time_step() * pulse(__data["time"], 0, width=time_step())
    )


@component.add(
    name="Easy Emails",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_easy_emails": 1},
    other_deps={
        "_integ_easy_emails": {
            "initial": {},
            "step": {"easy_arrival": 1, "easy_reply": 1},
        }
    },
)
def easy_emails():
    return _integ_easy_emails()


_integ_easy_emails = Integ(
    lambda: easy_arrival() - easy_reply(), lambda: 0, "_integ_easy_emails"
)


@component.add(
    name="Hard Emails",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hard_emails": 1},
    other_deps={
        "_integ_hard_emails": {
            "initial": {},
            "step": {"hard_arrival": 1, "hard_reply": 1},
        }
    },
)
def hard_emails():
    return _integ_hard_emails()


_integ_hard_emails = Integ(
    lambda: hard_arrival() - hard_reply(), lambda: 0, "_integ_hard_emails"
)

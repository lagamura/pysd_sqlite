"""
Python model 'Rookies Demo Model.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.statefuls import Integ
from pysd.py_backend.lookups import HardcodedLookups
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
    "final_time": lambda: 150,
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
    name="Average Tenure",
    limits=(30.0, 300.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_tenure():
    return 35


@component.add(
    name="Departure",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"experts": 1, "average_tenure": 1},
)
def departure():
    return experts() / average_tenure()


@component.add(
    name="Effect of Pressure on Hiring",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_effect_of_pressure_on_hiring"},
)
def effect_of_pressure_on_hiring(x, final_subs=None):
    return _hardcodedlookup_effect_of_pressure_on_hiring(x, final_subs)


_hardcodedlookup_effect_of_pressure_on_hiring = HardcodedLookups(
    [-1.0, -0.25, 0.0, 0.5, 1.0, 2.0, 3.0],
    [0.0, 0.0, 2.5, 15.0, 20.0, 25.0, 25.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_effect_of_pressure_on_hiring",
)


@component.add(
    name="Expert Task Completion",
    units="Tasks/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"experthours_on_task_per_week": 1, "expert_time_per_task": 1},
)
def expert_task_completion():
    return experthours_on_task_per_week() / expert_time_per_task()


@component.add(
    name="Expert Time per Task",
    units="Person*Hours",
    comp_type="Constant",
    comp_subtype="Normal",
)
def expert_time_per_task():
    return 10


@component.add(
    name="Expert Workweek",
    units="Hours/Week",
    comp_type="Constant",
    comp_subtype="Normal",
)
def expert_workweek():
    return 40


@component.add(
    name='"Expert-Hours on Task per Week"',
    units="Person*Hours/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "experthours_worked_per_week": 1,
        "experthours_spent_on_rookie_supervision_per_week": 1,
    },
)
def experthours_on_task_per_week():
    return (
        experthours_worked_per_week()
        - experthours_spent_on_rookie_supervision_per_week()
    )


@component.add(
    name='"Expert-Hours Spent on Rookie Supervision per Week"',
    units="Hours*Person/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hours_of_supervision_required_per_rookie_per_week": 1, "rookies": 1},
)
def experthours_spent_on_rookie_supervision_per_week():
    return hours_of_supervision_required_per_rookie_per_week() * rookies()


@component.add(
    name='"Expert-Hours Worked per Week"',
    units="Hours*Person/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"experts": 1, "expert_workweek": 1},
)
def experthours_worked_per_week():
    return experts() * expert_workweek()


@component.add(
    name="Experts",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_experts": 1},
    other_deps={
        "_integ_experts": {"initial": {}, "step": {"maturation": 1, "departure": 1}}
    },
)
def experts():
    return _integ_experts()


_integ_experts = Integ(lambda: maturation() - departure(), lambda: 50, "_integ_experts")


@component.add(
    name="Hiring",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_to_hire": 1, "effect_of_pressure_on_hiring": 1},
)
def hiring():
    return effect_of_pressure_on_hiring(pressure_to_hire())


@component.add(
    name="Hours of Supervision Required per Rookie Per Week",
    units="Person*Hours/Person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hours_of_supervision_required_per_rookie_per_week():
    return 20


@component.add(
    name="Maturation",
    units="Persons/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rookies": 1, "maturation_time": 1},
)
def maturation():
    return rookies() / maturation_time()


@component.add(
    name="Maturation Time",
    units="Weeks",
    limits=(0.0, 80.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def maturation_time():
    return 15


@component.add(
    name="Pressure to Hire",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"task_backlog": 1, "target_backlog": 2},
)
def pressure_to_hire():
    return (task_backlog() - target_backlog()) / target_backlog()


@component.add(
    name="Rookie Task Completion",
    units="Tasks/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rookiehours_on_task_per_week": 1, "rookie_time_per_task": 1},
)
def rookie_task_completion():
    return rookiehours_on_task_per_week() / rookie_time_per_task()


@component.add(
    name="Rookie Time per Task",
    units="Person*Hours",
    comp_type="Constant",
    comp_subtype="Normal",
)
def rookie_time_per_task():
    return 30


@component.add(
    name="Rookie Workweek",
    units="Hours/Week",
    comp_type="Constant",
    comp_subtype="Normal",
)
def rookie_workweek():
    return 40


@component.add(
    name='"Rookie-Hours on Task per Week"',
    units="Person*Hours/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rookiehours_worked_per_week": 1},
)
def rookiehours_on_task_per_week():
    return rookiehours_worked_per_week()


@component.add(
    name='"Rookie-Hours Worked per Week"',
    units="Person Hours",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rookie_workweek": 1, "rookies": 1},
)
def rookiehours_worked_per_week():
    return rookie_workweek() * rookies()


@component.add(
    name="Rookies",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rookies": 1},
    other_deps={
        "_integ_rookies": {"initial": {}, "step": {"hiring": 1, "maturation": 1}}
    },
)
def rookies():
    return _integ_rookies()


_integ_rookies = Integ(lambda: hiring() - maturation(), lambda: 5, "_integ_rookies")


@component.add(name="Target Backlog", comp_type="Constant", comp_subtype="Normal")
def target_backlog():
    return 500


@component.add(
    name="Task Arrival", units="Tasks/Week", comp_type="Constant", comp_subtype="Normal"
)
def task_arrival():
    return 230


@component.add(
    name="Task Backlog",
    units="Tasks",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_task_backlog": 1},
    other_deps={
        "_integ_task_backlog": {
            "initial": {},
            "step": {"task_arrival": 1, "task_completion": 1},
        }
    },
)
def task_backlog():
    return _integ_task_backlog()


_integ_task_backlog = Integ(
    lambda: task_arrival() - task_completion(), lambda: 500, "_integ_task_backlog"
)


@component.add(
    name="Task Completion",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "expert_task_completion": 1,
        "rookie_task_completion": 1,
        "task_backlog": 1,
    },
)
def task_completion():
    return np.minimum(
        expert_task_completion() + rookie_task_completion(), task_backlog()
    )

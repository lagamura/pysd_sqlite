"""
Python model 'Capability Trap.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import step
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
    name="Influence of Work Pressure on Improvement Time",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_influence_of_work_pressure_on_improvement_time"
    },
)
def influence_of_work_pressure_on_improvement_time(x, final_subs=None):
    return _hardcodedlookup_influence_of_work_pressure_on_improvement_time(
        x, final_subs
    )


_hardcodedlookup_influence_of_work_pressure_on_improvement_time = HardcodedLookups(
    [0.0, 1.0, 1.5, 2.0, 5.0],
    [1.0, 1.0, 0.75, 0.25, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_influence_of_work_pressure_on_improvement_time",
)


@component.add(
    name="Investment in Capability",
    units="Widgets/Person Hour/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time_spend_on_improvement": 1,
        "capability_improvement_per_investment": 1,
    },
)
def investment_in_capability():
    return time_spend_on_improvement() * capability_improvement_per_investment()


@component.add(
    name="Capability Erosion",
    units="Widgets/Person Hour/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"capability": 1, "erosion_timescale": 1},
)
def capability_erosion():
    return capability() / erosion_timescale()


@component.add(
    name="Capability improvement per investment",
    units="Widgets/Person Hour/Person Hour",
    limits=(0.0, 5.0, 0.25),
    comp_type="Constant",
    comp_subtype="Normal",
)
def capability_improvement_per_investment():
    return 0.5


@component.add(
    name="Change in Pressure to Do Work",
    units="1/Weeks",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "stretch": 1,
        "pressure_to_do_work": 1,
        "work_harder_adjustment_time": 1,
    },
)
def change_in_pressure_to_do_work():
    return (stretch() - pressure_to_do_work()) / work_harder_adjustment_time()


@component.add(
    name="Change in Pressure to Improve Capability",
    units="1/Weeks",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "stretch": 1,
        "pressure_to_improve_capability": 1,
        "improve_capability_adjustment_time": 1,
        "exogenous_capability_pressure": 1,
    },
)
def change_in_pressure_to_improve_capability():
    return (
        stretch() - pressure_to_improve_capability()
    ) / improve_capability_adjustment_time() + exogenous_capability_pressure()


@component.add(
    name="Desired Performance",
    units="Widgets/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"performance_step": 1, "time": 1},
)
def desired_performance():
    return 3000 + step(__data["time"], performance_step(), 10)


@component.add(
    name="Erosion Timescale",
    units="Weeks",
    limits=(0.0, 50.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def erosion_timescale():
    return 20


@component.add(
    name="Exogenous Capability Pressure",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_step": 1, "time": 1},
)
def exogenous_capability_pressure():
    return step(__data["time"], pressure_step(), 10)


@component.add(
    name="Improve Capability Adjustment Time",
    units="Weeks",
    limits=(0.0, 50.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def improve_capability_adjustment_time():
    return 9


@component.add(
    name="Influence of Capability Pressure on Improvement Time",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_influence_of_capability_pressure_on_improvement_time"
    },
)
def influence_of_capability_pressure_on_improvement_time(x, final_subs=None):
    return _hardcodedlookup_influence_of_capability_pressure_on_improvement_time(
        x, final_subs
    )


_hardcodedlookup_influence_of_capability_pressure_on_improvement_time = (
    HardcodedLookups(
        [0.0, 0.5, 0.75, 1.0, 2.0, 5.0],
        [0.0, 0.0, 0.5, 1.0, 1.5, 1.5],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_influence_of_capability_pressure_on_improvement_time",
    )
)


@component.add(
    name="Influence of Pressure on Work Time",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_influence_of_pressure_on_work_time"},
)
def influence_of_pressure_on_work_time(x, final_subs=None):
    return _hardcodedlookup_influence_of_pressure_on_work_time(x, final_subs)


_hardcodedlookup_influence_of_pressure_on_work_time = HardcodedLookups(
    [0.0, 0.75, 1.0, 1.25, 2.0, 10.0],
    [0.75, 0.75, 1.0, 1.25, 1.5, 1.5],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_influence_of_pressure_on_work_time",
)


@component.add(
    name="Work Harder Adjustment Time",
    units="Weeks",
    comp_type="Constant",
    comp_subtype="Normal",
)
def work_harder_adjustment_time():
    return 3


@component.add(
    name="Pressure to Do Work",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pressure_to_do_work": 1},
    other_deps={
        "_integ_pressure_to_do_work": {
            "initial": {},
            "step": {"change_in_pressure_to_do_work": 1},
        }
    },
)
def pressure_to_do_work():
    return _integ_pressure_to_do_work()


_integ_pressure_to_do_work = Integ(
    lambda: change_in_pressure_to_do_work(), lambda: 1, "_integ_pressure_to_do_work"
)


@component.add(
    name="Maximum Work Time",
    units="Person Hours/Week",
    limits=(0.0, 100.0, 5.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def maximum_work_time():
    return 40


@component.add(
    name="Normal Time Spent on Improvement",
    units="Person Hours/Week",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_time_spent_on_improvement():
    return 10


@component.add(
    name="Normal Time Spent Working",
    units="Person Hours/Week",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_time_spent_working():
    return 30


@component.add(
    name="Performance Step",
    units="Widgets/Week",
    limits=(0.0, 1000.0, 50.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def performance_step():
    return 0


@component.add(
    name="Pressure Step",
    limits=(-0.05, 0.1, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def pressure_step():
    return 0


@component.add(
    name="Time Spend on Improvement",
    units="Person Hours/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_time_spent_on_improvement": 1,
        "influence_of_capability_pressure_on_improvement_time": 1,
        "pressure_to_improve_capability": 1,
        "pressure_to_do_work": 1,
        "influence_of_work_pressure_on_improvement_time": 1,
    },
)
def time_spend_on_improvement():
    return (
        normal_time_spent_on_improvement()
        * influence_of_capability_pressure_on_improvement_time(
            pressure_to_improve_capability()
        )
        * influence_of_work_pressure_on_improvement_time(pressure_to_do_work())
    )


@component.add(
    name="Pressure to Improve Capability",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pressure_to_improve_capability": 1},
    other_deps={
        "_integ_pressure_to_improve_capability": {
            "initial": {},
            "step": {"change_in_pressure_to_improve_capability": 1},
        }
    },
)
def pressure_to_improve_capability():
    return _integ_pressure_to_improve_capability()


_integ_pressure_to_improve_capability = Integ(
    lambda: change_in_pressure_to_improve_capability(),
    lambda: 1,
    "_integ_pressure_to_improve_capability",
)


@component.add(
    name="Stretch",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_performance": 1, "actual_performance": 1},
)
def stretch():
    return desired_performance() / actual_performance()


@component.add(
    name="Time Spent Working",
    units="Person Hours/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_time_spent_working": 1,
        "influence_of_pressure_on_work_time": 1,
        "pressure_to_do_work": 1,
        "maximum_work_time": 1,
        "time_spend_on_improvement": 1,
    },
)
def time_spent_working():
    """
    This formulation not quite correct, need to de-conflate the pressure to work from the time spent on improvement...
    """
    return np.minimum(
        normal_time_spent_working()
        * influence_of_pressure_on_work_time(pressure_to_do_work()),
        maximum_work_time() - time_spend_on_improvement(),
    )


@component.add(
    name="Actual Performance",
    units="Widgets/Week",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"capability": 1, "time_spent_working": 1},
)
def actual_performance():
    return capability() * time_spent_working()


@component.add(
    name="Capability",
    units="Widgets/Person Hour",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_capability": 1},
    other_deps={
        "_integ_capability": {
            "initial": {},
            "step": {"investment_in_capability": 1, "capability_erosion": 1},
        }
    },
)
def capability():
    return _integ_capability()


_integ_capability = Integ(
    lambda: investment_in_capability() - capability_erosion(),
    lambda: 100,
    "_integ_capability",
)

"""
Python model 'Double_Pendulum.py'
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
    "time_step": lambda: 0.0078125,
    "saveper": lambda: 0.1,
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
    name="FINAL TIME", units="Second", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Second", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Second",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Second",
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
    name="Change in Angular Velocity",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "acceleration_due_to_gravity": 2,
        "mass_of_pendulum": 2,
        "mass_of_pendulum2": 5,
        "angular_position": 5,
        "angular_position2": 4,
        "angular_velocity": 1,
        "length_of_pendulum2": 1,
        "angular_velocity2": 1,
        "length_of_pendulum": 2,
    },
)
def change_in_angular_velocity():
    """
    If anything is worth doing, it's worth doing well. This is not worth doing well.
    """
    return (
        acceleration_due_to_gravity()
        * (2 * mass_of_pendulum() + mass_of_pendulum2())
        * np.sin(angular_position())
        - mass_of_pendulum2()
        * acceleration_due_to_gravity()
        * np.sin(angular_position() - 2 * angular_position2())
        - 2
        * np.sin(angular_position() - angular_position2())
        * mass_of_pendulum2()
        * (
            angular_velocity2() ** 2 * length_of_pendulum2()
            + angular_velocity() ** 2
            * length_of_pendulum()
            * np.cos(angular_position() - angular_position2())
        )
    ) / (
        length_of_pendulum()
        * (
            2 * mass_of_pendulum()
            + mass_of_pendulum2()
            - mass_of_pendulum2()
            * np.cos(2 * angular_position() - 2 * angular_position2())
        )
    )


@component.add(
    name="Change in Angular Velocity2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "angular_position": 4,
        "angular_position2": 3,
        "angular_velocity": 1,
        "mass_of_pendulum2": 5,
        "mass_of_pendulum": 3,
        "length_of_pendulum": 1,
        "angular_velocity2": 1,
        "length_of_pendulum2": 2,
        "acceleration_due_to_gravity": 1,
    },
)
def change_in_angular_velocity2():
    return (
        2
        * np.sin(angular_position() - angular_position2())
        * (
            angular_velocity() ** 2
            * length_of_pendulum()
            * (mass_of_pendulum() + mass_of_pendulum2())
            + acceleration_due_to_gravity()
            * (mass_of_pendulum() + mass_of_pendulum2())
            * np.cos(angular_position())
            + angular_velocity2() ** 2
            * length_of_pendulum2()
            * mass_of_pendulum2()
            * np.cos(angular_position() - angular_position2())
        )
    ) / (
        length_of_pendulum2()
        * (
            2 * mass_of_pendulum()
            + mass_of_pendulum2()
            - mass_of_pendulum2()
            * np.cos(2 * angular_position() - 2 * angular_position2())
        )
    )


@component.add(
    name="Acceleration due to Gravity",
    units="Meters/Second/Second",
    comp_type="Constant",
    comp_subtype="Normal",
)
def acceleration_due_to_gravity():
    return -9.8


@component.add(
    name="Angular Position",
    units="radians",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_angular_position": 1},
    other_deps={
        "_integ_angular_position": {
            "initial": {},
            "step": {"change_in_angular_position": 1},
        }
    },
)
def angular_position():
    """
    Angle between the pendulum and vertical
    """
    return _integ_angular_position()


_integ_angular_position = Integ(
    lambda: change_in_angular_position(), lambda: 1, "_integ_angular_position"
)


@component.add(
    name="Angular Position2",
    units="radians",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_angular_position2": 1},
    other_deps={
        "_integ_angular_position2": {
            "initial": {},
            "step": {"change_in_angular_position2": 1},
        }
    },
)
def angular_position2():
    """
    http://www.myphysicslab.com/dbl_pendulum.html
    """
    return _integ_angular_position2()


_integ_angular_position2 = Integ(
    lambda: change_in_angular_position2(), lambda: 1, "_integ_angular_position2"
)


@component.add(
    name="Angular Velocity",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_angular_velocity": 1},
    other_deps={
        "_integ_angular_velocity": {
            "initial": {},
            "step": {"change_in_angular_velocity": 1},
        }
    },
)
def angular_velocity():
    return _integ_angular_velocity()


_integ_angular_velocity = Integ(
    lambda: change_in_angular_velocity(), lambda: 0, "_integ_angular_velocity"
)


@component.add(
    name="Angular Velocity2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_angular_velocity2": 1},
    other_deps={
        "_integ_angular_velocity2": {
            "initial": {},
            "step": {"change_in_angular_velocity2": 1},
        }
    },
)
def angular_velocity2():
    return _integ_angular_velocity2()


_integ_angular_velocity2 = Integ(
    lambda: change_in_angular_velocity2(), lambda: 0, "_integ_angular_velocity2"
)


@component.add(
    name="Change in Angular Position",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"angular_velocity": 1},
)
def change_in_angular_position():
    return angular_velocity()


@component.add(
    name="Change in Angular Position2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"angular_velocity2": 1},
)
def change_in_angular_position2():
    return angular_velocity2()


@component.add(
    name="Length of Pendulum",
    units="Meter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def length_of_pendulum():
    return 10


@component.add(
    name="Length of Pendulum2",
    units="Meter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def length_of_pendulum2():
    return 10


@component.add(
    name="Mass of Pendulum",
    units="Kilogram",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mass_of_pendulum():
    return 10


@component.add(
    name="Mass of Pendulum2",
    units="Kilogram",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mass_of_pendulum2():
    return 10

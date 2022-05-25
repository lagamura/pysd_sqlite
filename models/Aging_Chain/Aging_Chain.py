"""
Python model 'Aging_Chain.py'
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
    "initial_time": lambda: 2000,
    "final_time": lambda: 2010,
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
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
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
    units="Year",
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
    name="bday10", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_1": 1}
)
def bday10():
    return dec_1() / 10


@component.add(
    name="bday20", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_2": 1}
)
def bday20():
    return dec_2() / 10


@component.add(
    name="bday30", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_3": 1}
)
def bday30():
    return dec_3() / 10


@component.add(
    name="bday40", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_4": 1}
)
def bday40():
    return dec_4() / 10


@component.add(
    name="bday50", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_5": 1}
)
def bday50():
    return dec_5() / 10


@component.add(
    name="bday60", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_6": 1}
)
def bday60():
    return dec_6() / 10


@component.add(
    name="bday70", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_7": 1}
)
def bday70():
    return dec_7() / 10


@component.add(
    name="bday80", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"dec_8": 1}
)
def bday80():
    return dec_8() / 10


@component.add(name="births", comp_type="Constant", comp_subtype="Normal")
def births():
    return 0


@component.add(
    name="dec 1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_1": 1},
    other_deps={
        "_integ_dec_1": {
            "initial": {},
            "step": {"births": 1, "bday10": 1, "dec_1_loss": 1},
        }
    },
)
def dec_1():
    return _integ_dec_1()


_integ_dec_1 = Integ(
    lambda: births() - bday10() - dec_1_loss(), lambda: 10, "_integ_dec_1"
)


@component.add(
    name="dec 1 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_1": 1, "dec_1_loss_rate": 1},
)
def dec_1_loss():
    return dec_1() * dec_1_loss_rate()


@component.add(name="dec 1 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_1_loss_rate():
    return 0.05


@component.add(
    name="dec 2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_2": 1},
    other_deps={
        "_integ_dec_2": {
            "initial": {},
            "step": {"bday10": 1, "bday20": 1, "dec_2_loss": 1},
        }
    },
)
def dec_2():
    return _integ_dec_2()


_integ_dec_2 = Integ(
    lambda: bday10() - bday20() - dec_2_loss(), lambda: 10, "_integ_dec_2"
)


@component.add(
    name="dec 2 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_2": 1, "dec_2_loss_rate": 1},
)
def dec_2_loss():
    return dec_2() * dec_2_loss_rate()


@component.add(name="dec 2 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_2_loss_rate():
    return 0.05


@component.add(
    name="dec 3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_3": 1},
    other_deps={
        "_integ_dec_3": {
            "initial": {},
            "step": {"bday20": 1, "bday30": 1, "dec_3_loss": 1},
        }
    },
)
def dec_3():
    return _integ_dec_3()


_integ_dec_3 = Integ(
    lambda: bday20() - bday30() - dec_3_loss(), lambda: 10, "_integ_dec_3"
)


@component.add(
    name="dec 3 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_3": 1, "dec_3_loss_rate": 1},
)
def dec_3_loss():
    return dec_3() * dec_3_loss_rate()


@component.add(name="dec 3 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_3_loss_rate():
    return 0.05


@component.add(
    name="dec 4",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_4": 1},
    other_deps={
        "_integ_dec_4": {
            "initial": {},
            "step": {"bday30": 1, "bday40": 1, "dec_4_loss": 1},
        }
    },
)
def dec_4():
    return _integ_dec_4()


_integ_dec_4 = Integ(
    lambda: bday30() - bday40() - dec_4_loss(), lambda: 10, "_integ_dec_4"
)


@component.add(
    name="dec 4 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_4": 1, "dec_4_loss_rate": 1},
)
def dec_4_loss():
    return dec_4() * dec_4_loss_rate()


@component.add(name="dec 4 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_4_loss_rate():
    return 0.05


@component.add(
    name="dec 5",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_5": 1},
    other_deps={
        "_integ_dec_5": {
            "initial": {},
            "step": {"bday40": 1, "bday50": 1, "dec_5_loss": 1},
        }
    },
)
def dec_5():
    return _integ_dec_5()


_integ_dec_5 = Integ(
    lambda: bday40() - bday50() - dec_5_loss(), lambda: 10, "_integ_dec_5"
)


@component.add(
    name="dec 5 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_5": 1, "dec_5_loss_rate": 1},
)
def dec_5_loss():
    return dec_5() * dec_5_loss_rate()


@component.add(name="dec 5 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_5_loss_rate():
    return 0.05


@component.add(
    name="dec 6",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_6": 1},
    other_deps={
        "_integ_dec_6": {
            "initial": {},
            "step": {"bday50": 1, "bday60": 1, "dec_6_loss": 1},
        }
    },
)
def dec_6():
    return _integ_dec_6()


_integ_dec_6 = Integ(
    lambda: bday50() - bday60() - dec_6_loss(), lambda: 10, "_integ_dec_6"
)


@component.add(
    name="dec 6 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_6": 1, "dec_6_loss_rate": 1},
)
def dec_6_loss():
    return dec_6() * dec_6_loss_rate()


@component.add(name="dec 6 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_6_loss_rate():
    return 0.05


@component.add(
    name="dec 7",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_7": 1},
    other_deps={
        "_integ_dec_7": {
            "initial": {},
            "step": {"bday60": 1, "bday70": 1, "dec_7_loss": 1},
        }
    },
)
def dec_7():
    return _integ_dec_7()


_integ_dec_7 = Integ(
    lambda: bday60() - bday70() - dec_7_loss(), lambda: 10, "_integ_dec_7"
)


@component.add(
    name="dec 7 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_7": 1, "dec_7_loss_rate": 1},
)
def dec_7_loss():
    return dec_7() * dec_7_loss_rate()


@component.add(name="dec 7 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_7_loss_rate():
    return 0.05


@component.add(
    name="dec 8",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_8": 1},
    other_deps={
        "_integ_dec_8": {
            "initial": {},
            "step": {"bday70": 1, "bday80": 1, "dec_8_loss": 1},
        }
    },
)
def dec_8():
    return _integ_dec_8()


_integ_dec_8 = Integ(
    lambda: bday70() - bday80() - dec_8_loss(), lambda: 10, "_integ_dec_8"
)


@component.add(
    name="dec 8 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_8": 1, "dec_8_loss_rate": 1},
)
def dec_8_loss():
    return dec_8() * dec_8_loss_rate()


@component.add(name="dec 8 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_8_loss_rate():
    return 0.05


@component.add(name="dec 9 loss rate", comp_type="Constant", comp_subtype="Normal")
def dec_9_loss_rate():
    return 0.05


@component.add(
    name="dec 9",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dec_9": 1},
    other_deps={
        "_integ_dec_9": {"initial": {}, "step": {"bday80": 1, "dec_9_loss": 1}}
    },
)
def dec_9():
    return _integ_dec_9()


_integ_dec_9 = Integ(lambda: bday80() - dec_9_loss(), lambda: 10, "_integ_dec_9")


@component.add(
    name="dec 9 loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dec_9": 1, "dec_9_loss_rate": 1},
)
def dec_9_loss():
    return dec_9() * dec_9_loss_rate()

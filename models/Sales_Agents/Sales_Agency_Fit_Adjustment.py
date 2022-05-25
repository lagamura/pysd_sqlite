"""
Python model 'Sales_Agency_Fit_Adjustment.py'
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
    "final_time": lambda: 120,
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
    name="Good Fit Fraction", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def good_fit_fraction():
    return 0.2


@component.add(
    name="Good Fit Mean Tenure",
    units="Months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def good_fit_mean_tenure():
    return 48


@component.add(
    name="Good Fit Productivity",
    units="Sales/Agent/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def good_fit_productivity():
    return 1


@component.add(
    name="Gross Hiring Rate",
    units="Agents/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gross_hiring_rate():
    return 1


@component.add(
    name="Hiring Good Fit Agents",
    units="Agents/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"good_fit_fraction": 1, "gross_hiring_rate": 1},
)
def hiring_good_fit_agents():
    return good_fit_fraction() * gross_hiring_rate()


@component.add(
    name="Hiring Poor Fit Agents",
    units="Agents/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"good_fit_fraction": 1, "gross_hiring_rate": 1},
)
def hiring_poor_fit_agents():
    return (1 - good_fit_fraction()) * gross_hiring_rate()


@component.add(
    name="Poor Fit Mean Tenure",
    units="Months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def poor_fit_mean_tenure():
    return 6


@component.add(
    name="Poor Fit Productivity",
    units="Sales/Agent/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def poor_fit_productivity():
    return 0.5


@component.add(
    name="Sales Agents with Good Fit",
    units="Agents",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_sales_agents_with_good_fit": 1},
    other_deps={
        "_integ_sales_agents_with_good_fit": {
            "initial": {},
            "step": {"hiring_good_fit_agents": 1, "turnover_of_good_fit_agents": 1},
        }
    },
)
def sales_agents_with_good_fit():
    return _integ_sales_agents_with_good_fit()


_integ_sales_agents_with_good_fit = Integ(
    lambda: hiring_good_fit_agents() - turnover_of_good_fit_agents(),
    lambda: 0,
    "_integ_sales_agents_with_good_fit",
)


@component.add(
    name="Sales Agents with Poor Fit",
    units="Agents",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_sales_agents_with_poor_fit": 1},
    other_deps={
        "_integ_sales_agents_with_poor_fit": {
            "initial": {},
            "step": {"hiring_poor_fit_agents": 1, "turnover_of_poor_fit_agents": 1},
        }
    },
)
def sales_agents_with_poor_fit():
    return _integ_sales_agents_with_poor_fit()


_integ_sales_agents_with_poor_fit = Integ(
    lambda: hiring_poor_fit_agents() - turnover_of_poor_fit_agents(),
    lambda: 0,
    "_integ_sales_agents_with_poor_fit",
)


@component.add(
    name="Total Productivity",
    units="Sales/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "good_fit_productivity": 1,
        "sales_agents_with_good_fit": 1,
        "sales_agents_with_poor_fit": 1,
        "poor_fit_productivity": 1,
    },
)
def total_productivity():
    return (
        good_fit_productivity() * sales_agents_with_good_fit()
        + poor_fit_productivity() * sales_agents_with_poor_fit()
    )


@component.add(
    name="Turnover of Good Fit Agents",
    units="Agents/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sales_agents_with_good_fit": 1, "good_fit_mean_tenure": 1},
)
def turnover_of_good_fit_agents():
    return sales_agents_with_good_fit() / good_fit_mean_tenure()


@component.add(
    name="Turnover of Poor Fit Agents",
    units="Agents/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sales_agents_with_poor_fit": 1, "poor_fit_mean_tenure": 1},
)
def turnover_of_poor_fit_agents():
    return sales_agents_with_poor_fit() / poor_fit_mean_tenure()

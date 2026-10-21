#!/usr/bin/env python3
"""Clean-room audit of Somake Blood Cut overload and Iron's 3.16.3 API.
A binary method name does not establish overload dispatch or actual lifesteal.
"""
from somake_109_perk_method_probe import GateError

def survey_overload_family(base_methods,child_methods):
    raise GateError("overload dispatch contract has not yet been certified")

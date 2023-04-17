"""
This file contains code for using environmment variables.
"""

import os
from typing import Dict


class Config:
    """
    Class for storing environment variables as mapping.

    Input for constructor is of the form:
    {variable: help string of variable, ...}

    Then one can access with:

    config = Config({"a": "b"})

    config.a

    variable needs to be an environment variable.
    """

    def __init__(self, config_dict: Dict[str, str]) -> None:
        self.env_vars = {}
        for k, v in config_dict.items():
            self.env_vars[k] = os.environ.get(k)

    def __getattr__(self, var_name: str) -> str:
        return self.env_vars[var_name]

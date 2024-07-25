# -*- coding: utf-8 -*-
# Copyright © YodaPY 2024-present
#
# This file is part of tk-netgraph.
#
# tk-netgraph is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tk-netgraph is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with tk-netgraph. If not, see <https://www.gnu.org/licenses/>.

import os
import platform
import tkinter

from netgraph import __version__


def main() -> None:
    """Print netgraph info"""
    root = tkinter.Tk()
    tk_version = root.tk.call("info", "patchlevel")
    path = os.path.abspath(os.path.dirname(__file__))
    py_impl = platform.python_implementation()
    py_ver = platform.python_version()
    py_compiler = platform.python_compiler()
    plat_info = platform.uname()
    print(f"netgraph {__version__} at {path}")
    print(f"tkinter {tk_version}")
    try:
        import customtkinter

        print(f"customtkinter {customtkinter.__version__}")
    except ModuleNotFoundError:
        print("customtkinter is not installed")
    print(f"{py_impl}, {py_ver}, {py_compiler}")
    print(f"{plat_info.system} {plat_info.version} {plat_info.machine}\n")

    print(f"NETGRAPH_USE_CTK={os.environ.get('NETGRAPH_USE_CTK', '')}")

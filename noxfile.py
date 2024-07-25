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

import nox

SCRIPT_PATHS = [
    os.path.join(".", "netgraph"),
    "noxfile.py",
]


@nox.session()
def format_fix(session: nox.Session) -> None:
    session.install(".[dev.format]")
    session.run("python", "-m", "ruff", "format", *SCRIPT_PATHS)
    session.run("python", "-m", "ruff", "check", "--fix", *SCRIPT_PATHS)


@nox.session()
def slotscheck(session: nox.Session) -> None:
    session.install(".[dev.slotscheck]")
    session.run("python", "-m", "slotscheck", "-m", "netgraph")

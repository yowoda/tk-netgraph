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

from __future__ import annotations

import abc
import typing as t

if t.TYPE_CHECKING:
    import tkinter as tk

    from netgraph import NetCanvas


@t.runtime_checkable
class CanvasAware(t.Protocol):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def canvas(self) -> NetCanvas:
        """The canvas class"""

    @property
    @abc.abstractmethod
    def canvas_id(self) -> t.Union[str, int]:
        """The object's canvas ID"""


@t.runtime_checkable
class Draggable(t.Protocol):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def drag_data(self) -> tuple[int, int]:
        """The drag data of this component"""

    @abc.abstractmethod
    def on_click(self, event: tk.Event) -> None:
        """
        The event listener that is called when the component is clicked.
        Used to initialize the drag data.
        """

    @abc.abstractmethod
    def on_drag(self, event: tk.Event) -> None:
        """
        The event listener that is called when the component is dragged.
        Used to move the component on the canvas and modify the drag data.
        """

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
import functools
import tkinter as tk
import typing as t

if t.TYPE_CHECKING:
    from netgraph.api import CanvasNode, ObjectContainer
    from netgraph._types import CanvasObjectsLike

__all__: t.Sequence[str] = (
    "ActiveNode",
    "NetCanvas"
)

class ActiveNode(abc.ABC):
    __slots__: t.Sequence[str] = ()
    
    @property
    @abc.abstractmethod
    def node(self) -> CanvasNode:
        """
        The node object that is currently active. It's the node that was left-clicked and that started the dynamic edge
        """

    @property
    @abc.abstractmethod
    def edge_container(self) -> ObjectContainer:
        """
        The container that holds the dynamic edge lines
        """

class NetCanvas(abc.ABC, tk.Canvas):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def active_node(self) -> t.Optional[ActiveNode]:
        """
        The ActiveNode instance when a node was left-clicked. None if no dynamic edge exists
        """

    @abc.abstractmethod
    def start_dynamic_line(self, node: CanvasNode) -> None:
        """
        Creates a dynamic edge and sets the active_node attribute
        """

    @abc.abstractmethod
    def stop_dynamic_line(self) -> None:
        """
        Deletes the dynamic edge and sets the active_node attribute to None
        """
    
    @abc.abstractmethod
    def create_aa_border_circle(self, pos: tuple[int, int], radius: int, width: int) -> CanvasObjectsLike:
        """
        Creates an anti-aliased circle with a border
        """

    @abc.abstractmethod
    def create_aa_double_circle(self, pos: tuple[int, int], space: int, radius: int) -> CanvasObjectsLike:
        """
        Creates an anti-aliased circle with two borders
        """

    @functools.wraps(tk.Canvas.create_line)
    @abc.abstractmethod
    def create_aa_line(self, *args, **kwargs) -> CanvasObjectsLike:
        """
        Creates an anti-aliased line
        """
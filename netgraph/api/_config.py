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
from typing_extensions import Self

from netgraph.api import CanvasEdge, CanvasNode, DragMode, ObjectContainer

__all__: t.Sequence[str]  = ("EdgeTextConfig", "EdgeConfig", "NodeConfig", "NetConfig")


C = t.TypeVar("C")
T = t.TypeVar("T")

class ReactiveField(abc.ABC, t.Generic[C, T]):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def value(self) -> T:
        """The value of the field"""
    
    @value.setter
    @abc.abstractmethod
    def value(self, new_value: T) -> None:
        """Set the new  value of the field"""
    
    @property
    @abc.abstractmethod
    def observers(self) -> list[t.Callable[[T], None]]:
        """Returns a list of observers that are called once the field value changes"""
    
    @t.overload
    def __get__(self, instance: None, owner: type[C]) -> Self:
        ...

    @t.overload
    def __get__(self, instance: C, owner: type[C]) -> T:
        ...

    @t.no_type_check
    @abc.abstractmethod
    def __get__(self, instance, owner):
        ...

    @abc.abstractmethod
    def __set__(self, instance: C, value: T) -> None:
        ...
    
    @abc.abstractmethod
    def add_observer(self, instance: C, callback: t.Callable[[T], None]) -> None:
        """Add an observer to the field"""

@t.runtime_checkable
class EdgeTextConfig(t.Protocol):
    gap: int
    """The gap between the text and the edge line"""
    color: str
    """The color of the text"""

@t.runtime_checkable
class EdgeConfig(t.Protocol):
    factory: type[CanvasEdge]
    """
    The CanvasEdge implementation to use internally when an edge is created. 
    The factory class should inherit from the CanavsEdge interface
    """
    antialiased: bool
    """Whether to draw antialiased lines"""
    label_config: EdgeTextConfig
    """The EdgeTextConfig for the edge label text"""
    weight_config: EdgeTextConfig
    """The EdgeTextConfig for the weight text"""
    line_color: str
    """The line color of the edge"""
    line_width: float
    """The line width of the edge"""
    drag_mode: DragMode
    """The drag mode of the edge"""
    offset: int
    """The offset of the edge line's midpoint. """
    line_segments: int
    """The number of segments the edge line consists of."""

@t.runtime_checkable
class NodeConfig(t.Protocol):
    factory: type[CanvasNode]
    """
    The CanvasNode implementation to use internally when a node is created. 
    The factory class should inherit from the CanavsNode interface
    """
    antialiased: bool
    """Whether to draw antialiased circles"""
    enable_dragging: bool
    """Whether to allow dragging of the node"""
    label_color: str
    """The color of the label text"""

@t.runtime_checkable
class NetConfig(t.Protocol):
    enable_zoom: ReactiveField[NetConfig, bool]
    """Whether to allow zooming in on the graph"""
    zoom_in_limit: int
    """The maximum number of times (inclusive) you can zoom in"""
    zoom_out_limit: int
    """The maximum number of times (inclusive) you can zoom out"""
    edge_config: EdgeConfig
    """The edge configuration that is applied to all edges if not overriden in the `create_edge` method"""
    node_config: NodeConfig
    """The node configuration that is applied to all nodes if not overriden in the `create_node` method"""
    object_container: type[ObjectContainer]
    """The object container that is used to store the canvas representation of edges and nodes"""

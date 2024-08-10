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
import enum
import typing as t

from netgraph._traits import CanvasAware

if t.TYPE_CHECKING:
    from netgraph import NetManager
    from netgraph._types import CanvasObjectsLike
    from netgraph.api import CanvasNode, EdgeConfig, NetCanvas, ObjectContainer

__all__: t.Sequence[str] = ("DragMode", "CanvasEdge")


class DragMode(enum.Enum):
    DISABLED = 1
    """Dragging the edge does nothing"""
    COMPONENT_ONLY = 2
    """Dragging the edge drags the whole component that the edge is apart of"""
    ALL = 3
    """Dragging the edge drags the whole graph"""


class CanvasEdge(abc.ABC, CanvasAware):
    __slots__: t.Sequence[str] = ()

    @abc.abstractmethod
    def __init__(
        self,
        manager: NetManager,
        canvas: NetCanvas,
        nodes: tuple[CanvasNode, CanvasNode],
        label: str,
        weight: t.Optional[int],
        *,
        config: EdgeConfig,
        obj_container: type[ObjectContainer],
    ) -> None:
        """The constructor of the canvas object"""

    @property
    @abc.abstractmethod
    def manager(self) -> NetManager:
        """The NetManager instance"""

    @property
    @abc.abstractmethod
    def component_id(self) -> t.Optional[str]:
        """The tag of the component that the edge is apart of"""

    @component_id.setter
    @abc.abstractmethod
    def component_id(self, value: t.Optional[str]) -> None:
        """Sets the new component id of the edge"""

    @property
    @abc.abstractmethod
    def endpoints(self) -> tuple[CanvasNode, CanvasNode]:
        """The two vertices connected by the edge. The vertices will be the same if the edge is a loop"""

    @property
    @abc.abstractmethod
    def label(self) -> str:
        """The label of the edge. Returns an empty string if the edge has no label"""

    @property
    @abc.abstractmethod
    def weight(self) -> t.Optional[int]:
        """The weight of the edge. Returns None if the edge has no weight"""

    @property
    @abc.abstractmethod
    def obj_container(self) -> ObjectContainer:
        """The object container instance that holds canvas objects related to the edge and the edge itself"""

    @property
    @abc.abstractmethod
    def config(self) -> EdgeConfig:
        """The configuration for this edge"""

    @property
    @abc.abstractmethod
    def position(self) -> int:
        """
        The position of the edge in the set of edges between the two endpoints.
        The position will be calculated when the `create_edge` method is called.
        """

    @position.setter
    @abc.abstractmethod
    def position(self, value: int) -> None:
        """
        Set the position of the edge to `value`
        """

    @property
    @abc.abstractmethod
    def is_selfloop(self) -> bool:
        """Whether the edge connects the given node to itself"""

    @abc.abstractmethod
    def update(self) -> None:
        """Update the coordinates of the edge"""

    @abc.abstractmethod
    def draw(self) -> CanvasObjectsLike:
        """
        Draws the canvas objects that are needed for the edge onto the canvas.
        This method should be overriden if you want to change the edge display (e.g. display a dashed line)
        Important: yield all objects IDs that you receive when creating canvas objects
        """

    @abc.abstractmethod
    def render(self) -> None:
        """Render the edge and manage the object container"""

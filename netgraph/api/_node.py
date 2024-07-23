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

from netgraph._traits import CanvasAware

if t.TYPE_CHECKING:
    from netgraph import NetManager, NetCanvas, NodeConfig
    from netgraph.api._objects import ObjectContainer
    from netgraph.api._edge import CanvasEdge
    from netgraph._types import CanvasObjectsLike


class CanvasNode(abc.ABC, CanvasAware):
    __slots__: t.Sequence[str] = ()

    @abc.abstractmethod
    def __init__(
        self, 
        manager: NetManager, 
        canvas: NetCanvas, 
        label: str,
        *,
        config: NodeConfig,
        obj_container: type[ObjectContainer]#=_ObjectContainer
    ) -> None:
        """
        The constructor of the canvas object
        """

    @property
    @abc.abstractmethod
    def manager(self) -> NetManager:
        """
        The NetManager instance
        """

    @property
    @abc.abstractmethod
    def component_id(self) -> t.Optional[str]:
        """
        The tag of the component that the node is apart of
        """

    @property
    @abc.abstractmethod
    def label(self) -> str:
        """
        The label of the node. Returns an empty string if the node has no label.
        """

    @property
    @abc.abstractmethod
    def obj_container(self) -> ObjectContainer:
        """
        The object container instance that holds canvas objects related to the node and the node itself
        """

    @property
    @abc.abstractmethod
    def config(self) -> NodeConfig:
        """
        The configuration for this node
        """

    @property
    @abc.abstractmethod
    def edges(self) -> set[CanvasEdge]:
        """
        A list of edges that the node is apart of, which need to be updated when the node is dragged 
        """

    @abc.abstractmethod
    def get_center(self) -> tuple[float, float]:
        """
        Returns the center of the node
        """

    @abc.abstractmethod
    def draw(self, pos: tuple[int, int]) -> CanvasObjectsLike:
        """
        Draws the canvas objects that are needed for the node onto the canvas.
        This method should be overriden if you want to change the node display (e.g. display a rectangle instead of a circle)
        Important: yield all objects IDs that you receive when creating canvas objects
        """

    @abc.abstractmethod
    def render(self, pos: tuple[int, int]) -> None:
        """
        Render the node and manage the object container
        """
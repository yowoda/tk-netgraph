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
    from netgraph.api import CanvasEdge, CanvasNode, DragMode

__all__: t.Sequence[str] = ("EdgeTextConfig", "EdgeConfig", "NodeConfig", "NetConfig")


class EdgeTextConfig(abc.ABC):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def gap(self) -> int:
        """The distance between the text and the line"""

    @property
    @abc.abstractmethod
    def color(self) -> str:
        """The color of the text"""


class EdgeConfig(abc.ABC):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def factory(self) -> type[CanvasEdge]:
        """
        The class to instantiate when using the `create_edge` method of `NetManager`.
        The class must inherit from the `CanvasEdge` interface.
        """

    @property
    @abc.abstractmethod
    def antialiased(self) -> bool:
        """
        Whether to draw antialiased lines.
        If True, two lines are drawn, one with the given color and the given width and
        another with 33% of the color intensity and the given width + 0.5
        """

    @property
    @abc.abstractmethod
    def label_config(self) -> EdgeTextConfig:
        """The configuration for the positioning and appearance of the label"""

    @property
    @abc.abstractmethod
    def weight_config(self) -> EdgeTextConfig:
        """The configuration for the positioning and appearance of the weight"""

    @property
    @abc.abstractmethod
    def line_color(self) -> str:
        """The color of the line"""

    @property
    @abc.abstractmethod
    def line_segments(self) -> int:
        """
        The number of segments which make up the whole line.
        If the line is not smooth enough you may increase this number however beware that the performance might suffer
        """

    @property
    @abc.abstractmethod
    def line_width(self) -> float:
        """The width of the line"""

    @property
    @abc.abstractmethod
    def drag_mode(self) -> DragMode:
        """The drag mode of the edge"""

    @property
    @abc.abstractmethod
    def offset(self) -> int:
        """The offset of the edge and the gap to other edges which have the same endpoints"""


class NodeConfig(abc.ABC):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def factory(self) -> type[CanvasNode]:
        """
        The class to instantiate when using the `create_node` method of `NetManager`.
        The class must implement the `CanvasNode` interface.
        """

    @property
    @abc.abstractmethod
    def antialiased(self) -> bool:
        """Whether to draw antialiased circles"""

    @property
    @abc.abstractmethod
    def enable_dragging(self) -> bool:
        """Whether to allow dragging the node"""

    @property
    @abc.abstractmethod
    def label_color(self) -> str:
        """The color of the label"""


class NetConfig(abc.ABC):
    __slots__: t.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def enable_zoom(self) -> bool:
        """Whether to allow zooming on nodes and edges"""

    @property
    @abc.abstractmethod
    def edge_config(self) -> EdgeConfig:
        """The edge configuration that will be applied to all created edges unless overriden"""

    @property
    @abc.abstractmethod
    def node_config(self) -> NodeConfig:
        """The node configuration that will be applied to all created node unless overriden"""

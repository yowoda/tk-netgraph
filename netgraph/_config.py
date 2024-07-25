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

import typing as t

import attrs

from netgraph._edge import CanvasEdge as CanvasEdgeImpl
from netgraph._node import CanvasNode as CanvasNodeImpl
from netgraph._objects import _ObjectContainer as ObjectContainerImpl
from netgraph.api import _config, _edge

if t.TYPE_CHECKING:
    from netgraph.api import CanvasEdge, CanvasNode, ObjectContainer

__all__: t.Sequence[str] = ("NetConfig", "EdgeConfig", "NodeConfig", "EdgeTextConfig")


@attrs.define(slots=True)
class EdgeTextConfig(_config.EdgeTextConfig):
    gap: int = 0
    color: str = "black"


@attrs.define(slots=True)
class EdgeConfig(_config.EdgeConfig):
    factory: type[CanvasEdge] = CanvasEdgeImpl
    antialiased: bool = False
    label_config: _config.EdgeTextConfig = EdgeTextConfig(gap=20)
    weight_config: _config.EdgeTextConfig = EdgeTextConfig(gap=-20)
    line_color: str = "black"
    line_width: float = 1.5
    drag_mode: _edge.DragMode = _edge.DragMode.COMPONENT_ONLY
    offset: int = -150
    line_segments: int = 30


@attrs.define(slots=True)
class NodeConfig(_config.NodeConfig):
    factory: type[CanvasNode] = CanvasNodeImpl
    antialiased: bool = False
    enable_dragging: bool = True
    label_color: str = "black"


@attrs.define(slots=True)
class NetConfig(_config.NetConfig):
    enable_zoom: bool = True
    edge_config: _config.EdgeConfig = EdgeConfig()
    node_config: _config.NodeConfig = NodeConfig()
    object_container: ObjectContainer = ObjectContainerImpl

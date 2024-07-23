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

from dataclasses import dataclass
import typing as t

from netgraph.api import _config, _edge
from netgraph._node import CanvasNode as CanvasNodeImpl
from netgraph._edge import CanvasEdge as CanvasEdgeImpl

if t.TYPE_CHECKING:
    from netgraph.api._edge import CanvasEdge
    from netgraph.api._node import CanvasNode

__all__: t.Sequence[str] = (
    "NetConfig",
    "EdgeConfig",
    "NodeConfig",
    "EdgeTextConfig"
)

@dataclass
class EdgeTextConfig(_config.EdgeTextConfig):
    gap: int = 0
    color: str = "black"

@dataclass
class EdgeConfig(_config.EdgeConfig):
    factory: type[CanvasEdge] = CanvasEdgeImpl
    antialiased: bool = False
    label_config: EdgeTextConfig = EdgeTextConfig(gap=20)
    weight_config: EdgeTextConfig = EdgeTextConfig(gap=-20)
    line_color: str = "black"
    width: float = 1.5
    drag_mode: _edge.DragMode = _edge.DragMode.COMPONENT_ONLY
    offset: int = -150
    line_segments: int = 30

@dataclass
class NodeConfig(_config.NodeConfig):
    factory: type[CanvasNode] = CanvasNodeImpl
    antialiased: bool = True
    enable_dragging: bool = True
    label_color: str = "black"

@dataclass
class NetConfig(_config.NetConfig):
    enable_zoom: bool = True
    edge_config: EdgeConfig = EdgeConfig()
    node_config: NodeConfig = NodeConfig()
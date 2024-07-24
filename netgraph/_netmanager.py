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

import tkinter as tk
import typing as t

from netgraph import NetConfig
from netgraph.api import _node, _edge, _config

if t.TYPE_CHECKING:
    from netgraph.api  import NetCanvas

__all__: t.Sequence[str] = (
    "NetManager",
)

class _ComponentManager(dict[str, list[t.Union[_node.CanvasNode, _edge.CanvasEdge]]]):
    __slots__: t.Sequence[str] = ("_component_id")
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._component_id = 0

    def add_component(self) -> str:
        tag = f"component{self._component_id}"
        self._component_id += 1

        self[tag] = []

        return tag

class NetManager:
    __slots__: t.Sequence[str] = ("_canvas", "_config", "_component_manager", "_nodes")

    def __init__(self, canvas: NetCanvas, config: t.Optional[_config.NetConfig] = None) -> None:
        self._canvas = canvas

        self._config = config if config is not None else NetConfig()
        
        self._component_manager = _ComponentManager()

        self._canvas.bind("<MouseWheel>", self.zoom)

    def zoom(self, event: tk.Event) -> None:
        if not self._config.enable_zoom:
            return
        
        if (event.delta > 0):
            self._canvas.scale(tk.ALL, event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self._canvas.scale(tk.ALL, event.x, event.y, 0.9, 0.9)

    @property
    def component_manager(self) -> _ComponentManager:
        return self._component_manager

    @property
    def config(self) -> NetConfig:
        return self._config

    def create_node(self, label: str, config: t.Optional[_config.NodeConfig] = None) -> _node.CanvasNode:
        if config is None:
            config = self._config.node_config
            
        node = self._config.node_config.factory(
            self, self._canvas, label, config=config, obj_container=self._config.object_container
        )
        return node
    
    def create_edge(
        self, 
        nodes: tuple[_node.CanvasNode, _node.CanvasNode], 
        label: str, 
        weight: t.Optional[int]=None,
        config: t.Optional[_config.EdgeConfig] = None
    ) -> _edge.CanvasEdge:
        if config is None:
            config = self._config.edge_config
            
        edge = self._config.edge_config.factory(
            self, self._canvas, nodes, label,
            weight, config=config, obj_container=self._config.object_container
        )

        for node in nodes:
            node.edges.add(edge)

        existing_edges = nodes[0].edges.intersection(nodes[1].edges)
        edge.position = sum(1 for e in existing_edges if e.endpoints == nodes)

        return edge
        
    
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

from netgraph._objects import _convert_to_canvas_objects, _ObjectContainer
from netgraph.api import _node

if t.TYPE_CHECKING:
    import tkinter as tk

    from netgraph import NetManager
    from netgraph._types import CanvasObjectsLike
    from netgraph.api import CanvasEdge, NetCanvas, NodeConfig, ObjectContainer

__all__: t.Sequence[str] = ("CanvasNode",)


class CanvasNode(_node.CanvasNode):
    __slots__: t.Sequence[str] = (
        "_manager",
        "_canvas",
        "_label",
        "_component_id",
        "_obj_container",
        "_config",
        "_edges",
    )

    def __init__(
        self,
        manager: NetManager,
        canvas: NetCanvas,
        label: str,
        *,
        config: NodeConfig,
        obj_container: type[ObjectContainer] = _ObjectContainer,
    ) -> None:
        self._manager = manager
        self._canvas = canvas
        self._label = label

        self._component_id: t.Optional[str] = None
        self._config = config
        self._edges: set[CanvasEdge] = set()

        self._obj_container = obj_container(self._canvas, disabled=not self._config.enable_dragging)
        if self._config.enable_dragging:
            self._obj_container.bind("<B1-Motion>", self._update_edges)

        self._obj_container.bind("<Button-1>", self._create_edge)

    @property
    def manager(self) -> NetManager:
        return self._manager

    @property
    def component_id(self) -> t.Optional[str]:
        return self._component_id

    @component_id.setter
    def component_id(self, id_: t.Optional[str]) -> None:
        self._component_id = id_

    @property
    def label(self) -> str:
        return self._label

    @property
    def canvas(self) -> NetCanvas:
        return self._canvas

    @property
    def canvas_id(self) -> str:
        return t.cast(str, self._obj_container.canvas_id)

    @property
    def obj_container(self) -> ObjectContainer:
        return self._obj_container

    @property
    def config(self) -> NodeConfig:
        return self._config

    @property
    def edges(self) -> list[CanvasEdge]:
        return self._edges

    def get_center(self) -> tuple[float, float]:
        box = self._canvas.bbox(self.canvas_id)
        return (box[0] + box[2]) / 2, (box[1] + box[3]) / 2

    def _create_edge(self, event: tk.Event) -> None:
        if self._canvas.active_node is not None:
            edge = self._manager.create_edge(
                (self._canvas.active_node.node, self),
                "",
            )
            self._canvas.stop_dynamic_line()
            edge.render()

        else:
            self._canvas.start_dynamic_line(self)

    def _update_edges(self, event: tk.Event) -> None:
        for edge in self._edges:
            edge.update()

    def render(self, pos: tuple[int, int]) -> None:
        ids = self.draw(pos)
        objects = _convert_to_canvas_objects(self._canvas, ids)
        self._obj_container.add(*objects)

    def draw(self, pos: tuple[int, int]) -> CanvasObjectsLike:
        radius = 50
        if self._config.antialiased:
            yield from self._canvas.create_aa_double_circle(pos, 10, radius)
        else:
            yield from self._canvas.create_oval(
                pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius, fill=self._canvas.cget("bg")
            )

        yield self._canvas.create_text(pos, text=self._label, fill=self._config.label_color)

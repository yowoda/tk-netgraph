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

import functools
import os
import tkinter as tk
import typing as t

import attrs

from netgraph._objects import _convert_to_canvas_objects, _ObjectContainer
from netgraph._types import CanvasObjectsLike
from netgraph.api import ActiveNode as AbstractActiveNode
from netgraph.api import NetCanvas as AbstractNetCanvas
from netgraph._vendor.ctk_canvas import CTkCanvas

if t.TYPE_CHECKING:
    from netgraph._types import CanvasObjectsLike
    from netgraph.api._node import CanvasNode

__all__: t.Sequence[str] = ("NetCanvas",)

@attrs.define(slots=True, frozen=True)
class _ActiveNode(AbstractActiveNode):
    node: CanvasNode
    edge_container: _ObjectContainer


class NetCanvas(AbstractNetCanvas, CTkCanvas):
    __slots__: t.Sequence[str] = ("_active_node",)

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)

        self._active_node: t.Optional[_ActiveNode] = None

        self.tag_bind("all", "<Enter>", lambda _: self.config(cursor="hand2"))
        self.tag_bind("all", "<Leave>", lambda _: self.config(cursor=""))

    @property
    def active_node(self) -> t.Optional[_ActiveNode]:
        return self._active_node

    def _draw_dynamic_line(self, event: tk.Event) -> None:
        self._active_node = t.cast(_ActiveNode, self._active_node)
        self._active_node.edge_container.coords(*self._active_node.node.get_center(), event.x, event.y)

    def start_dynamic_line(self, node: CanvasNode) -> None:
        node_center = node.get_center()
        config = node.manager.config
        obj_container = config.object_container(self, disabled=True)
        create_line = self.create_aa_line if config.edge_config.antialiased else self.create_line

        ids = create_line(*node_center, *node_center, width=config.edge_config.line_width)
        objects = _convert_to_canvas_objects(self, ids)
        obj_container.add(*objects)
        obj_container.lower()

        self._active_node = _ActiveNode(node, obj_container)
        self.bind("<Motion>", self._draw_dynamic_line, "+")

    def stop_dynamic_line(self) -> None:
        if self._active_node is None:
            raise RuntimeError("'stop_dynamic_line' call must always follow a 'start_dynamic_line' call")

        self._active_node.edge_container.remove_all()
        self._active_node = None
        self.unbind("<Motion>")

    # Add consistent "yield from " to the current interface
    # Not sure if I like this, we will see

    @functools.wraps(tk.Canvas.create_oval)
    def create_oval(self, *args, **kwargs) -> CanvasObjectsLike:
        yield super().create_oval(*args, **kwargs)

    @functools.wraps(tk.Canvas.create_line)
    def create_line(self, *args, **kwargs) -> CanvasObjectsLike:
        yield super().create_line(*args, **kwargs)

    @functools.wraps(tk.Canvas.create_line)
    def create_aa_line(self, *args, **kwargs) -> CanvasObjectsLike:
        kwargs["fill"] = "#000"
        yield from self.create_line(*args, **kwargs)
        kwargs["fill"] = "#AAA"
        kwargs["width"] += 0.5
        yield from self.create_line(*args, **kwargs)

    def create_aa_border_circle(self, pos: tuple[int, int], radius: int, width: int) -> CanvasObjectsLike:
        yield self.create_aa_circle(*pos, radius, fill="black")
        yield self.create_aa_circle(*pos, radius - width, fill=self.cget("bg"))

    def create_aa_double_circle(self, pos: tuple[int, int], space: int, radius: int) -> CanvasObjectsLike:
        yield from self.create_aa_border_circle(pos, radius, 2)
        yield from self.create_aa_border_circle(pos, radius - space, 2)

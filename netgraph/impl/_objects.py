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

import itertools
import typing as t

from netgraph import _math
from netgraph.api import _objects

if t.TYPE_CHECKING:
    import tkinter as tk

    from netgraph.api import NetCanvas, CanvasEdge, EdgeTextConfig
    from netgraph._types import CanvasObjectsLike

__all__: t.Sequence[str] = ("CanvasObject", "CanvasEdgeTextObject")


class CanvasObject(_objects.CanvasObject):
    __slots__: t.Sequence[str] = ("_object_id", "_canvas")

    def __init__(self, id: int, canvas: NetCanvas) -> None:
        self._object_id = id
        self._canvas = canvas

    @property
    def canvas_id(self) -> int:
        return self._object_id

    @property
    def canvas(self) -> NetCanvas:
        return self._canvas

    def coords(self, *positions: float) -> None:
        self._canvas.coords(self._object_id, *positions)


class CanvasEdgeTextObject(CanvasObject):
    __slots__: t.Sequence[str] = ("_edge", "_config")

    def __init__(self, *args, edge: CanvasEdge, config: EdgeTextConfig, **kwargs) -> None:
        self._edge = edge
        self._config = config

        super().__init__(*args, **kwargs)

    def coords(self, *positions: float) -> None:
        if self._edge.is_selfloop:
            node = self._edge.endpoints[0]
            box = self._canvas.bbox(node.canvas_id)
            offset = abs(self._edge.config.offset) / 2 * self._edge.position
            x, y = _math._calc_selfloop_text_pos(box, offset)
            y -= self._config.gap

        else:
            pos1 = t.cast(tuple[float, float], positions[:2])
            pos2 = t.cast(tuple[float, float], positions[2:4])
            pos3 = t.cast(tuple[float, float], positions[4:6])
            distance = self._edge.config.offset * self._edge.position
            point = _math._calc_offset_point(pos2, pos1, pos3, distance / 2)
            x, y, angle = _math._calc_text_position(point, pos1, pos3, self._config.gap)
            self.canvas.itemconfig(self.canvas_id, angle=angle)

        self.canvas.coords(self.canvas_id, x, y)


class _ObjectContainer(_objects.ObjectContainer):
    """A container class that manages tkinter canvas objects using their object ID"""

    _id_iter = itertools.count()

    __slots__: t.Sequence[str] = ("_disabled", "_canvas", "_id", "_drag_x", "_drag_y", "_tags", "_objects")

    def __init__(self, canvas: NetCanvas, *, disabled: bool = False) -> None:
        self._canvas = canvas
        self._id = f"tag{next(self._id_iter)}"

        self._disabled = disabled
        self._tags: list[str] = [self._id]

        if self._disabled is False:
            self._create_drag_binds()

        self._objects: list[_objects.CanvasObject] = []

    @property
    def objects(self) -> list[_objects.CanvasObject]:
        return self._objects

    @property
    def tags(self) -> list[str]:
        return self._tags

    @property
    def canvas(self) -> NetCanvas:
        return self._canvas

    @property
    def canvas_id(self) -> str:
        return self._id

    def _create_drag_binds(self) -> None:
        self._canvas.tag_bind(self._id, "<ButtonPress-1>", self.on_click)
        self._canvas.tag_bind(self._id, "<B1-Motion>", self.on_drag)

    def _get_object_ids(self) -> tuple[int, ...]:
        return t.cast(tuple[int, ...], self._canvas.find_withtag(self._id))

    def add(self, *objects: _objects.CanvasObject) -> None:
        for obj in objects:
            for tag in self._tags:
                self._canvas.addtag_withtag(tag, obj.canvas_id)

        self._objects.extend(objects)

    def add_tag(self, tag: str) -> None:
        self._tags.append(tag)
        for object in self._get_object_ids():
            self._canvas.addtag_withtag(tag, object)

    def remove_tag(self, tag: str) -> None:
        self._tags.remove(tag)
        for object in self._get_object_ids():
            self._canvas.dtag(object, tag)

    def remove(self, *objects: _objects.CanvasObject) -> None:
        for obj in objects:
            self._canvas.dtag(obj.canvas_id, self._id)
            self._objects.remove(obj)

    def remove_all(self) -> None:
        self._canvas.delete(self._id)
        self._objects = []

    def coords(self, *positions: float) -> None:
        for obj in self._objects:
            obj.coords(*positions)

    def lower(self) -> None:
        for object in self._get_object_ids():
            self._canvas.tag_lower(object)

    def bind(self, event: str, callback: t.Callable[[tk.Event], None]) -> None:
        self._canvas.tag_bind(self._id, event, callback, "+")

    @property
    def drag_data(self) -> tuple[int, int]:
        return self._drag_x, self._drag_y

    def on_click(self, event: tk.Event) -> None:
        self._drag_x = event.x
        self._drag_y = event.y

    def on_drag(self, event: tk.Event) -> None:
        delta_x = event.x - self._drag_x
        delta_y = event.y - self._drag_y
        self._canvas.move(self._id, delta_x, delta_y)

        self._drag_x = event.x
        self._drag_y = event.y

        if self._canvas.active_node is not None:
            self._canvas.stop_dynamic_line()


def _convert_to_canvas_objects(canvas: NetCanvas, ids: CanvasObjectsLike) -> list[_objects.CanvasObject]:
    """Converts the given canvas IDs or objects to a CanvasObject instance"""
    objects: list[_objects.CanvasObject] = []

    for obj in ids:
        if isinstance(obj, _objects.CanvasObject):
            objects.append(obj)

        if isinstance(obj, int):
            objects.append(CanvasObject(obj, canvas))

    return objects

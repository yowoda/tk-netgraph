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

from netgraph import _math
from netgraph._objects import CanvasEdgeTextObject, _convert_to_canvas_objects, _ObjectContainer
from netgraph.api import _edge

if t.TYPE_CHECKING:
    from netgraph import NetManager
    from netgraph._types import CanvasObjectsLike
    from netgraph.api import CanvasNode, EdgeTextConfig, NetCanvas, _config, _objects

__all__: t.Sequence[str] = ("CanvasEdge",)


class CanvasEdge(_edge.CanvasEdge):
    __slots__: t.Sequence[str] = (
        "_manager",
        "_canvas",
        "_nodes",
        "_label",
        "_weight",
        "_obj_container",
        "_config",
        "_pan_data",
        "_component_id",
        "_position",
    )

    def __init__(
        self,
        manager: NetManager,
        canvas: NetCanvas,
        nodes: tuple[CanvasNode, CanvasNode],
        label: str,
        weight: t.Optional[int] = None,
        *,
        config: _config.EdgeConfig,
        obj_container: type[_objects.ObjectContainer] = _ObjectContainer,
    ) -> None:
        self._manager = manager
        self._canvas = canvas
        self._nodes = nodes
        self._label = label
        self._weight = weight

        self._config = config

        self._obj_container = obj_container(self._canvas, disabled=True)

        self._position = 0

        self._component_id: t.Optional[str] = None

        _node_comp_ids = [node.component_id for node in self._nodes]
        _new_objects: list[t.Union[CanvasNode, _edge.CanvasEdge]] = [self]

        # Logic to add edge and the given nodes to the graph component manager

        # Both nodes are part of different graph components
        # Choose one component and add the nodes and edges of the other component to the new one
        if (new_id := _node_comp_ids[0]) != (old_id := _node_comp_ids[1]) and all(_node_comp_ids):
            objs = self._manager.component_manager[old_id]
            for obj in objs:
                obj.obj_container.remove_tag(old_id)
            _new_objects.extend(objs)
            del self._manager.component_manager[old_id]

        # The first node is part of a component, the second one is a node not connected to any other nodes
        # Add the second node to the component of the first node
        elif (new_id := _node_comp_ids[0]) is not None and _node_comp_ids[1] is None:
            _new_objects.append(self._nodes[1])

        # The second node is part of a component, the first one is a node not connected to any other nodes
        # Add the first one to the component of the second node
        elif (new_id := _node_comp_ids[1]) is not None and _node_comp_ids[0] is None:
            _new_objects.append(self._nodes[0])

        # Both nodes are part of the same component
        elif any(_node_comp_ids):
            new_id = _node_comp_ids[0]

        # Neither of the nodes are part of a component
        # Create a new component
        else:
            new_id = self._manager.component_manager.add_component()
            _new_objects.extend(self._nodes)

        # Add all new objects to the component, the edge as well
        for object in _new_objects:
            object.component_id = new_id
            object.obj_container.add_tag(new_id)  # make sure the objects have an additional tag (the component id)
            # so you're able to select a specific component

        self._manager.component_manager[new_id].extend(_new_objects)

        self._canvas.tag_bind(self.canvas_id, "<Button-1>", self._drag_start, "+")
        self._canvas.tag_bind(self.canvas_id, "<B1-Motion>", self._drag, "+")

    @property
    def manager(self) -> NetManager:
        return self._manager

    @property
    def component_id(self) -> t.Optional[str]:
        return self._component_id

    @component_id.setter
    def component_id(self, id_: t.Optional[str]) -> None:
        self._component_id = id_

    def _drag_start(self, event: tk.Event) -> None:
        self._pan_data = (event.x, event.y)

    def _drag(self, event: tk.Event) -> None:
        delta_x = event.x - self._pan_data[0]
        delta_y = event.y - self._pan_data[1]

        if self._config.drag_mode is _edge.DragMode.COMPONENT_ONLY:
            self._canvas.move(self._component_id, delta_x, delta_y)

        elif self._config.drag_mode is _edge.DragMode.ALL:
            self._canvas.move(tk.ALL, delta_x, delta_y)

        self._pan_data = (event.x, event.y)

    @property
    def canvas(self) -> NetCanvas:
        return self._canvas

    @property
    def endpoints(self) -> tuple[CanvasNode, CanvasNode]:
        return self._nodes

    @property
    def label(self) -> str:
        return self._label

    @property
    def canvas_id(self) -> str:
        return t.cast(str, self._obj_container.canvas_id)

    @property
    def obj_container(self) -> _objects.ObjectContainer:
        return self._obj_container

    @property
    def config(self) -> _config.EdgeConfig:
        return self._config

    @property
    def weight(self) -> t.Optional[int]:
        return self._weight

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, pos: int) -> None:
        self._position = pos

    @property
    def is_selfloop(self) -> bool:
        return self._nodes[0] == self._nodes[1]

    def update(self) -> None:
        if self.is_selfloop:
            node = self._nodes[0]
            box = self._canvas.bbox(node.canvas_id)
            offset = abs(self._config.offset) / 2 * self._position
            points = _math._calc_selfloop_points(box, offset)

        else:
            node1_pos = self._nodes[0].get_center()
            node2_pos = self._nodes[1].get_center()

            distance = self._config.offset * self._position
            center_point = _math._calc_curved_center(node1_pos, node2_pos, distance)
            points = (*node1_pos, *center_point, *node2_pos)

        self._obj_container.coords(*points)

    def draw(self) -> CanvasObjectsLike:
        node1_pos = self._nodes[0].get_center()
        node2_pos = self._nodes[1].get_center()

        if self.is_selfloop:
            node = self._nodes[0]
            box = self._canvas.bbox(node.canvas_id)
            offset = abs(self._config.offset) / 2 * self._position
            points = _math._calc_selfloop_points(box, offset)
            x, y = _math._calc_selfloop_text_pos(box, offset)
            label_point = x, y - self._config.label_config.gap
            weight_point = x, y - self._config.weight_config.gap

        else:
            distance = self._config.offset * self._position
            center_point = _math._calc_curved_center(node1_pos, node2_pos, distance)

            # Smoothed out lines actually dont contain the given mid point
            # this has to be reversed so the label and weight are centered around the line correctly
            # calculate the mid point with 1/2 of the actual offset
            label_point = weight_point = _math._calc_offset_point(center_point, node1_pos, node2_pos, distance / 2)
            points = (*node1_pos, *center_point, *node2_pos)

        kw = {
            "fill": "#000",
            "width": self._config.line_width,
            "smooth": True,
            "splinesteps": self._config.line_segments,
        }

        create_line = self._canvas.create_aa_line if self._config.antialiased else self._canvas.create_line

        yield from create_line(*points, **kw)
        yield from self._draw_text(self._label, label_point, config=self._config.label_config)
        yield from self._draw_text(
            str(self._weight) if self._weight else "", weight_point, config=self._config.weight_config
        )

    def _draw_text(self, text: str, pos: tuple[float, float], *, config: EdgeTextConfig) -> CanvasObjectsLike:
        node1_pos = self._nodes[0].get_center()
        node2_pos = self._nodes[1].get_center()
        x, y, angle = (
            _math._calc_text_position(pos, node1_pos, node2_pos, config.gap) if self.is_selfloop is False else (*pos, 0)
        )
        yield CanvasEdgeTextObject(
            self._canvas.create_text(x, y, text=text, angle=angle, fill=config.color),
            self._canvas,
            edge=self,
            config=config,
        )

    def render(self) -> None:
        ids = self.draw()
        objects = _convert_to_canvas_objects(self._canvas, ids)
        self._obj_container.add(*objects)
        self._obj_container.lower()

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

import math
import typing as t

SELFLOOP_CENTER_Y_APPROX: t.Final[float] = 0.9375 # Factor to approximate the actual y coordinate of the center top point of the line

def _calc_text_position(text_pos, node1_pos: tuple[float, float], node2_pos: tuple[float, float], offset: float) -> tuple[float, float, float]:
    x0, y0 = node1_pos
    x1, y1 = node2_pos

    xside = x1 - x0
    yside = y1 - y0

    angle = math.degrees(math.atan2(yside, -xside))
    if abs(angle) > 90:
        angle = math.degrees(math.atan2(-yside, xside))

    point = _calc_offset_point(text_pos, node1_pos, node2_pos, offset)

    return *point, angle

def _calc_offset_point(pos: tuple[float, float], node1_pos: tuple[float, float], node2_pos: tuple[float, float], offset: float) -> tuple[float, float]:
    x0, y0 = node1_pos
    x1, y1 = node2_pos

    xside = x1 - x0
    yside = y1 - y0

    norm = math.hypot(xside, yside)
    ux, uy = xside / norm, yside / norm
    off_x, off_y = uy * offset, -ux * offset

    return pos[0] + off_x, pos[1] + off_y

def _calc_curved_center(node1_pos: tuple[float, float], node2_pos: tuple[float, float], offset: float):
    x0, y0 = node1_pos
    x1, y1 = node2_pos
    a = (x1 + x0)/2
    b = (y1 + y0)/2
    beta = (math.pi/2) - math.atan2((y1-y0), (x1-x0))

    xa = a - offset * math.cos(beta)
    ya = b + offset * math.sin(beta)
    return (xa, ya)

def _calc_selfloop_points(bbox: tuple[int, int, int, int], offset: float) -> tuple[int, ...]:
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2
    height = bbox[3] - bbox[1]
    # the self-loop edge line contains the following points
    x_offset = 30
    return (
        center_x-x_offset, center_y,
        center_x - offset, center_y - offset,
        center_x, center_y - offset - height * 0.25,
        center_x + offset, center_y - offset,
        center_x+x_offset, center_y
    )

def _calc_selfloop_text_pos(bbox: tuple[int, int, int, int], offset: float) -> tuple[int, int]:
    height = bbox[3] - bbox[1]
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2

    point = center_x, center_y - offset - height * 0.25 * SELFLOOP_CENTER_Y_APPROX
    return point
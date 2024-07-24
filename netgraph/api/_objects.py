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

from netgraph._traits import CanvasAware, Draggable

if t.TYPE_CHECKING:
    import tkinter as tk

    from netgraph.api import NetCanvas

__all__: t.Sequence[str] = (
    "CanvasObject",
    "ObjectContainer"
)

class CanvasObject(abc.ABC, CanvasAware):
    __slots__: t.Sequence[str] = ()

    @abc.abstractmethod
    def coords(self, *positions: float) -> None:
        """
        Change the coordinates of the object
        """

class ObjectContainer(abc.ABC, CanvasAware, Draggable):
    __slots__: t.Sequence[str] = ()

    @abc.abstractmethod
    def __init__(self, canvas: NetCanvas, *, disabled: bool=False) -> None:
        """
        The constructor of the object container
        """

    @property
    @abc.abstractmethod
    def objects(self) -> list[CanvasObject]:
        """
        The list of managed objects
        """

    @property
    @abc.abstractmethod
    def tags(self) -> list[str]:
        """
        A list of tags added to this container
        """

    @abc.abstractmethod
    def add(self, *objects: CanvasObject) -> None:
        """
        Adds the canvas object with the given ID to the container
        """

    @abc.abstractmethod
    def add_tag(self, tag: str) -> None:
        """
        Add the given tag to this container
        """

    @abc.abstractmethod
    def remove_tag(self, tag: str) -> None:
        """
        Remove the given tag from this container
        """

    @abc.abstractmethod
    def remove(self, *object_ids: CanvasObject) -> None:
        """
        Removes the canvas object with the given ID from the container
        """

    @abc.abstractmethod
    def coords(self, *positions: float) -> None:
        """
        Change the coordinates of all objects in the container
        """

    @abc.abstractmethod
    def lower(self) -> None:
        """
        Lower all objects in the stacking order
        """

    @abc.abstractmethod
    def bind(self, event: str, callback: t.Callable[[tk.Event], None]) -> None:
        """
        Bind a callback to the given event
        """
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

# pyright: reportIncompatibleMethodOverride=false

from __future__ import annotations

import inspect
import typing as t
from dataclasses import dataclass

from typing_extensions import Self, dataclass_transform

from netgraph._edge import CanvasEdge as CanvasEdgeImpl
from netgraph._node import CanvasNode as CanvasNodeImpl
from netgraph._objects import _ObjectContainer as ObjectContainerImpl
from netgraph.api import _edge, ObjectContainer

if t.TYPE_CHECKING:
    from netgraph.api import CanvasEdge, CanvasNode

__all__: t.Sequence[str] = ("NetConfig", "EdgeConfig", "NodeConfig", "EdgeTextConfig")

C = t.TypeVar("C")
T = t.TypeVar("T")

class ReactiveField(t.Generic[C, T]):
    __slots__: t.Sequence[str] = ("_value", "_observers")

    def __init__(self, value: T) -> None:
        self._value = value
        self._observers: list[t.Callable[[T], None]] = []

    @property
    def value(self) -> T:
        return self._value
    
    @value.setter
    def value(self, new_value: T) -> None:
        self._value = new_value
    
    @property
    def observers(self) -> list[t.Callable[[T], None]]:
        return self._observers
    
    @t.overload
    def __get__(self, instance: None, owner: type[C]) -> Self:
        ...

    @t.overload
    def __get__(self, instance: C, owner: type[C]) -> T:
        ...

    @t.no_type_check
    def __get__(self, instance, owner):
        ...

    def __set__(self, instance: C, value: T) -> None:
        ...
    
    def add_observer(self, instance: C, callback: t.Callable[[T], None]) -> None:
        ...

class _ReactiveWrapper:
    __slots__: t.Sequence[str] = ("_name", "_default")

    def __init__(self, name: str, default: t.Any) -> None:
        self._name = name
        self._default = default

    @t.no_type_check
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        return getattr(instance, self._name).value
    
    @t.no_type_check
    def __set__(self, instance, value):
        field = getattr(instance, self._name, None)
        if field is None:
            self._default = value
            return
        
        field.value = value
        for observer in field.observers:
            observer(value)

    @t.no_type_check
    def add_observer(self, instance, callback) -> None:
        getattr(instance, self._name).observers.append(callback)

_ClassT = t.TypeVar("_ClassT")
_ValueT = t.TypeVar("_ValueT")

def field(value: _ValueT) -> ReactiveField[t.Any, _ValueT]:
    return value  # pyright: ignore[reportReturnType]

@dataclass_transform(field_specifiers=(field,))
def reactive(cls: type[_ClassT]) -> type[_ClassT]:
    field_names: list[str] = []

    # Filter out the fields that are marked as reactive by their annotation
    annotations = t.get_type_hints(cls)
    for name, annotation in annotations.items():
        if getattr(annotation, "__origin__", None) is ReactiveField:
            field_names.append(name)

    # __post_init__ after dataclass initialization to set up reactive fields that are stored as private names

    @t.no_type_check
    def __post_init__(self) -> None:
        for name in field_names:
            attr = inspect.getattr_static(self, name)
            if not isinstance(attr, _ReactiveWrapper):
                setattr(self.__class__, name, _ReactiveWrapper(f"_{name}", attr))
            
            else:
                attr = attr._default
            
            reactive_field = ReactiveField(attr)
            setattr(self, f"_{name}", reactive_field)

    setattr(cls, "__post_init__", __post_init__)
    return cls

@dataclass
class EdgeTextConfig:
    gap: int = 0
    color: str = "black"


@dataclass
class EdgeConfig:
    factory: type[CanvasEdge] = CanvasEdgeImpl
    antialiased: bool = False
    label_config: EdgeTextConfig = EdgeTextConfig(gap=20)
    weight_config: EdgeTextConfig = EdgeTextConfig(gap=-20)
    line_color: str = "black"
    line_width: float = 1.5
    drag_mode: _edge.DragMode = _edge.DragMode.COMPONENT_ONLY
    offset: int = -150
    line_segments: int = 30


@dataclass
class NodeConfig:
    factory: type[CanvasNode] = CanvasNodeImpl
    antialiased: bool = False
    enable_dragging: bool = True
    label_color: str = "black"


@dataclass
@reactive
class NetConfig:
    enable_zoom: ReactiveField[Self, bool] = field(True)
    zoom_in_limit: int = 10
    zoom_out_limit: int = 10
    edge_config: EdgeConfig = EdgeConfig()
    node_config: NodeConfig = NodeConfig()
    object_container: type[ObjectContainer] = ObjectContainerImpl
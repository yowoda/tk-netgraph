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

import typing as t
from typing_extensions import ParamSpec, TypeAlias

if t.TYPE_CHECKING:
    from netgraph.api import CanvasObject

__all__: t.Sequence[str] = ("CanvasObjectsLike", "copy_signature")

CanvasObjectsLike: TypeAlias = "t.Generator[t.Union[int, CanvasObject], None, None]"

_P = ParamSpec("_P")
_OriginReturnT = t.TypeVar("_OriginReturnT")
_NewReturnT = t.TypeVar("_NewReturnT")

@t.overload
def copy_signature(
    origin: t.Callable[_P, _OriginReturnT], return_type: None=None
) -> t.Callable[[t.Callable[..., t.Any]], t.Callable[_P, _OriginReturnT]]:
    ...

@t.overload
def copy_signature(
    origin: t.Callable[_P, _OriginReturnT], return_type: type[_NewReturnT]
) -> t.Callable[[t.Callable[..., t.Any]], t.Callable[_P, _NewReturnT]]:
    ...

def copy_signature(
    origin: t.Callable[_P, _OriginReturnT], return_type: t.Optional[type[_NewReturnT]]=None
) -> t.Callable[[t.Callable[..., t.Any]], t.Callable[_P, t.Union[_NewReturnT, _OriginReturnT]]]:
    def inner(target: t.Callable[..., t.Any]) -> t.Callable[_P, t.Union[_OriginReturnT, _NewReturnT]]:
        if return_type is None:
            return t.cast(t.Callable[_P, _OriginReturnT], target)
        
        return t.cast(t.Callable[_P, _NewReturnT], target)
    
    return inner
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

# Nodes can be created by right-clicking anywhere
# Edges can be created by left-clicking on the respective nodes

import tkinter as tk

import netgraph

app = tk.Tk()
app.geometry("600x500")
canvas = netgraph.NetCanvas(app, highlightthickness=0)
canvas.pack(side="top", fill="both", expand=True)
net_manager = netgraph.NetManager(canvas)


def spawn_nodes(event):
    node = net_manager.create_node("MyNode")  # "MyNode" is the label of the node
    node.render((event.x, event.y))  # place the node at the mouse position


canvas.bind("<Button-3>", spawn_nodes)
app.mainloop()

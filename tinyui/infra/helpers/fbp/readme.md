# [WIP]FBP

A simple implementation of Flow-based programming in Python.

## Usage

```python
from blabla import demo_func
from fbp import (
    Node,
    Port,
    nodewrapper,
)


class SimpleNode(Node):
    input_ = Port("input", type_=str, role=["input"])
    output = Port("output", type_=str, tole=["output"])

    func = demo_func

```

## Components

This package provide several components:

- Port
- Node
- Graph
- Pipeline
- Runner

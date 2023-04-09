from typing import Any, Dict, Callable

from ..meta.node import NodeMeta


class Node(metaclass=NodeMeta):
    """Provide `Node`.

    Node is a container to warp a function.

    Here's demo:
    ```python
    def q(flow: PIL.Image, part: str) -> None:
        ...

    class SimpleNode(Node):
        flow = Port("flow", input=True, type=PIL.Image)
        part = Port("part", dependency=True, type=str)

        function = q

    simpleNode = SimpleNode()
    result = simpleNode(Image.create(...), "Blabla")
    ```
    """

    pass

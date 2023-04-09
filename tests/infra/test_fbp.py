import pytest
import typing as t
import pathlib as p, sys
sys.path.append(p.Path(p.Path(__file__).parent.parent.parent).__str__())
print(sys.path)

from tinyui.infrastructure.helpers.fbp.meta.node import NodeMeta
from tinyui.infrastructure.helpers.fbp.components.node import Node
from tinyui.infrastructure.helpers.fbp.components.port import Port


class TestPort:
    def test_singleton(self):
        a = Port("a", type_=int)
        b = Port("a", type_=t.Any)

        assert a == b
        assert b.t == int

    def test_value_typechecking(self):
        a = Port("a", type_=int)
        a.value = 1
        assert isinstance(a.value, int)

        b = Port("a", ...)
        b.t = str
        b.value = ""

    def test_port_update(self):
        pass


class TestNode:
    def test_node_abstract(self):

        class Node4Test(Node):
            __abstract__ = True

            input = Port("input", int | str)
            output = Port("output", int)


class TestPipe: ...


class TestConfig: ...


class TestRun: ...

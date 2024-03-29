import pytest
import typing as t
import pathlib as p

from chestnut.infra.helpers.fbp.meta.node import NodeMeta
from chestnut.infra.helpers.fbp.components.node import Node
from chestnut.infra.helpers.fbp.components.port import Port

class TestPort:
    def test_singleton(self):
        ...
        """
        a = Port("a", type_=int)
        b = Port("a", type_=t.Any)

        assert a == b
        assert b.t == int
        # """

    def test_value_typechecking(self):
        ...
        """
        a = Port("a", type_=int)
        a.value = 1
        assert isinstance(a.value, int)

        b = Port("a", type_=object)
        b.t = str
        b.value = ""
        # """

    def test_port_update(self):
        pass


class TestNode:
    def test_node_abstract(self):
        class Node4Test(Node):
            __abstract__ = True

            input = Port("input", type_=int | str, role=None)
            output = Port("output", type_=int, role=None)


class TestPipe:
    ...
    def test_oprator(self):
        class A(Node): ...
        class B(Node): ...

        a = A()
        b = B()

        x = a >> b >> a

        ...


class TestConfig:
    ...


class TestRun:
    ...

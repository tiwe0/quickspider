#!/usr/bin/env python3
from quickspider.core.Node import BaseNode
from quickspider.core.nodes import *
from collections import deque

class Builder:
    node_class = {
            "basenode": BaseNode,
            "getnode": GetNode,
            "postnode": PostNode,
            "pagenode": PageNode,
            "parsernode": ParserNode,
            "parserdomnode": ParserDomNode,
            "parserjsonnode": ParserJsonNode,
            "extractnode": ExtractNode,
            "concatnode": ConcatNode,
            "csvreadernode": CsvReaderNode,
            "excelreadernode": ExcelReaderNode,
            "linereadernode": LineReaderNode,
            "jsonwriternode": JsonWriterNode
            }
    def __init__(self):
        self._nodes = deque()

    def _add_node(self, _node):
        self._nodes.append(_node)

    def node_build(self, _name, _config):
        node_class_name = _config.pop("type").lower()
        node_class = Builder.get_class_from_name(node_class_name)
        config = {f"_{k}": v for k, v in _config.items()}
        name = _name.split(".")[-1]
        node = node_class(_name=name, **config)
        self._add_node(node)
        return node

    def link(self):
        header = BaseNode("header")
        node = header
        while self._nodes:
            next_node = self._nodes.popleft()
            node = node.add_child(next_node)
        return header

    @staticmethod
    def get_class_from_name(node_class_name):
        return Builder.node_class.get(node_class_name, BaseNode)


if __name__ == "__main__":
    b = Builder()

from quickspider.core.Node import BaseNode, IterableNode
from scrapy import Selector
from requests import Session
from termcolor import colored
import pandas as pd
import json
import os
s = Session()
s.headers = {"User-Agent": "Google-Bot"}


#-------------> 网络节点 <--------------
class SessionNode(BaseNode):
    def __init__(self, _name, _session=s):
        super().__init__(_name)
        self._session = _session


class GetNode(SessionNode):
    def process_input(self, _input_url):
        try:
            resp = self._session.get(_input_url)
        except Exception as e:
            print(e)
            resp = None
        return resp


class PostNode(SessionNode):
    def _set_data(self, data: dict):
        self._data = data

    def process_input(self, _input_url):
        try:
            resp = self._session.post(_input_url, json=self._data)
        except Exception as e:
            print(e)
            resp = None
        return resp


#-------------> 解析节点 <--------------
class ParserNode(BaseNode):
    def __init__(self, _name, _mode):
        super().__init__(_name)
        self._set_mode(_mode)

    def _set_mode(self, _mode="dom"):
        self._mode = _mode

    def process_input(self, _response):
        if self._mode == "dom":
            return Selector(text=_response.text)
        if self._mode == "json":
            return _response.json()


class ParserDomNode(BaseNode):
    def __init__(self, _name, _mode="css", _parser=""):
        super().__init__(_name)
        self._set_mode(_mode)
        self._set_parser(_parser)

    def _set_mode(self, _mode="css"):
        self._mode = _mode

    def _set_parser(self, _parser):
        self._parser = _parser

    def process_input(self, _response):
        selector = _response
        if self._mode == "css":
            result = selector.css(self._parser)
        elif self._mode == "xpath":
            result = selector.xpath(self._parser)
        return result


class ParserJsonNode(BaseNode):
    pass


#-------------> 组合节点 <--------------
class ExtractNode(IterableNode):
    def process_input(self, _input_parser):
        result = _input_parser.getall()
        return (colored(i, "green") for i in result)


class ConcatNode(BaseNode):
    def process_input(self, _input_parser):
        result = "".join(_input_parser.getall())
        return result


#-------------> 输出测试节点 <--------------
class PrintNode(BaseNode):
    def process_input(self, _input):
        print(_input)
        return _input


class PageNode(IterableNode):
    def __init__(self, _name, _input, _start, _stop, _step=1):
        super().__init__(_name)
        self._set_input(_input)
        self._info = (_start, _stop, _step)

    def process_input(self, _input):
        _start, _stop, _step = self._info
        return (_input.format(page=p) for p in range(_start, _stop, _step))


#-------------> 读写节点 <--------------
FileReaderNode = IterableNode

class CsvReaderNode(FileReaderNode):
    def __init__(self, _name, _file, _column):
        super().__init__(_name)
        self._set_input(_file)
        self._column = _column

    def process_input(self, _input):
        df = pd.read_csv(_input)
        for item in df[self._column]:
            yield item


class ExcelReaderNode(FileReaderNode):
    def __init__(self, _name, _file, _column):
        super().__init__(_name)
        self._set_input(_file)
        self._column = _column

    def process_input(self, _input):
        df = pd.read_excel(_input)
        for item in df[self._column]:
            yield item


class LineReaderNode(FileReaderNode):
    def __init__(self, _name, _file):
        super().__init__(_name)
        self._set_input(_file)

    def process_input(self, _input):
        with open(_input, "rt", encoding="utf8") as f:
            for line in f:
                yield line


class JsonWriterNode(BaseNode):
    def __init__(self, _name, _file):
        super().__init__(_name)
        self._file = _file
        self._container = []

    def init(self):
        if os.path.exists(self._file):
            os.remove(self._file)

    def process_input(self, _input):
        self._container.append(_input)
        return _input

    def post(self):
        with open(self._file, "wt", encoding="utf8") as f:
            json.dump(self._container, f)


if __name__ == "__main__":
    header = BaseNode("header")
    url_gen = PageNode("url", "http://quotes.toscrape.com/page/{page}/", 1, 6)
    getnode = GetNode("Geter")
    parsernode= ParserNode("parser", "dom")
    parserdomnode = ParserDomNode("parserdomnode" ,"css", "span.text::text")
    extractnode = ExtractNode("extract_node")

    header._add_child(url_gen)
    url_gen._add_child(getnode)
    getnode._add_child(parsernode)
    parsernode._add_child(parserdomnode)
    parserdomnode._add_child(extractnode)

    from controller import Controller
    c = Controller(header)
    c.start()

# coding=utf-8

from bs4 import BeautifulSoup
from bs4 import Tag
from bcy import BcyException
from bcy import PythonNode

# html node
class PythonNode(object):

    def __init__(self, node=None):
        if node is None:
            self.node = BeautifulSoup("<html></html>", "html.parser")
        elif isinstance(node, BeautifulSoup):
            self.node = node
        elif isinstance(node, str):
            self.node = BeautifulSoup(node, "html.parser")
        elif isinstance(node, Tag):
            self.node = BeautifulSoup(str(node), "html.parser")
        else:
            raise BcyException("Unsupported data types")

    # 第一个标签
    def fristNode(self) -> PythonNode:
        return PythonNode(self.fristTag())

    # 最后一个标签
    def lastNode(self) -> PythonNode:
        return PythonNode(self.lastTag())

    # 第一个标签
    def fristTag(self, cssQuery=None) -> Tag:
        ts = self.tags(cssQuery)
        if ts is not None and len(ts) > 0:
            return ts[0]
        return None

    # 最后一个标签
    def lastTag(self, cssQuery=None) -> Tag:
        ts = self.tags(cssQuery)
        if ts is not None and len(ts) > 0:
            return ts[len(ts) - 1]
        return None

    # 标签列表
    def tags(self, cssQuery=None) -> list:
        if self.node is None:
            return None
        if cssQuery is None:
            return self.node.contents
        return self.node.select(cssQuery)

    def tag(self, cssQuery=None, position=0) -> Tag:
        ta = self.tags(cssQuery)
        if ta is not None and len(ta) > position:
            return ta[position]
        return None

    # 标签的html
    def html(self, cssQuery=None, position=0) -> str:
        if self.node is None:
            return ""
        if cssQuery is None:
            return str(self.node)
        else:
            select = self.node.select(cssQuery)
            if select is not None and len(select) > position:
                return str(select[position].node)
        return ""

    # 标签的文字内容
    def text(self, cssQuery=None, position=0) -> str:
        if self.node is None:
            return ""
        if cssQuery is None:
            return str(self.node.text)
        else:
            select = self.node.select(cssQuery)
            if select is not None and len(select) > position:
                return str(select[position].text)
        return ""

    # 标签属性
    def attr(self, attr, cssQuery=None, position=0) -> str:
        if self.node is None:
            return ""
        ta = self.tags(cssQuery)
        if ta is not None and len(ta) > position:
            return ta[position].attrs.get(attr)
        return None

    def list(self, cssQuery=None) -> list:
        lis = self.tags(cssQuery)
        if lis is None:
            return None
        newLis = []
        for li in lis:
            newLis.append(PythonNode(li))
        return newLis

    def href(self, cssQuery=None, position=0) -> str:
        return self.attr("href",cssQuery,position)

    def src(self, cssQuery=None, position=0) -> str:
        return self.attr("src", cssQuery, position)

    def img(self, position=0) -> PythonNode:
        ta = self.tag("img", position)
        if ta is None:
            return None
        return PythonNode(ta)

    def a(self, position=0) -> PythonNode:
        ta = self.tag("a", position)
        if ta is None:
            return None
        return PythonNode(ta)

    def __str__(self):
        return self.html()
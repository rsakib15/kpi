from collections import defaultdict
import re


class TreeNode(object):
    def __init__(self, text, offset, elements=None):
        self.text = text
        self.offset = offset
        self.elements = elements or []

    def __iter__(self):
        for el in self.elements:
            yield el


class TreeNode1(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode1, self).__init__(text, offset, elements)
        self.andexp = elements[0]


class TreeNode2(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode2, self).__init__(text, offset, elements)
        self.expr = elements[3]
        self.andexp = elements[3]


class TreeNode3(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode3, self).__init__(text, offset, elements)
        self.groupexp = elements[0]


class TreeNode4(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode4, self).__init__(text, offset, elements)
        self.expr = elements[3]
        self.groupexp = elements[3]


class TreeNode5(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode5, self).__init__(text, offset, elements)
        self.exp = elements[2]


class TreeNode6(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode6, self).__init__(text, offset, elements)
        self.exp = elements[2]


class TreeNode7(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode7, self).__init__(text, offset, elements)
        self.field = elements[0]
        self.value = elements[1]


class TreeNode8(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode8, self).__init__(text, offset, elements)
        self.name = elements[0]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[^\\s():]')
    REGEX_2 = re.compile('^[^"]')
    REGEX_3 = re.compile('^[^\']')
    REGEX_4 = re.compile('^[a-zA-Z_]')
    REGEX_5 = re.compile('^[a-zA-Z0-9\\-_]')
    REGEX_6 = re.compile('^[\\s]')

    def _read_query(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['query'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        remaining0, index2, elements1, address2 = 0, self._offset, [], True
        while address2 is not FAILURE:
            address2 = self._read__()
            if address2 is not FAILURE:
                elements1.append(address2)
                remaining0 -= 1
        if remaining0 <= 0:
            address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
            self._offset = self._offset
        else:
            address1 = FAILURE
        if address1 is not FAILURE:
            elements0.append(address1)
            address3 = FAILURE
            index3 = self._offset
            address3 = self._read_exp()
            if address3 is FAILURE:
                address3 = TreeNode(self._input[index3:index3], index3)
                self._offset = index3
            if address3 is not FAILURE:
                elements0.append(address3)
                address4 = FAILURE
                remaining1, index4, elements2, address5 = 0, self._offset, [], True
                while address5 is not FAILURE:
                    address5 = self._read__()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        remaining1 -= 1
                if remaining1 <= 0:
                    address4 = TreeNode(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.query(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['query'][index0] = (address0, self._offset)
        return address0

    def _read_exp(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['exp'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_andexp()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                remaining1, index4, elements3, address5 = 1, self._offset, [], True
                while address5 is not FAILURE:
                    address5 = self._read__()
                    if address5 is not FAILURE:
                        elements3.append(address5)
                        remaining1 -= 1
                if remaining1 <= 0:
                    address4 = TreeNode(self._input[index4:self._offset], index4, elements3)
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address6 = FAILURE
                    chunk0 = None
                    if self._offset < self._input_size:
                        chunk0 = self._input[self._offset:self._offset + 2]
                    if chunk0 == 'OR':
                        address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                        self._offset = self._offset + 2
                    else:
                        address6 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"OR"')
                    if address6 is not FAILURE:
                        elements2.append(address6)
                        address7 = FAILURE
                        remaining2, index5, elements4, address8 = 1, self._offset, [], True
                        while address8 is not FAILURE:
                            address8 = self._read__()
                            if address8 is not FAILURE:
                                elements4.append(address8)
                                remaining2 -= 1
                        if remaining2 <= 0:
                            address7 = TreeNode(self._input[index5:self._offset], index5, elements4)
                            self._offset = self._offset
                        else:
                            address7 = FAILURE
                        if address7 is not FAILURE:
                            elements2.append(address7)
                            address9 = FAILURE
                            address9 = self._read_andexp()
                            if address9 is not FAILURE:
                                elements2.append(address9)
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode2(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.orexp(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['exp'][index0] = (address0, self._offset)
        return address0

    def _read_andexp(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['andexp'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_groupexp()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                index5, elements3 = self._offset, []
                address5 = FAILURE
                remaining1, index6, elements4, address6 = 1, self._offset, [], True
                while address6 is not FAILURE:
                    address6 = self._read__()
                    if address6 is not FAILURE:
                        elements4.append(address6)
                        remaining1 -= 1
                if remaining1 <= 0:
                    address5 = TreeNode(self._input[index6:self._offset], index6, elements4)
                    self._offset = self._offset
                else:
                    address5 = FAILURE
                if address5 is not FAILURE:
                    elements3.append(address5)
                    address7 = FAILURE
                    chunk0 = None
                    if self._offset < self._input_size:
                        chunk0 = self._input[self._offset:self._offset + 3]
                    if chunk0 == 'AND':
                        address7 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                        self._offset = self._offset + 3
                    else:
                        address7 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"AND"')
                    if address7 is not FAILURE:
                        elements3.append(address7)
                    else:
                        elements3 = None
                        self._offset = index5
                else:
                    elements3 = None
                    self._offset = index5
                if elements3 is None:
                    address4 = FAILURE
                else:
                    address4 = TreeNode(self._input[index5:self._offset], index5, elements3)
                    self._offset = self._offset
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[index4:index4], index4)
                    self._offset = index4
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address8 = FAILURE
                    remaining2, index7, elements5, address9 = 1, self._offset, [], True
                    while address9 is not FAILURE:
                        address9 = self._read__()
                        if address9 is not FAILURE:
                            elements5.append(address9)
                            remaining2 -= 1
                    if remaining2 <= 0:
                        address8 = TreeNode(self._input[index7:self._offset], index7, elements5)
                        self._offset = self._offset
                    else:
                        address8 = FAILURE
                    if address8 is not FAILURE:
                        elements2.append(address8)
                        address10 = FAILURE
                        index8 = self._offset
                        chunk1 = None
                        if self._offset < self._input_size:
                            chunk1 = self._input[self._offset:self._offset + 2]
                        if chunk1 == 'OR':
                            address10 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                            self._offset = self._offset + 2
                        else:
                            address10 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"OR"')
                        self._offset = index8
                        if address10 is FAILURE:
                            address10 = TreeNode(self._input[self._offset:self._offset], self._offset)
                            self._offset = self._offset
                        else:
                            address10 = FAILURE
                        if address10 is not FAILURE:
                            elements2.append(address10)
                            address11 = FAILURE
                            address11 = self._read_groupexp()
                            if address11 is not FAILURE:
                                elements2.append(address11)
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode4(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.andexp(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['andexp'][index0] = (address0, self._offset)
        return address0

    def _read_groupexp(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['groupexp'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '(':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"("')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read__()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                address4 = self._read_exp()
                if address4 is not FAILURE:
                    elements0.append(address4)
                    address5 = FAILURE
                    remaining1, index4, elements2, address6 = 0, self._offset, [], True
                    while address6 is not FAILURE:
                        address6 = self._read__()
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            remaining1 -= 1
                    if remaining1 <= 0:
                        address5 = TreeNode(self._input[index4:self._offset], index4, elements2)
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements0.append(address5)
                        address7 = FAILURE
                        chunk1 = None
                        if self._offset < self._input_size:
                            chunk1 = self._input[self._offset:self._offset + 1]
                        if chunk1 == ')':
                            address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address7 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('")"')
                        if address7 is not FAILURE:
                            elements0.append(address7)
                        else:
                            elements0 = None
                            self._offset = index2
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.parenexp(self._input, index2, self._offset, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            index5, elements3 = self._offset, []
            address8 = FAILURE
            chunk2 = None
            if self._offset < self._input_size:
                chunk2 = self._input[self._offset:self._offset + 3]
            if chunk2 == 'NOT':
                address8 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                self._offset = self._offset + 3
            else:
                address8 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"NOT"')
            if address8 is not FAILURE:
                elements3.append(address8)
                address9 = FAILURE
                remaining2, index6, elements4, address10 = 1, self._offset, [], True
                while address10 is not FAILURE:
                    address10 = self._read__()
                    if address10 is not FAILURE:
                        elements4.append(address10)
                        remaining2 -= 1
                if remaining2 <= 0:
                    address9 = TreeNode(self._input[index6:self._offset], index6, elements4)
                    self._offset = self._offset
                else:
                    address9 = FAILURE
                if address9 is not FAILURE:
                    elements3.append(address9)
                    address11 = FAILURE
                    address11 = self._read_exp()
                    if address11 is not FAILURE:
                        elements3.append(address11)
                    else:
                        elements3 = None
                        self._offset = index5
                else:
                    elements3 = None
                    self._offset = index5
            else:
                elements3 = None
                self._offset = index5
            if elements3 is None:
                address0 = FAILURE
            else:
                address0 = self._actions.notexp(self._input, index5, self._offset, elements3)
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_term()
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['groupexp'][index0] = (address0, self._offset)
        return address0

    def _read_term(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['term'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        index3, elements1 = self._offset, []
        address2 = FAILURE
        address2 = self._read_name()
        if address2 is not FAILURE:
            elements1.append(address2)
            address3 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == ':':
                address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address3 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('":"')
            if address3 is not FAILURE:
                elements1.append(address3)
            else:
                elements1 = None
                self._offset = index3
        else:
            elements1 = None
            self._offset = index3
        if elements1 is None:
            address1 = FAILURE
        else:
            address1 = TreeNode8(self._input[index3:self._offset], index3, elements1)
            self._offset = self._offset
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2)
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address4 = FAILURE
            address4 = self._read_value()
            if address4 is not FAILURE:
                elements0.append(address4)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.term(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['term'][index0] = (address0, self._offset)
        return address0

    def _read_value(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['value'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_string()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_word()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['value'][index0] = (address0, self._offset)
        return address0

    def _read_word(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['word'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^\\s():]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = self._actions.word(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['word'][index0] = (address0, self._offset)
        return address0

    def _read_string(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['string'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '"':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'"\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index4 = self._offset
                index5, elements2 = self._offset, []
                address4 = FAILURE
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 == '\\':
                    address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"\\\\"')
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    if self._offset < self._input_size:
                        address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('<any char>')
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index5
                else:
                    elements2 = None
                    self._offset = index5
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode(self._input[index5:self._offset], index5, elements2)
                    self._offset = self._offset
                if address3 is FAILURE:
                    self._offset = index4
                    chunk2 = None
                    if self._offset < self._input_size:
                        chunk2 = self._input[self._offset:self._offset + 1]
                    if chunk2 is not None and Grammar.REGEX_2.search(chunk2):
                        address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address3 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('[^"]')
                    if address3 is FAILURE:
                        self._offset = index4
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk3 = None
                if self._offset < self._input_size:
                    chunk3 = self._input[self._offset:self._offset + 1]
                if chunk3 == '"':
                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'"\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.string(self._input, index2, self._offset, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            index6, elements3 = self._offset, []
            address7 = FAILURE
            chunk4 = None
            if self._offset < self._input_size:
                chunk4 = self._input[self._offset:self._offset + 1]
            if chunk4 == '\'':
                address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address7 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"\'"')
            if address7 is not FAILURE:
                elements3.append(address7)
                address8 = FAILURE
                remaining1, index7, elements4, address9 = 0, self._offset, [], True
                while address9 is not FAILURE:
                    index8 = self._offset
                    index9, elements5 = self._offset, []
                    address10 = FAILURE
                    chunk5 = None
                    if self._offset < self._input_size:
                        chunk5 = self._input[self._offset:self._offset + 1]
                    if chunk5 == '\\':
                        address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address10 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"\\\\"')
                    if address10 is not FAILURE:
                        elements5.append(address10)
                        address11 = FAILURE
                        if self._offset < self._input_size:
                            address11 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address11 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('<any char>')
                        if address11 is not FAILURE:
                            elements5.append(address11)
                        else:
                            elements5 = None
                            self._offset = index9
                    else:
                        elements5 = None
                        self._offset = index9
                    if elements5 is None:
                        address9 = FAILURE
                    else:
                        address9 = TreeNode(self._input[index9:self._offset], index9, elements5)
                        self._offset = self._offset
                    if address9 is FAILURE:
                        self._offset = index8
                        chunk6 = None
                        if self._offset < self._input_size:
                            chunk6 = self._input[self._offset:self._offset + 1]
                        if chunk6 is not None and Grammar.REGEX_3.search(chunk6):
                            address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address9 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('[^\']')
                        if address9 is FAILURE:
                            self._offset = index8
                    if address9 is not FAILURE:
                        elements4.append(address9)
                        remaining1 -= 1
                if remaining1 <= 0:
                    address8 = TreeNode(self._input[index7:self._offset], index7, elements4)
                    self._offset = self._offset
                else:
                    address8 = FAILURE
                if address8 is not FAILURE:
                    elements3.append(address8)
                    address12 = FAILURE
                    chunk7 = None
                    if self._offset < self._input_size:
                        chunk7 = self._input[self._offset:self._offset + 1]
                    if chunk7 == '\'':
                        address12 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address12 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"\'"')
                    if address12 is not FAILURE:
                        elements3.append(address12)
                    else:
                        elements3 = None
                        self._offset = index6
                else:
                    elements3 = None
                    self._offset = index6
            else:
                elements3 = None
                self._offset = index6
            if elements3 is None:
                address0 = FAILURE
            else:
                address0 = self._actions.string(self._input, index6, self._offset, elements3)
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
        self._cache['string'][index0] = (address0, self._offset)
        return address0

    def _read_name(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['name'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_4.search(chunk0):
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[a-zA-Z_]')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 is not None and Grammar.REGEX_5.search(chunk1):
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[a-zA-Z0-9\\-_]')
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.name(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['name'][index0] = (address0, self._offset)
        return address0

    def _read__(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['_'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_6.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[\\s]')
        self._cache['_'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_query()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()

# -*- coding: utf-8 -*-

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from rdg import linkedlist

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.list = linkedlist.LinkedList()
        self.list.append("test1")
        self.list.append("test2")
        self.list.append("test3")
        self.list.append("test1")
        pass
    
    def test1(self):
        self.failUnless(self.list.count() == 4)
        
    def test2(self):
        self.list.remove("test1")
        self.failUnless(self.list.count() == 3)

    def test3(self):
        self.list.remove("test1")
        self.list.remove("test1")
        self.list.remove("test1")
        self.failUnless(self.list.count() == 2)


if __name__ == '__main__':
    unittest.main()

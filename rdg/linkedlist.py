# -*- coding: utf-8 -*-

class ListNode:

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class LinkedList:

    def __init__(self):
        self.root = None
        self.current = None

    def append(self, data):
        if self.root is None:
            self.root = ListNode(data)
            return True
        
        p = self.root
        while p.next is not None:
            p = p.next
        
        node = ListNode(data)
        node.prev = p
        p.next = node
        return
    
    def remove(self, data):
        if self.root is None:
            return
        
        p = self.root
        while p is not None:
            if p.data == data:
                if p == self.root:
                    self.root = self.root.next
                    self.root.prev = None
                else:
                    p.prev.next = p.next
                if p.next is not None:
                    p.prev = p.next.prev
                break
            p = p.next

    def foreach(self, func):
        p = self.root
        while p is not None:
            func(p)
            p = p.next
    
    def count(self):
        count = 0
        p = self.root
        while p is not None:
            count = count + 1
            p = p.next
        return count

class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class DoubleNode(Node):
    def __init__(self, value):
        super().__init__(value)
        self.next = None
        self.prior = None

class SLinkedList:
    def __init__(self):
        self.head = None
        self.tail = self.head
        self.length = 0
    # Print the linked list, O(n)    
    def print(self):
        printVal = self.head
        while printVal is not None:
            print (printVal.value)
            printVal = printVal.next
    #adds node to the front, O(1)
    def prepend(self,newVal):
        newNode = Node(newVal)
        newNode.next = self.head
        self.tail = self.head
        self.head = newNode
        self.length += 1
    #adds to the last node, O(1)
    def append(self, newVal):
        newNode = Node(newVal)
        tail = self.tail
        if self.head is None:
            self.head = newNode
            self.tail = self.head
            self.length += 1
            return self
        tail.next = newNode
        self.tail = newNode
        self.length += 1
    #gathers node values into array, O(n)
    def getNodes(self):
        array = []
        currentNode = self.head
        while currentNode is not None:
            array.append(currentNode.value)
            currentNode = currentNode.next
        return array  
    #lookup/traversal, O(n)
    def traverseToIndex(self, index):
        counter = 0
        currentNode = self.head
        while counter != index:
            currentNode = currentNode.next
            counter += 1
        return currentNode
    #requires traversal, O(n), inserts at given index
    def insert(self, index, value):
        if index is None:
            print("Error: no index given")
            return self
        if index == 0:
            self.prepend(value)
            return self
        if index == self.length-1:
            self.append(value)
            return self
        newNode = Node(value)
        marker = self.traverseToIndex(index-1)
        pointer = marker.next
        marker.next = newNode
        newNode.next = pointer
        self.length += 1
        return self
    #requires traversal, O(n), removes node at index
    def remove(self, index):
        if index is None:
            print("Error: index not given")
            return self
        if index == 0:
            self.head = self.traverseToIndex(index+1)
            self.length -= 1
            return self
        if index == self.length-1:
            self.tail = self.traverseToIndex(index-1)
            self.tail.next = None
            return self
        preMarker = self.traverseToIndex(index-1)
        postMarker = self.traverseToIndex(index+1)
        preMarker.next = postMarker
        return self
    #reverse the order of the linked list, O(n)
    def reverse(self):
        if self.head.next is None:
            return self.head
        first = self.head
        second = first.next
        while second is not None:
            temp = second.next
            second.next = first
            first = second
            second = temp
        self.head.next = None
        self.head = first
        return self
    #retrieves the length of the list, O(1)
    def getLength(self):
        return self.length 
        
class DLinkedList(SLinkedList):
    def __init__(self):
        super().__init__()
        self.length = 1
    #O(1)
    def prepend(self, newVal):
        newNode = DoubleNode(newVal)
        oldNode = self.head
        newNode.next = oldNode
        self.head = newNode
        oldNode.prior = newNode
        self.length += 1
        return self
    #O(1)
    def append(self, newVal):
        newNode = DoubleNode(newVal)
        if self.head is None:
            self.head = newNode
            self.tail = self.head
            self.length += 1
            return self
        newNode.prior = self.tail
        self.tail.next = newNode
        self.tail = newNode
        self.length += 1
        return self
    #O(1)
    def traverseToIndex(self, index):
        halfLength = self.length/2
        counter = 0
        if index >= halfLength:
            counter = self.length - 1
            currentNode = self.tail
            while counter != index:
                currentNode = self.tail.prior
                counter -= 1
            return currentNode
        else:
            return super().traverseToIndex(index)
    #O(n)
    def insert(self, index, value):
        newNode = DoubleNode(value)
        if index == 0:
            return self.prepend(value)
        if index == self.length-1:
            return self.append(value)
        currentNode = self.traverseToIndex(index)
        priorNode = self.traverseToIndex(index-1)
        currentNode.prior = newNode
        newNode.next = currentNode
        priorNode.next = newNode
        newNode.priot = priorNode
        return self
    #O(n)
    def remove(self, index):
        currentNode = self.traverseToIndex(index)
        if currentNode.next is None:
            newTail = self.traverseToIndex(index-1)
            newTail.next = None
            self.length -= 1
            return self
        if currentNode is self.head:
            nextNode = self.traverseToIndex(1)
            self.head = nextNode
            self.length -= 1
            return self
        priorNode = currentNode.prior
        nextNode = currentNode.next
        priorNode.next = nextNode
        nextNode.prior = priorNode
        self.length -= 1
        return self
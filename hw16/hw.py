from typing import List, Optional
g
# Static Array
class StaticArray:
    def __init__(self, capacity: int):
        self.array = [None] * capacity
        self.capacity = capacity

    def set(self, index: int, value: int) -> None:
        self.array[index] = value

    def get(self, index: int) -> int:
        return self.array[index]


# Dynamic Array
class DynamicArray:
    def __init__(self):
        self.array = []

    def append(self, value: int) -> None:
        self.array.append(value)

    def insert(self, index: int, value: int) -> None:
        self.array.insert(index, value)

    def delete(self, index: int) -> None:
        self.array.pop(index)

    def get(self, index: int) -> int:
        return self.array[index]


# Singly Linked List
class Node:
    def __init__(self, value: int):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, value: int) -> None:
        if not self.head:
            self.head = Node(value)
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(value)

    def delete(self, value: int) -> None:
        if not self.head:
            return
        if self.head.value == value:
            self.head = self.head.next
            return
        current = self.head
        while current.next and current.next.value != value:
            current = current.next
        if current.next:
            current.next = current.next.next


# Doubly Linked List
class DoubleNode:
    def __init__(self, value: int):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, value: int) -> None:
        if not self.head:
            self.head = DoubleNode(value)
            return
        current = self.head
        while current.next:
            current = current.next
        new_node = DoubleNode(value)
        current.next = new_node
        new_node.prev = current

    def delete(self, value: int) -> None:
        if not self.head:
            return
        current = self.head
        while current and current.value != value:
            current = current.next
        if current:
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev


# Queue
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value: int) -> None:
        self.queue.append(value)

    def dequeue(self) -> int:
        return self.queue.pop(0) if self.queue else None

    def peek(self) -> int:
        return self.queue[0] if self.queue else None


# Sorting Algorithms

def insertion_sort(lst: List[int]) -> List[int]:
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and key < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst


def selection_sort(lst: List[int]) -> List[int]:
    n = len(lst)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_idx]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst


def bubble_sort(lst: List[int]) -> List[int]:
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def merge_sort(lst: List[int]) -> List[int]:
    if len(lst) > 1:
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1
    return lst


def quick_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1:
        return lst
    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

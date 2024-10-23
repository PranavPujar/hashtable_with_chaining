from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
import ctypes

K = TypeVar('K')
V = TypeVar('V')

class Node(Generic[K, V]):
    """Node class for doubly linked list."""
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None

class DoublyLinkedList(Generic[K, V]):
    """Doubly linked list implementation for collision chaining."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0
    
    def insert(self, key: K, value: V) -> None:
        """Insert a new node at the end of the list."""
        new_node = Node(key, value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def remove(self, key: K) -> bool:
        """Remove a node with the given key. Returns True if found and removed."""
        current = self.head
        while current:
            if current.key == key:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                self.size -= 1
                return True
            current = current.next
        return False
    
    def find(self, key: K) -> Optional[Node]:
        """Find and return the node with the given key."""
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None
    
    def clear(self) -> None:
        """Clear the entire list."""
        self.head = None
        self.tail = None
        self.size = 0

class HashFunction(ABC):
    """Abstract base class for hash functions."""
    @abstractmethod
    def hash(self, key: K, table_size: int) -> int:
        pass

class MultiplicationDivisionHash(HashFunction):
    """Implementation of multiplication-division hash method."""
    def __init__(self):
        self.A = 0.6180339887  # Golden ratio constant
    
    def hash(self, key: int, table_size: int) -> int:
        """Hash function using multiplication and division method."""
        hash_val = int(table_size * ((key * self.A) % 1))
        return hash_val

class CArray(Generic[K]):
    """C-style array implementation using ctypes."""
    def __init__(self, size: int):
        self.size = size
        # Create a C-style array of pointers (references in Python)
        self.array = (size * ctypes.py_object)()
        # Initialize with empty linked lists
        for i in range(size):
            self.array[i] = DoublyLinkedList()
    
    def __getitem__(self, index: int) -> DoublyLinkedList:
        if not 0 <= index < self.size:
            raise IndexError("Array index out of bounds")
        return self.array[index]
    
    def __setitem__(self, index: int, value: DoublyLinkedList) -> None:
        if not 0 <= index < self.size:
            raise IndexError("Array index out of bounds")
        self.array[index] = value

class HashTable(Generic[K, V]):
    """Hash table implementation with collision resolution by chaining."""
    def __init__(self, initial_size: int = 8, hash_function: Optional[HashFunction] = None):
        self.size = initial_size
        self.count = 0
        self.table = CArray(initial_size)
        self.hash_function = hash_function or MultiplicationDivisionHash()
    
    def _get_hash(self, key: K) -> int:
        """Get hash value for a key."""
        return self.hash_function.hash(key, self.size)
    
    def _resize(self, new_size: int) -> None:
        """Resize the hash table and rehash all elements."""
        old_table = self.table
        self.size = new_size
        self.table = CArray(new_size)
        self.count = 0
        
        # Rehash all existing elements
        for i in range(old_table.size):
            linked_list = old_table[i]
            current = linked_list.head
            while current:
                self.insert(current.key, current.value)
                current = current.next
    
    def insert(self, key: K, value: V) -> None:
        """Insert a key-value pair into the hash table."""
        hash_val = self._get_hash(key)
        
        # Check if key already exists
        existing_node = self.table[hash_val].find(key)
        if existing_node:
            existing_node.value = value
            return
        
        self.table[hash_val].insert(key, value)
        self.count += 1
        
        # Resize if load factor is too high
        if self.count >= self.size:
            self._resize(self.size * 2)
    
    def remove(self, key: K) -> bool:
        """Remove a key-value pair from the hash table."""
        hash_val = self._get_hash(key)
        if self.table[hash_val].remove(key):
            self.count -= 1
            # Resize if load factor is too low
            if self.count <= self.size // 4 and self.size > 8:
                self._resize(self.size // 2)
            return True
        return False
    
    def get(self, key: K) -> Optional[V]:
        """Get the value associated with a key."""
        hash_val = self._get_hash(key)
        node = self.table[hash_val].find(key)
        return node.value if node else None
    
    def __len__(self) -> int:
        return self.count
    
    def __contains__(self, key: K) -> bool:
        hash_val = self._get_hash(key)
        return self.table[hash_val].find(key) is not None

# Example usage and testing
if __name__ == "__main__":
    # Create a hash table
    ht = HashTable[int, int]()
    
    # Test insertions
    for i in range(10):
        ht.insert(i, i * 100)
    
    # Test retrieval
    assert ht.get(5) == 500
    assert len(ht) == 10
    
    # Test removal
    assert ht.remove(5) == True
    assert ht.get(5) is None
    assert len(ht) == 9
    
    # Test resizing
    for i in range(10, 20):
        ht.insert(i, i * 100)
    
    # Test contains
    assert 15 in ht
    assert 5 not in ht
    
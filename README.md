# Python Hash Table Implementation with C-style Arrays

A custom implementation of a hash table data structure in Python using C-style arrays and chaining for collision resolution. This implementation focuses on maintaining C-like memory management while leveraging Python's type system.

## Technical Details

### Components

1. **Node Class**

   - Generic key-value storage
   - Doubly linked list pointers (prev/next)

2. **DoublyLinkedList Class**

   - Implements chaining for collision resolution
   - Operations: insert, remove, find, clear
   - Maintains head and tail pointers

3. **CArray Class**

   - C-style array implementation using `ctypes`
   - Bounds checking
   - Fixed-size array behavior

4. **HashTable Class**
   - Initial size: 8 buckets
   - Growth condition: Doubles size when full
   - Shrink condition: Halves size when ≤ 1/4 full
   - Minimum size maintained at 8 buckets

### Hash Function

- Default implementation uses multiplication-division method
- Uses golden ratio (φ ≈ 0.6180339887) as multiplier
- Custom hash functions can be provided through `HashFunction` abstract base class

## Usage

```python
# Create a hash table
ht = HashTable[int, int]()  

# Insert key-value pairs
ht.insert(1, 100)
ht.insert(2, 200)

# Get values
value = ht.get(1)  # Returns 100
missing = ht.get(999)  # Returns None if key doesn't exist

# Remove entries
removed = ht.remove(1) 

# Check if key exists
exists = 2 in ht 

# Get number of entries
size = len(ht)
```

### Custom Hash Function Example

```python
class CustomHash(HashFunction):
    def hash(self, key: int, table_size: int) -> int:
        return key % table_size

# Use custom hash function
ht = HashTable(hash_function=CustomHash())
```

## Implementation Details

- Uses Python's `ctypes` to implement true C-style arrays
- Maintains O(1) average case complexity for insertions, deletions, and lookups
- Worst case O(n) when many collisions occur
- Automatic resizing ensures consistent performance as table grows/shrinks
- Type safety through Python's typing system

## Requirements

- Python 3.7+
- `ctypes` module (included in Python standard library)
- No external dependencies


## Testing

The implementation includes basic test cases that verify:

- Insertion and retrieval of values
- Removal of entries
- Dynamic resizing
- Collision handling
- Type safety
- Boundary conditions

Run the tests by executing the file directly:

```bash
python hash_table.py
```

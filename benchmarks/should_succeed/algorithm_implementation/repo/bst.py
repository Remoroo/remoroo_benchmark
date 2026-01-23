"""Binary Search Tree implementation - incomplete."""

class TreeNode:
    """A node in the binary search tree."""
    
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree data structure.
    
    TODO: Implement the following methods:
    - insert(value): Insert a value into the BST
    - search(value): Return True if value exists, False otherwise
    - inorder_traversal(): Return list of values in sorted order
    """
    
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        """Insert a value into the BST.
        
        TODO: Implement this method.
        - If tree is empty, create root node
        - Otherwise, find correct position maintaining BST property:
          - Values less than current node go left
          - Values greater than current node go right
        """
        pass  # TODO: Implement
    
    def search(self, value) -> bool:
        """Search for a value in the BST.
        
        TODO: Implement this method.
        Returns True if value exists, False otherwise.
        """
        pass  # TODO: Implement
    
    def inorder_traversal(self) -> list:
        """Return list of values in sorted (in-order) order.
        
        TODO: Implement this method.
        In-order traversal visits: left subtree, current node, right subtree
        """
        pass  # TODO: Implement


def main():
    """Test the BST implementation."""
    bst = BinarySearchTree()
    
    # Insert values
    values_to_insert = [5, 3, 7, 1, 4, 6, 8]
    print(f"Inserting values: {values_to_insert}")
    
    for v in values_to_insert:
        bst.insert(v)
    
    # Test search
    print("\nTesting search:")
    for v in [1, 5, 8, 10]:
        found = bst.search(v)
        print(f"  search({v}) = {found}")
    
    # Test traversal
    result = bst.inorder_traversal()
    expected = [1, 3, 4, 5, 6, 7, 8]
    
    print(f"\nIn-order traversal: {result}")
    print(f"Expected: {expected}")
    
    traversal_correct = result == expected
    print(f"\ntraversal_correct: {traversal_correct}")
    
    if traversal_correct:
        print("SUCCESS: BST implementation is correct!")
    else:
        print("FAILED: Traversal does not match expected order")


if __name__ == "__main__":
    main()


"""Directed graph with broken cycle detection.

The bug is subtle: the algorithm confuses "visited ever" with 
"currently in the DFS recursion stack".

In a DAG (Directed Acyclic Graph), a node can be visited multiple 
times via different paths without there being a cycle.

Example of false positive:
    A -> B -> D
    A -> C -> D
    
This is a DAG (no cycles), but if we just track "visited":
    1. Start DFS from A
    2. Visit B, mark visited
    3. Visit D from B, mark visited
    4. Backtrack to A
    5. Visit C, mark visited
    6. Try to visit D from C - it's already visited!
    7. BUG: Report cycle, but there isn't one!

The fix: Track which nodes are in the CURRENT recursion stack,
not just which nodes have ever been visited.

Three-color algorithm:
    - WHITE (0): Unvisited
    - GRAY (1): Currently in recursion stack (being processed)
    - BLACK (2): Completely processed (all descendants visited)
    
A cycle exists only if we encounter a GRAY node (back edge).
"""

from typing import Dict, List, Set, Tuple


class DirectedGraph:
    """A directed graph using adjacency list representation."""
    
    def __init__(self):
        self.adj_list: Dict[str, List[str]] = {}
    
    def add_node(self, node: str):
        """Add a node to the graph."""
        if node not in self.adj_list:
            self.adj_list[node] = []
    
    def add_edge(self, from_node: str, to_node: str):
        """Add a directed edge from from_node to to_node."""
        self.add_node(from_node)
        self.add_node(to_node)
        self.adj_list[from_node].append(to_node)
    
    def has_cycle(self) -> bool:
        """Check if the graph has a cycle.
        
        BUG: This implementation is WRONG!
        
        It only tracks if a node was ever visited, not if it's
        currently in the recursion stack. This causes false positives
        when a node is reachable via multiple paths.
        """
        visited: Set[str] = set()
        
        def dfs(node: str) -> bool:
            if node in visited:
                return True  # BUG: This is wrong! Visited doesn't mean cycle!
            
            visited.add(node)
            
            for neighbor in self.adj_list.get(node, []):
                if dfs(neighbor):
                    return True
            
            # BUG: We never "unmark" the node after processing!
            # We need to distinguish between "in current path" and "fully processed"
            
            return False
        
        # Check from all nodes (graph might be disconnected)
        for node in self.adj_list:
            if node not in visited:
                if dfs(node):
                    return True
        
        return False
    
    def find_cycle(self) -> List[str]:
        """Find and return a cycle if one exists, empty list otherwise.
        
        TODO: Implement this to return the actual cycle path.
        """
        # Placeholder - could be implemented for debugging
        return []


def test_cases() -> List[Tuple[str, DirectedGraph, bool]]:
    """Return test cases: (name, graph, expected_has_cycle)."""
    cases = []
    
    # Test 1: Simple cycle (A -> B -> C -> A)
    g1 = DirectedGraph()
    g1.add_edge("A", "B")
    g1.add_edge("B", "C")
    g1.add_edge("C", "A")
    cases.append(("simple_cycle", g1, True))
    
    # Test 2: Self loop (A -> A)
    g2 = DirectedGraph()
    g2.add_edge("A", "A")
    cases.append(("self_loop", g2, True))
    
    # Test 3: Linear chain - NO CYCLE
    g3 = DirectedGraph()
    g3.add_edge("A", "B")
    g3.add_edge("B", "C")
    g3.add_edge("C", "D")
    cases.append(("linear_chain", g3, False))
    
    # Test 4: Diamond DAG - NO CYCLE (this is where the bug shows!)
    #     A
    #    / \
    #   B   C
    #    \ /
    #     D
    g4 = DirectedGraph()
    g4.add_edge("A", "B")
    g4.add_edge("A", "C")
    g4.add_edge("B", "D")
    g4.add_edge("C", "D")
    cases.append(("diamond_dag", g4, False))  # BUG: Current code says True!
    
    # Test 5: Complex DAG - NO CYCLE
    #     A
    #    /|\
    #   B C D
    #   |X|/
    #   E F
    g5 = DirectedGraph()
    g5.add_edge("A", "B")
    g5.add_edge("A", "C")
    g5.add_edge("A", "D")
    g5.add_edge("B", "E")
    g5.add_edge("B", "F")
    g5.add_edge("C", "E")
    g5.add_edge("C", "F")
    g5.add_edge("D", "F")
    cases.append(("complex_dag", g5, False))  # BUG: Current code says True!
    
    # Test 6: DAG with cycle
    g6 = DirectedGraph()
    g6.add_edge("A", "B")
    g6.add_edge("B", "C")
    g6.add_edge("C", "D")
    g6.add_edge("D", "B")  # Creates cycle B -> C -> D -> B
    cases.append(("dag_with_cycle", g6, True))
    
    # Test 7: Disconnected with cycle
    g7 = DirectedGraph()
    g7.add_edge("A", "B")  # Component 1
    g7.add_edge("C", "D")  # Component 2
    g7.add_edge("D", "C")  # Cycle in component 2
    cases.append(("disconnected_cycle", g7, True))
    
    # Test 8: Disconnected no cycle
    g8 = DirectedGraph()
    g8.add_edge("A", "B")
    g8.add_edge("C", "D")
    cases.append(("disconnected_no_cycle", g8, False))
    
    return cases


def main():
    """Run all test cases."""
    print("Testing cycle detection in directed graphs\n")
    print("=" * 60)
    
    cases = test_cases()
    passed = 0
    failed = 0
    
    for name, graph, expected in cases:
        result = graph.has_cycle()
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: {name}")
        print(f"       Expected: {expected}, Got: {result}")
        if result != expected:
            print(f"       ERROR: {'False positive!' if result else 'Missed cycle!'}")
        print()
    
    print("=" * 60)
    print(f"Results: {passed}/{len(cases)} passed")
    
    all_tests_pass = (failed == 0)
    print(f"\nall_tests_pass: {all_tests_pass}")
    
    if all_tests_pass:
        print("\nSUCCESS: Cycle detection works correctly!")
    else:
        print(f"\nFAILED: {failed} test(s) failed")
        print("The bug is likely confusing 'visited' with 'in recursion stack'")


if __name__ == "__main__":
    main()


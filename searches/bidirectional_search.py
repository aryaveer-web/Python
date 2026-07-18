"""
Bidirectional Search algorithm.

Runs two simultaneous BFS — one forward from the source, one backward from
the target — and stops as soon as the two frontiers meet. This cuts the
search space roughly in half compared to a single BFS, reducing time
complexity from O(b^d) to O(b^(d/2)), where b is the branching factor and
d is the shortest-path length.

Only works on unweighted, undirected (or bidirectional) graphs where the
reverse graph is available.

Reference: https://en.wikipedia.org/wiki/Bidirectional_search
"""

from __future__ import annotations

from collections import deque


def bidirectional_search(
    graph: dict[str, list[str]], source: str, target: str
) -> list[str] | None:
    """
    Return the shortest path from source to target using bidirectional BFS,
    or None if no path exists.

    >>> g = {
    ...     "A": ["B", "C"],
    ...     "B": ["A", "D", "E"],
    ...     "C": ["A", "F"],
    ...     "D": ["B"],
    ...     "E": ["B", "F"],
    ...     "F": ["C", "E"],
    ... }
    >>> bidirectional_search(g, "A", "F")
    ['A', 'C', 'F']
    >>> bidirectional_search(g, "A", "A")
    ['A']
    >>> bidirectional_search(g, "D", "F")
    ['D', 'B', 'E', 'F']
    >>> bidirectional_search(g, "A", "Z") is None
    True
    """
    if source == target:
        return [source]

    if source not in graph or target not in graph:
        return None

    # Forward BFS state
    front_visited: dict[str, str | None] = {source: None}
    front_queue: deque[str] = deque([source])

    # Backward BFS state
    back_visited: dict[str, str | None] = {target: None}
    back_queue: deque[str] = deque([target])

    def reconstruct(meeting: str) -> list[str]:
        """Build path by tracing parents from both sides."""
        path = []
        node: str | None = meeting
        while node is not None:
            path.append(node)
            node = front_visited[node]
        path.reverse()

        node = back_visited[meeting]
        while node is not None:
            path.append(node)
            node = back_visited[node]

        return path

    while front_queue and back_queue:
        # Expand one level of the forward frontier
        for _ in range(len(front_queue)):
            node = front_queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in front_visited:
                    front_visited[neighbor] = node
                    front_queue.append(neighbor)
                if neighbor in back_visited:
                    return reconstruct(neighbor)

        # Expand one level of the backward frontier
        for _ in range(len(back_queue)):
            node = back_queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in back_visited:
                    back_visited[neighbor] = node
                    back_queue.append(neighbor)
                if neighbor in front_visited:
                    return reconstruct(neighbor)

    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }

    print("Graph:", graph)
    for src, tgt in [("A", "F"), ("D", "F"), ("A", "A"), ("A", "Z")]:
        result = bidirectional_search(graph, src, tgt)
        print(f"  {src} -> {tgt}: {result}")

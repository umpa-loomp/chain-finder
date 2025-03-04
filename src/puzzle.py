import time
import logging

logger = logging.getLogger(__name__)


class Puzzle:
    _puzzle_registry = {}  # Class-level storage for all puzzles
    _next_id = 1  # Auto-incrementing ID for puzzles

    def __init__(self, puzzle_number):
        """Initialize a puzzle with its number"""
        self.puzzle_number = puzzle_number
        self.id = Puzzle._next_id
        Puzzle._next_id += 1

        # Extract puzzle sides
        self.puzzle_sides = {"takes": puzzle_number[0:3], "gives": puzzle_number[3:6]}

    @classmethod
    def reset(cls):
        """Reset the puzzle registry and ID counter"""
        cls._puzzle_registry = {}
        cls._next_id = 1

    @classmethod
    def add_puzzle_direct(cls, puzzle_number):
        """Create and register a puzzle directly from its number"""
        if not puzzle_number or len(puzzle_number) != 6 or not puzzle_number.isdigit():
            return False

        puzzle = Puzzle(puzzle_number)
        cls._puzzle_registry[puzzle.id] = puzzle
        return True

    @classmethod
    def get_all_puzzles(cls):
        """Return a list of all registered puzzles"""
        return list(cls._puzzle_registry.values())

    @classmethod
    def find_longest_chain(
        cls, timeout_seconds=None, export_paths=False, log_progress=False
    ):
        """
        Find the longest possible chain of connected puzzles using DFS with memoization.

        Args:
            timeout_seconds: Maximum seconds to search (None for unlimited)
            export_paths: Whether to export all paths found
            log_progress: Whether to log progress

        Returns:
            list: List of puzzle IDs forming the longest chain
        """
        start_time = time.time()
        puzzles = cls.get_all_puzzles()

        if log_progress:
            logger.info(f"Starting longest chain search with {len(puzzles)} puzzles")

        # Build adjacency list for quick lookups
        graph = {}  # puzzle_id -> list of puzzle_ids it connects to
        takes_to_id = {}  # takes_value -> list of puzzle_ids

        # Index puzzles by their "takes" value
        for puzzle in puzzles:
            takes = puzzle.puzzle_sides["takes"]
            if takes not in takes_to_id:
                takes_to_id[takes] = []
            takes_to_id[takes].append(puzzle.id)

        # Build the graph connections
        for puzzle in puzzles:
            puzzle_id = puzzle.id
            gives = puzzle.puzzle_sides["gives"]

            # Find all puzzles that can connect to this one
            graph[puzzle_id] = []
            if gives in takes_to_id:
                graph[puzzle_id].extend(takes_to_id[gives])

            # Log progress periodically
            if log_progress and len(graph) % 100 == 0:
                logger.debug(f"Built graph for {len(graph)}/{len(puzzles)} puzzles")

        if log_progress:
            logger.info(f"Graph built with {len(graph)} nodes")
            edge_count = sum(len(edges) for edges in graph.values())
            logger.info(f"Total edges in graph: {edge_count}")

        # Depth-first search with memoization to find longest path
        memo = {}  # (node) -> (length, path)
        nodes_processed = 0

        def dfs(node, visited=None):
            nonlocal nodes_processed
            nodes_processed += 1

            if visited is None:
                visited = set()

            # Log progress periodically
            if log_progress and nodes_processed % 1000 == 0:
                elapsed = time.time() - start_time
                logger.debug(f"Processed {nodes_processed} nodes in {elapsed:.2f}s")

            # Check if we've already computed this
            if node in memo:
                return memo[node]

            # Check if we're in a cycle
            if node in visited:
                return 1, [node]

            # Check timeout
            if timeout_seconds and time.time() - start_time > timeout_seconds:
                raise TimeoutError("Chain search timed out")

            visited.add(node)

            max_length = 1
            max_path = [node]

            # Try each neighbor
            for neighbor in graph[node]:
                # Skip self-references
                if neighbor == node:
                    continue

                # Create a new visited set for this branch
                # This is important for proper backtracking!
                new_visited = visited.copy()
                length, path = dfs(neighbor, new_visited)

                # If this path is longer, update our max
                if length + 1 > max_length:
                    max_length = length + 1
                    max_path = [node] + path

            # Cache the result
            memo[node] = (max_length, max_path)
            return max_length, max_path

        longest_chain = []

        # Try starting from each puzzle
        try:
            for i, puzzle in enumerate(puzzles):
                if log_progress and (i == 0 or i % 100 == 0):
                    logger.info(f"Searching from starting point {i + 1}/{len(puzzles)}")

                _, path = dfs(puzzle.id)
                if len(path) > len(longest_chain):
                    longest_chain = path
                    if log_progress:
                        logger.info(
                            f"New longest chain found: {len(longest_chain)} puzzles"
                        )

                # Check timeout
                if timeout_seconds and time.time() - start_time > timeout_seconds:
                    logger.warning(f"Search timed out after {timeout_seconds} seconds")
                    break

        except TimeoutError:
            logger.warning(f"Search timed out after {timeout_seconds} seconds")

        # Log final results
        elapsed = time.time() - start_time
        logger.info(
            f"Found longest chain with {len(longest_chain)} puzzles in {elapsed:.2f} seconds"
        )
        logger.info(f"Total nodes processed: {nodes_processed}")

        return longest_chain

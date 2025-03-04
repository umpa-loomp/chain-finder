#!/usr/bin/env python3
"""
Quick test script for the Chain Finder
This creates a simple dataset and runs the chain finder algorithm
"""

import os
import logging
import sys
from src.puzzle import Puzzle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def create_test_data(filename="quick_test.txt"):
    """Create a simple test dataset"""
    os.makedirs("data", exist_ok=True)

    filepath = os.path.join("data", filename)

    # Create a test dataset with multiple paths
    test_data = [
        # Main path (length 5)
        "100200",
        "200300",
        "300400",
        "400500",
        "500600",
        # Alternative path (length 7)
        "100150",
        "150250",
        "250350",
        "350450",
        "450550",
        "550650",
        "650750",
    ]

    with open(filepath, "w") as f:
        for puzzle in test_data:
            f.write(f"{puzzle}\n")

    logger.info(f"Created test dataset with {len(test_data)} puzzles in {filepath}")
    return filepath


def run_quick_test():
    """Run a quick test of the chain finder"""
    # Create test data
    filepath = create_test_data()

    # Load puzzles
    Puzzle.reset()
    count = 0
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and len(line) == 6 and line.isdigit():
                if Puzzle.add_puzzle_direct(line):
                    count += 1

    logger.info(f"Loaded {count} puzzles")

    # Find longest chain
    logger.info("Finding longest chain...")
    chain = Puzzle.find_longest_chain(
        timeout_seconds=None, export_paths=False, log_progress=True
    )

    # Display results
    puzzles = Puzzle.get_all_puzzles()

    logger.info(f"Found chain with length {len(chain)}")
    logger.info("-" * 50)
    logger.info(f"{'Position':<8} {'ID':<5} {'Number':<8} {'Takes':<6} {'Gives':<6}")
    logger.info("-" * 50)

    for idx, puzzle_id in enumerate(chain):
        p = next((p for p in puzzles if p.id == puzzle_id), None)
        if p:
            logger.info(
                f"{idx + 1:<8} {p.id:<5} {p.puzzle_number:<8} {p.puzzle_sides['takes']:<6} {p.puzzle_sides['gives']:<6}"
            )

    # Verify connections
    logger.info("\nVerifying chain connections:")
    is_valid = True
    for i in range(len(chain) - 1):
        p1 = next((p for p in puzzles if p.id == chain[i]), None)
        p2 = next((p for p in puzzles if p.id == chain[i + 1]), None)

        if p1 and p2:
            connection_valid = p1.puzzle_sides["gives"] == p2.puzzle_sides["takes"]
            logger.info(
                f"Link {i + 1} -> {i + 2}: {p1.puzzle_number} -> {p2.puzzle_number} : {'✓ Valid' if connection_valid else '✗ INVALID'}"
            )
            is_valid = is_valid and connection_valid

    if is_valid:
        logger.info("\n✓ All connections are valid!")
    else:
        logger.error("\n✗ Some connections are invalid!")

    return is_valid


if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)

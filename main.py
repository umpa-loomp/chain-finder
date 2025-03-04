#!/usr/bin/env python3
# filepath: /c:/puz_pieces/chain-finder/main.py
# main.py - Entry point for the chain finder application
import os
import sys
import logging
import argparse
import time

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from puzzle import Puzzle
from test_graph import run_all_tests


def setup_logging(verbose=False):
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


def load_dataset(file_path, logger):
    """Load puzzles from a dataset file"""
    Puzzle.reset()

    if not os.path.exists(file_path):
        logger.error(f"Dataset file not found: {file_path}")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        count = 0
        for line in lines:
            line = line.strip()
            if line and len(line) == 6 and line.isdigit():
                if Puzzle.add_puzzle_direct(line):
                    count += 1

        logger.info(f"Loaded {count} puzzles from {file_path}")
        return count > 0

    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return False


def find_and_display_chain(timeout, logger, export_path=None):
    """Find the longest chain and display/export the results"""
    start_time = time.time()

    try:
        chain = Puzzle.find_longest_chain(
            timeout_seconds=timeout, export_paths=False, log_progress=True
        )
        elapsed = time.time() - start_time

        logger.info(f"Found chain with length {len(chain)} in {elapsed:.2f} seconds")

        if len(chain) > 0:
            puzzles = Puzzle.get_all_puzzles()

            # Display chain details
            logger.info("\nChain details:")
            logger.info("-" * 50)
            logger.info(
                f"{'Position':<8} {'ID':<5} {'Number':<8} {'Takes':<6} {'Gives':<6}"
            )
            logger.info("-" * 50)

            for idx, puzzle_id in enumerate(chain):
                p = next((p for p in puzzles if p.id == puzzle_id), None)
                if p:
                    logger.info(
                        f"{idx + 1:<8} {p.id:<5} {p.puzzle_number:<8} {p.puzzle_sides['takes']:<6} {p.puzzle_sides['gives']:<6}"
                    )

            # Export chain if requested
            if export_path:
                try:
                    with open(export_path, "w", encoding="utf-8") as f:
                        f.write(f"# Chain with {len(chain)} puzzles\n")
                        f.write(
                            f"# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        )

                        f.write(
                            f"{'Position':<8} {'ID':<5} {'Number':<8} {'Takes':<6} {'Gives':<6}\n"
                        )
                        f.write("-" * 40 + "\n")

                        for idx, puzzle_id in enumerate(chain):
                            p = next((p for p in puzzles if p.id == puzzle_id), None)
                            if p:
                                f.write(
                                    f"{idx + 1:<8} {p.id:<5} {p.puzzle_number:<8} {p.puzzle_sides['takes']:<6} {p.puzzle_sides['gives']:<6}\n"
                                )

                    logger.info(f"\nChain exported to {export_path}")
                except Exception as e:
                    logger.error(f"Error exporting chain: {e}")

            return True
        else:
            logger.warning("No chain found!")
            return False

    except Exception as e:
        logger.error(f"Error finding chain: {e}")
        return False


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(description="Puzzle Chain Finder")
    parser.add_argument("-f", "--file", help="Path to dataset file")
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=None,
        help="Timeout in seconds (default: none)",
    )
    parser.add_argument("-e", "--export", help="Export chain to file")
    parser.add_argument("--test", action="store_true", help="Run test suite")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()
    logger = setup_logging(args.verbose)

    if args.test:
        logger.info("Running test suite...")
        success = run_all_tests()
        return 0 if success else 1

    if not args.file:
        logger.error("Dataset file is required. Use -f/--file option.")
        return 1

    if load_dataset(args.file, logger):
        find_and_display_chain(args.timeout, logger, args.export)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())

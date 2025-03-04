# Puzzle Chain Finder

A utility for finding the longest possible chain of interconnected puzzles.

## Overview

This project implements an algorithm to find the longest possible chain of puzzles where each puzzle connects to the next by matching "gives" and "takes" values.

## How It Works

Each puzzle is represented by a 6-digit number:
- First 3 digits: what the puzzle "takes"
- Last 3 digits: what the puzzle "gives"

For example, puzzle "104211":
- Takes: 104
- Gives: 211

Two puzzles can connect if the "gives" of one puzzle matches the "takes" of another.

## Project Structure

```
chain-finder
├── src
│   ├── puzzle.py        # Contains the Puzzle class and its methods
│   └── test_graph.py    # Contains tests for the Puzzle class
├── data
│   └── source.txt       # Source file containing puzzle data
├── requirements.txt      # Lists project dependencies
├── main.py               # Entry point for running the application
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd chain-finder
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Prepare Data**
   Place your puzzle data in the `data/source.txt` file. Each line should contain a puzzle in the expected format.

4. **Run Tests**
   You can run the tests to validate the functionality of the `Puzzle` class:
   ```
   python src/test_graph.py
   ```

5. **Run the Application**
   To execute the chain finder functionality, run:
   ```
   python main.py
   ```

## Functionality Overview

- **Puzzle Class**: Implements methods to add puzzles, find the longest chain, and reset the puzzle state.
- **Testing**: Various test functions are provided to ensure the correctness of the implementation, including tests for simple chains, branching structures, complex structures, cycle detection, and performance.
- **Data Loading**: The application can load puzzles from a specified data file for performance testing.

## Usage
To run the project:
1. Navigate to the `chain-finder` directory
2. Run the test suite: `python main.py --test`
3. Find longest chains: `python main.py -f data/source.txt`

### Running Tests

```bash
python main.py --test
python main.py -f data/source.txt
python main.py -f data/source.txt -t 60
python main.py -f data/source.txt -e results.txt
```

Algorithm
The chain-finding algorithm works as follows:

Build a directed graph where each node is a puzzle
Add edges between puzzles where one puzzle's "gives" matches another's "takes"
Use depth-first search with memoization to find the longest path
Implement cycle detection to prevent infinite loops
Apply timeout functionality for handling large datasets
Performance Notes
The algorithm has O(n²) time complexity in the worst case
Memoization significantly improves performance by avoiding redundant calculations
The timeout parameter helps control execution time for large datasets
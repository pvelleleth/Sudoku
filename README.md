# Sudoku AI Project

This project implements a Sudoku puzzle solver using a combination of constraint propagation, optimization techniques, and recursive backtracking. The script reads a puzzle file, applies various solving strategies, and prints the solution along with timing and checksum information.

## Features
- **Support for puzzles of arbitrary size** (not limited to 9x9 grids).
- **Constraint propagation**: Optimizes the search space by eliminating invalid options based on neighboring constraints.
- **Recursive backtracking**: Solves the puzzle by recursively guessing values for the most constrained cells.

## How to Run the Script
- Ensure you have Python 3 installed.
- Place your puzzle file in the same directory as the script.
- Run the following command:

```bash
python3 sudokuBlack.py puzzle_file
```

Example:

```bash
python3 sudokuBlack.py puzzles.txt
```

### Input Format

The puzzle file should contain multiple lines, each representing a puzzle. Each puzzle should have one line of symbols, where unsolved cells are represented by a dot (.).

Example of a 9x9 puzzle:

```text
53..7....6..195....98....6.8...6...34..8..6...7...9...65....7..1...8.2..6...6....195
```

## Algorithms and Techniques

### 1. **Constraint Progagation**
The script propagates constraints across rows, columns, and sub-blocks by eliminating invalid symbols for unsolved cells. The primary method used is **forward-looking**, where solved cells immediately reduce the solution space for neighboring cells.

### 2. **Backtracking**
The solver uses a **recursive backtracking algorithm** to try different symbol placements for the most constrained cell (the one with the fewest possible symbols left). The solver explores potential solutions by recursively branching out for each valid guess and backtracks when an invalid configuration is reached.

### 3. **Optimization Techniques**
Several optimizations are applied to reduce the number of recursive calls and speed up solving:
   - **Squares1 Optimization**: Identifies and reduces repeated symbols within a constraint set (row, column, or block). For example, if only two cells in a row can contain certain symbols, this optimization ensures that other cells in the same row cannot contain these symbols.
   - **Squares2 Optimization**: Tracks the number of appearances of each symbol in a constraint set and groups them into pairs, reducing the solution space by narrowing down potential placements for these symbols.
   - **Overlap Optimization**: This technique leverages the overlap between blocks and rows/columns. By observing common cells between constraint sets, it eliminates symbol candidates in a way that satisfies both constraints simultaneously.

### 4. **Most Constrained Variable Heuristic**

The solver selects the next cell to work on based on the most constrained variable heuristic. It chooses the cell with the fewest remaining possibilities, reducing the number of guesses and improving efficiency.

### 5. **Forward-Looking**

A technique that continually propagates constraints forward after each cell is solved, ensuring that unnecessary guesses are avoided as the solution becomes clearer.

### 6. **Checksum Validation**

After each puzzle is solved, a checksum is generated to validate the correctness of the solution. This is done by converting each symbol to its ASCII value, summing them, and subtracting the minimal value.

## Performance

The script measures and outputs the time taken to solve each puzzle and the total time to solve all puzzles in the input file. Optimizations ensure the solver is efficient, even for larger or more complex puzzles.

## Example Output

```bash
1  : 53..7....6..195....98....6.8...6...34..8..6...7...9...65....7..1...8.2..6...6....195
   : 534678912672195348198342567859761423426853791713924856961537284287419635345286179 4625 0.0371s

2  : 3....5....62.1....7..9...3..2..8.....57....4...1..7..25....19.3....85....9..2...6
   : 348975126962314875751926483623758194895741362417682957276493518539167248184529637 4728 0.0258s

Total time: 0.0629s
```

## Future Improvements

- **Multithreading support** for solving multiple puzzles simultaneously.
- **Improved heuristics** for selecting the next guess to reduce backtracking.
- **Extended support** for more complex Sudoku variants, such as Samurai or Hyper Sudoku.


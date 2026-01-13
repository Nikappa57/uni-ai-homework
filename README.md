# AI Sudoku Solver

This repository contains the implementation and comparative analysis of two Artificial Intelligence approaches for solving Sudoku puzzles:

1. **Informed Search (A*):** A custom implementation of the A* algorithm, optimized with the *Minimum Remaining Values (MRV)* strategy and a domain-sum heuristic to reduce the branching factor.
2. **Constraint Satisfaction Problem (CSP):** A declarative solver utilizing the `python-constraint` library to solve the grid via constraint propagation and arc consistency.

This project was developed as part of the Artificial Intelligence course to analyze the performance trade-offs between search-based agents and constraint programming.

banckmarks: https://norvig.com/CQ/sudoku.html

## Dependencies

The project is developed in **Python 3** (tested on version 3.11).
The required external libraries are listed in `requirements.txt` and include:
* `python-constraint`: For the CSP solver implementation.
* `pandas`, `matplotlib`, `seaborn`: For data analysis and visualization.
* `notebook`: To execute the Jupyter Notebook for the experimental report.

## How to Run

### 1. Environment Setup
To ensure reproducibility and isolate dependencies, it is recommended to execute the code within a virtual environment.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run A* with a specific puzzle string
python src/AStarSolver.py "005080700700204005320000084060105040008000500070803010450000091600508007003010600"

# Run A* with a default instance
python src/AStarSolver.py

# Run CSP with a default instance
python src/CSPSolver.py

# Run CSP with a specific puzzle string

python src/CSPSolver.py ".923.........8.1...........1.7.4...........658.........6.5.2...4.....7.....9....."

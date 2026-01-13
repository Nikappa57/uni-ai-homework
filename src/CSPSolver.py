from constraint import AllDifferentConstraint, Problem

from Sudoku import Sudoku
import sys


class CSPSolver:
    """Sudoku Solver using Constraint Satisfaction Problem (CSP) approach."""

    def solve(self, initial_state: Sudoku) -> Sudoku | None:
        problem = Problem()

        # variables
        rows = range(Sudoku.SIZE)
        cols = range(Sudoku.SIZE)
        for r in rows:
            for c in cols:
                idx = r * Sudoku.SIZE + c
                val = initial_state.grid[idx]
                # void cell: domain is 1-9
                if val == 0:
                    problem.addVariable(idx, range(1, Sudoku.SIZE + 1))
                else:
                    # pre-filled cell: domain is the fixed value
                    problem.addVariable(idx, [val])

        # constraints #
        # rows
        for r in rows:
            # Raccogliamo gli indici di questa riga
            row_indices = [r * Sudoku.SIZE + c for c in cols]
            problem.addConstraint(AllDifferentConstraint(), row_indices)

        # cols
        for c in cols:
            # Raccogliamo gli indici di questa colonna
            col_indices = [r * Sudoku.SIZE + c for r in rows]
            problem.addConstraint(AllDifferentConstraint(), col_indices)

        # box
        for box_row in range(0, Sudoku.SIZE, Sudoku.BOX_SIZE):
            for box_col in range(0, Sudoku.SIZE, Sudoku.BOX_SIZE):
                box_indices = []
                for i in range(Sudoku.BOX_SIZE):
                    for j in range(Sudoku.BOX_SIZE):
                        r = box_row + i
                        c = box_col + j
                        box_indices.append(r * Sudoku.SIZE + c)

                problem.addConstraint(AllDifferentConstraint(), box_indices)

        # solve
        solution_dict = problem.getSolution()

        if solution_dict:
            new_grid = []
            for i in range(Sudoku.SIZE * Sudoku.SIZE):
                new_grid.append(solution_dict[i])

            return Sudoku(new_grid)

        return None


if __name__ == "__main__":
    instance = sys.argv[1] if len(sys.argv) > 1 else '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    puzzle = Sudoku.from_string(instance)
    print("Initial Sudoku:")
    print(puzzle)
    solver = CSPSolver()
    solution = solver.solve(puzzle)
    if solution:
        print("Solved Sudoku:")
        print(solution)
    else:
        print("No solution found.")

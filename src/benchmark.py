from AStarSolver import AStarSolver
from CSPSolver import CSPSolver
from heuristics import h_domain_sum, h_zero
from Sudoku import Sudoku

INSTANCES = [
    ("easy",
     "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
     ),
]

EURISTICS = {
    "zero": h_zero,
    "domain_sum": h_domain_sum,
}

STRATEGIES = {
    "first": Sudoku.ActionsStrategy.FIRST,
    "random": Sudoku.ActionsStrategy.RANDOM,
    "mrv": Sudoku.ActionsStrategy.MRV,
    "all": Sudoku.ActionsStrategy.ALL,
}


def main(string: str, name: str) -> None:

    puzzle = Sudoku.from_string(string)

    print(f"Solving instance: {name}")

    print(puzzle)
    print()

    print(
        "-" * 40,
        "A* Search Results",
        "-" * 40,
    )
    for euristic_name, euristic_func in EURISTICS.items():
        for strategy_name, strategy in STRATEGIES.items():
            solver = AStarSolver(heuristic_func=euristic_func,
                                 strategy=strategy)
            solution_node = solver.solve(puzzle)

            print(f"Instance: {name} | Heuristic: {euristic_name} | "
                  f"Strategy: {strategy_name}")
            if solution_node is not None:
                print("Solution found:")
                print(solution_node.state)
                print(f"Nodes expanded: {solver.nodes_expanded}")
                print(f"Nodes generated: {solver.nodes_generated}")
                print(f"Solution depth: {solution_node.g}")
            else:
                print("No solution found.")
            print("-" * 40)

    print("\n\n")
    print("-" * 40, "CSP Solver Results", "-" * 40)
    csp_solver = CSPSolver()
    csp_solution = csp_solver.solve(puzzle)
    if csp_solution:
        print("CSP Solution found:")
        print(csp_solution)
    else:
        print("No CSP solution found.")
    print("-" * 40)


if __name__ == "__main__":
    for name, instance in INSTANCES:
        main(instance, name=name)

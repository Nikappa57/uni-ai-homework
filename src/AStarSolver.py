from heapq import heappop, heappush

from Sudoku import Sudoku


class Node:
    """
    Data structure for a node in the A* search tree.
    """

    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action

        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


class AStarSolver:
    """
    A* Search Solver for Sudoku puzzles.
    """

    def __init__(
            self,
            heuristic_func,
            strategy: Sudoku.ActionsStrategy = Sudoku.ActionsStrategy.MRV):
        self.heuristic_func = heuristic_func
        self.strategy = strategy
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.max_frontier_size = 0
        self.max_explored_size = 0

    def solve(self, initial_state) -> Node | None:
        # node <- a node with n.State = problem.InitialState
        start_h = self.heuristic_func(initial_state)
        start_node = Node(state=initial_state, g=0, h=start_h)

        # frontier <- priority queue
        frontier = []
        heappush(frontier, start_node)
        self.nodes_generated += 1

        # explored <- empty set
        explored = set()

        # loop do
        while frontier:  # if Empty?(frontier)

            # Track max sizes
            self.max_frontier_size = max(self.max_frontier_size, len(frontier))
            self.max_explored_size = max(self.max_explored_size, len(explored))

            # n <- Pop(frontier)
            current_node = heappop(frontier)

            # if problem.GoalTest(n.State) then return Solution(n)
            if current_node.state.is_goal():
                return current_node

            # explored <- explored U n.State
            explored.add(current_node.state)
            self.nodes_expanded += 1

            # for each action a in problem.Actions(n.State) do
            actions = current_node.state.get_actions(self.strategy)

            for action in actions:
                cell_idx, value = action

                # n' <- ChildNode(problem, n, a)
                new_state = current_node.state.make_move(cell_idx, value)

                new_g = current_node.g + 1
                new_h = self.heuristic_func(new_state)

                child_node = Node(state=new_state,
                                  parent=current_node,
                                  action=action,
                                  g=new_g,
                                  h=new_h)

                # if n'.State not in explored U States(frontier)

                if new_state in explored:
                    continue

                for n in frontier:
                    if n.state == new_state:
                        continue

                heappush(frontier, child_node)
                self.nodes_generated += 1

                # NO REOPENING

        return None


if __name__ == "__main__":
    import sys

    from heuristics import h_domain_sum, h_zero

    instance = sys.argv[1] if len(
        sys.argv
    ) > 1 else '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    puzzle = Sudoku.from_string(instance)
    solver = AStarSolver(heuristic_func=h_domain_sum,
                         strategy=Sudoku.ActionsStrategy.MRV)
    solution_node = solver.solve(puzzle)
    if solution_node:
        # Reconstruct solution path
        path = []
        node = solution_node
        while node:
            path.append(node)
            node = node.parent
        path.reverse()

        for step, n in enumerate(path):
            print(
                f"Step {step} (g={n.g}, h={n.h}, f={n.f}) action : {n.action}")
            print(n.state)
            print()

        print(f"Solved in {len(path) - 1} moves.")
        print(f"Nodes expanded: {solver.nodes_expanded}")
        print(f"Nodes generated: {solver.nodes_generated}")
        print(f"Max frontier size: {solver.max_frontier_size}")
        print(f"Max explored size: {solver.max_explored_size}")
        print(f"Solution depth: {solution_node.g}")
        print(f"Solution heuristic cost: {solution_node.h}")
        print(f"Solution total cost (f): {solution_node.f}")
        print(f"Final state is goal: {solution_node.state.is_goal()}")
        print(f"Final state:\n{solution_node.state}")
    else:
        print("No solution found.")
        print("No solution found.")

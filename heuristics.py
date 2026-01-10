from Sudoku import Sudoku


def h_zero(state: Sudoku) -> int:
    return 0


def h_valid_sum(state: Sudoku) -> int:
    cost = 0
    empty_indices = [i for i, x in enumerate(state.grid) if x == 0]

    for idx in empty_indices:
        num_options = len(state.valid_values(idx))

        # If there are no valid options, return a high cost
        if num_options == 0:
            return 999

        cost += num_options

    return cost


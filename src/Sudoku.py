import random
from enum import Enum


class Sudoku:
    SIZE = 9
    BOX_SIZE = 3
    PEERS = {}
    DIGIT_SET = set(range(1, SIZE + 1))

    def __init__(self, board_grid: list[int]):
        self.grid = board_grid

    @classmethod
    def _initialize_peers(cls) -> None:
        for index in range(81):
            r, c = divmod(index, cls.SIZE)
            box_r, box_c = (r // 3) * 3, (c // 3) * 3

            peers = set()
            peers.update(range(r * cls.SIZE, r * cls.SIZE + cls.SIZE))
            peers.update(range(c, cls.SIZE * cls.SIZE, cls.SIZE))
            for br in range(box_r, box_r + 3):
                for bc in range(box_c, box_c + 3):
                    peers.add(br * cls.SIZE + bc)
            peers.discard(index)
            cls.PEERS[index] = list(peers)

    @classmethod
    def from_string(cls, board_str: str):
        _board_str: str = board_str.strip()

        if len(_board_str) != Sudoku.SIZE * Sudoku.SIZE:
            raise ValueError(
                f"Invalid board length: expected {Sudoku.SIZE * Sudoku.SIZE} characters, got {len(_board_str)}."
            )

        grid: list[int] = []
        for c in _board_str:
            if c.isdigit():
                grid.append(int(c))
            elif c in ('.', '0'):
                grid.append(0)
            else:
                raise ValueError(f"Invalid char '{c}'.")
        return cls(grid)

    def is_valid_move(self, index, value) -> bool:
        if self.grid[index] != 0:
            return False

        for peer_idx in self.PEERS[index]:
            if self.grid[peer_idx] == value:
                return False

        return True

    def make_move(self, index, value) -> "Sudoku":
        new_grid_data = self.grid[:]
        new_grid_data[index] = value
        return Sudoku(new_grid_data)

    def is_goal(self) -> bool:
        return 0 not in self.grid

    def valid_values(self, index) -> set[int]:
        return self.DIGIT_SET - set(self.grid[s] for s in self.PEERS[index])

    # GET ACTIONS #

    class ActionsStrategy(Enum):
        FIRST = "first"
        RANDOM = "random"
        MRV = "mrv"
        ALL = "all"

    def get_actions(
        self,
        strategy: ActionsStrategy = ActionsStrategy.MRV,
    ) -> list[tuple[int, int]]:
        """
        Dispatcher method to select the strategy.
        """
        if strategy == self.ActionsStrategy.FIRST:
            return self._get_actions_first()
        elif strategy == self.ActionsStrategy.RANDOM:
            return self._get_actions_random()
        elif strategy == self.ActionsStrategy.MRV:
            return self._get_actions_mrv()
        elif strategy == self.ActionsStrategy.ALL:
            return self._get_actions_all()

    def _get_actions_first(self) -> list[tuple[int, int]]:
        """Pick the first empty cell found."""
        idx = self.grid.index(0)  # note: no action -> error

        return [(idx, v) for v in self.valid_values(idx)]

    def _get_actions_random(self) -> list[tuple[int, int]]:
        """Pick a random empty cell."""
        # Find all empty indices
        empties = [i for i, x in enumerate(self.grid) if x == 0]

        if not empties:
            return []

        idx = random.choice(empties)
        valid_vals = self.valid_values(idx)
        return [(idx, v) for v in valid_vals]

    def _get_actions_mrv(self) -> list[tuple[int, int]]:
        """
        Minimum Remaining Values (MRV).
        Picks the cell with the fewest legal moves.
        """

        empties = [i for i, x in enumerate(self.grid) if x == 0]

        if not empties:
            return []

        best_idx = -1
        min_options = Sudoku.SIZE + 1
        best_vals = set()

        for idx in empties:
            vals = self.valid_values(idx)
            count = len(vals)

            # If a cell has 0 options, the branch is dead.
            if count == 0:
                return []

            # If a cell has only 1 option: stop searching.
            if count == 1:
                return [(idx, vals.pop())]

            if count < min_options:
                min_options = count
                best_idx = idx
                best_vals = vals

        return [(best_idx, v) for v in best_vals]

    def _get_actions_all(self) -> list[tuple[int, int]]:
        """Return all possible actions for all empty cells."""
        actions = []
        for idx, val in enumerate(self.grid):
            if val == 0:
                for v in self.valid_values(idx):
                    actions.append((idx, v))
        return actions

    # magic methods

    def __eq__(self, other):
        if isinstance(other, Sudoku):
            return self.grid == other.grid
        return False

    def __hash__(self):
        # need for set operations
        return hash(tuple(self.grid))

    def __str__(self):
        lines = []
        horizontal_line = "- " * 11

        for r in range(self.SIZE):
            if r > 0 and r % self.BOX_SIZE == 0:
                lines.append(horizontal_line.strip())

            row_chars = []
            for c in range(self.SIZE):
                if c > 0 and c % self.BOX_SIZE == 0:
                    row_chars.append("|")

                val = self.grid[r * self.SIZE + c]
                display_char = str(val) if val != 0 else "."
                row_chars.append(display_char)

            lines.append(" ".join(row_chars))

        return "\n".join(lines)


Sudoku._initialize_peers()

if __name__ == "__main__":
    instance = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    puzzle = Sudoku.from_string(instance)
    print(puzzle)

    print(f"Check if 5 is valid at index 1:", puzzle.is_valid_move(1, 5))
    print(f"Check if 7 is valid at index 1:", puzzle.is_valid_move(1, 7))
    puzzle2 = puzzle.make_move(1, 7)
    print(puzzle2)

    print("is goal?", puzzle.is_goal())

    print(f"Proposed Actions (first):",
          puzzle.get_actions(Sudoku.ActionsStrategy.FIRST))
    print(f"Proposed Actions (random):",
          puzzle.get_actions(Sudoku.ActionsStrategy.RANDOM))
    print(f"Proposed Actions (mrv):",
          puzzle.get_actions(Sudoku.ActionsStrategy.MRV))

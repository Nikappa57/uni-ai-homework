class Sudoku:
    """
    Represents a Sudoku puzzle instance.
    """

    SIZE = 9
    BOX_SIZE = 3

    def __init__(self, board_str: str):
        """
        Initializes the board from a string of 81 characters.

        Args:
            board_str (str): A string representing the puzzle.
                             Accepts digits '1'-'9' for values, 
                             and '.' for empty cells.
        """
        self.str: str = board_str.strip()

        if len(self.str) != 81:
            raise ValueError(
                f"Invalid board length: expected 81 characters, got {len(self.str)}."
            )

        # Internal Representation: a list
        self.grid: list[int] = []
        for c in self.str:
            if c.isdigit():
                self.grid.append(int(c))
            elif c == '.':
                self.grid.append(0)
            else:
                raise ValueError(f"Invalid char '{c}'.")

    def __str__(self):
        """
        Returns a formatted string representation of the board (Grid view).
        This allows you to simply call print(sudoku_instance).
        """
        lines = []
        # Horizontal separator line
        horizontal_line = "- " * 11

        for r in range(self.SIZE):
            # Add horizontal separator every 3 rows
            if r > 0 and r % self.BOX_SIZE == 0:
                lines.append(horizontal_line.strip())

            row_chars = []
            for c in range(self.SIZE):
                # Add vertical separator every 3 columns
                if c > 0 and c % self.BOX_SIZE == 0:
                    row_chars.append("|")

                val = self.grid[r * self.SIZE + c]
                display_char = str(val) if val != 0 else "."
                row_chars.append(display_char)

            lines.append(" ".join(row_chars))

        return "\n".join(lines)


if __name__ == "__main__":
    instance = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    print("--- Loading Sudoku ---")
    puzzle = Sudoku(instance)
    print(puzzle)

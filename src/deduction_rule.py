from abc import ABC, abstractmethod

class DeductionRule(ABC):
    def __init__(self, grid):
        self.grid = grid

    @abstractmethod
    def apply_rule(self):
        pass

class DR1(DeductionRule):
    def apply_rule(self):
        for i in range(81):
            if self.grid.grid[i] == 0:
                row, col = i // 9, i % 9
                possible_values = set(range(1, 10))

                for j in range(9):
                    possible_values.discard(self.grid.grid[row * 9 + j])

                for j in range(9):
                    possible_values.discard(self.grid.grid[j * 9 + col])

                box_start = (row // 3) * 27 + (col // 3) * 3
                for r in range(3):
                    for c in range(3):
                        possible_values.discard(self.grid.grid[box_start + r * 9 + c])

                if len(possible_values) == 1:
                    value = possible_values.pop()
                    self.grid.set_value(i, value)
                    return i, value
        return False

class DR2(DeductionRule):
    def apply_rule(self):
        return self.check_unique_in_row() or self.check_unique_in_column() or self.check_unique_in_box()

    def check_unique_in_row(self):
        for row in range(9):
            candidates = [[] for _ in range(9)]
            for col in range(9):
                index = row * 9 + col
                if self.grid.grid[index] == 0:
                    candidates[col] = self.get_candidates(index)

            for num in range(1, 10):
                occurences = [i for i, candidate in enumerate(candidates) if num in candidate]
                if len(occurences) == 1:
                    col = occurences[0]
                    index = row * 9 + col
                    self.grid.set_value(index, num)
                    return index, num
        return False

    def check_unique_in_column(self):
        for col in range(9):
            candidates = [[] for _ in range(9)]
            for row in range(9):
                index = row * 9 + col
                if self.grid.grid[index] == 0:
                    candidates[row] = self.get_candidates(index)

            for num in range(1, 10):
                occurences = [i for i, candidate in enumerate(candidates) if num in candidate]
                if len(occurences) == 1:
                    row = occurences[0]
                    index = row * 9 + col
                    self.grid.set_value(index, num)
                    return index, num
        return False

    def check_unique_in_box(self):
        for box_row in range(3):
            for box_col in range(3):
                candidates = [[] for _ in range(9)]
                indices = []
                for r in range(3):
                    for c in range(3):
                        index = (box_row * 3 + r) * 9 + (box_col * 3 + c)
                        indices.append(index)
                        if self.grid.grid[index] == 0:
                            candidates[r * 3 + c] = self.get_candidates(index)

                for num in range(1, 10):
                    occurences = [i for i, candidate in enumerate(candidates) if num in candidate]
                    if len(occurences) == 1:
                        index = indices[occurences[0]]
                        self.grid.set_value(index, num)
                        return index, num 
        return False

    def get_candidates(self, index):
        row, col = index // 9, index % 9
        candidates = set(range(1, 10))

        for i in range(9):
            candidates.discard(self.grid.grid[row * 9 + i])

        for i in range(9):
            candidates.discard(self.grid.grid[i * 9 + col])

        box_start = (row // 3) * 27 + (col // 3) * 3
        for i in range(3):
            for j in range(3):
                candidates.discard(self.grid.grid[box_start + i * 9 + j])

        return list(candidates)

class DR3(DeductionRule):
    def apply_rule(self):
        return self.find_hidden_pair_in_row() or self.find_hidden_pair_in_column() or self.find_hidden_pair_in_box()

    def find_hidden_pair_in_row(self):
        for row in range(9):
            candidates = [[] for _ in range(9)]
            for col in range(9):
                index = row * 9 + col
                if self.grid.grid[index] == 0:
                    candidates[col] = self.get_candidates(index)

            if result := self.find_hidden_pair(candidates, row, is_row=True):
                return result
        return False

    def find_hidden_pair_in_column(self):
        for col in range(9):
            candidates = [[] for _ in range(9)]
            for row in range(9):
                index = row * 9 + col
                if self.grid.grid[index] == 0:
                    candidates[row] = self.get_candidates(index)

            if result := self.find_hidden_pair(candidates, col, is_row=False):
                return result
        return False

    def find_hidden_pair_in_box(self):
        for box_row in range(3):
            for box_col in range(3):
                candidates = [[] for _ in range(9)]
                indices = []
                for r in range(3):
                    for c in range(3):
                        index = (box_row * 3 + r) * 9 + (box_col * 3 + c)
                        indices.append(index)
                        if self.grid.grid[index] == 0:
                            candidates[r * 3 + c] = self.get_candidates(index)

                if result := self.find_hidden_pair(candidates, indices, is_row=False):
                    return result
        return False

    def find_hidden_pair(self, candidates, region, is_row=True):
        for i in range(9):
            for j in range(i + 1, 9):
                if candidates[i] and candidates[j] and candidates[i] == candidates[j] and len(candidates[i]) == 2:
                    pair = set(candidates[i])

                    other_cells = [x for k, x in enumerate(candidates) if k != i and k != j]
                    if not any(pair & set(cell) for cell in other_cells):
                        if isinstance(region, list):
                            index1 = region[i]
                            index2 = region[j]
                        else:
                            index1 = region * 9 + i if is_row else i * 9 + region
                            index2 = region * 9 + j if is_row else j * 9 + region
                        
                        self.grid.set_value(index1, pair.pop())
                        self.grid.set_value(index2, pair.pop())
                        return index1, self.grid.grid[index1] 
        return False

    def get_candidates(self, index):
        row, col = index // 9, index % 9
        candidates = set(range(1, 10))

        for i in range(9):
            candidates.discard(self.grid.grid[row * 9 + i])

        for i in range(9):
            candidates.discard(self.grid.grid[i * 9 + col])

        box_start = (row // 3) * 27 + (col // 3) * 3
        for i in range(3):
            for j in range(3):
                candidates.discard(self.grid.grid[box_start + i * 9 + j])

        return list(candidates)

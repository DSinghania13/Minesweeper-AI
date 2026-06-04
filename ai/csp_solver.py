import numpy as np
from collections import defaultdict, deque


def get_probabilities(board):
    """
    board: 2D numpy array where:
           -1 = unrevealed & unflagged
           -2 = flagged mine
          0-8 = revealed clues
    Returns: Dictionary mapping (row, col) to mine probability.
    """
    rows, cols = board.shape
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    clue_to_frontier = defaultdict(list)
    frontier_to_clue = defaultdict(list)
    effective_clues = {}

    for r in range(rows):
        for c in range(cols):
            if board[r, c] > 0:
                unrevealed = []
                flagged_count = 0

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if board[nr, nc] == -1:
                            unrevealed.append((nr, nc))
                        elif board[nr, nc] == -2:
                            flagged_count += 1

                if unrevealed:
                    effective_val = board[r, c] - flagged_count
                    clue_pos = (r, c)
                    effective_clues[clue_pos] = effective_val

                    for f in unrevealed:
                        clue_to_frontier[clue_pos].append(f)
                        frontier_to_clue[f].append(clue_pos)

    if not effective_clues:
        return {}

    visited_clues = set()
    components = []

    for clue in effective_clues.keys():
        if clue not in visited_clues:
            comp_clues = []
            comp_frontiers = set()
            queue = deque([clue])
            visited_clues.add(clue)

            while queue:
                curr_clue = queue.popleft()
                comp_clues.append(curr_clue)

                for f in clue_to_frontier[curr_clue]:
                    if f not in comp_frontiers:
                        comp_frontiers.add(f)
                        for next_clue in frontier_to_clue[f]:
                            if next_clue not in visited_clues:
                                visited_clues.add(next_clue)
                                queue.append(next_clue)

            components.append((comp_clues, list(comp_frontiers)))

    final_probabilities = {}

    for comp_clues, comp_frontiers_list in components:
        num_vars = len(comp_frontiers_list)

        if num_vars > 80:
            print(f"CSP Warning: Island pathologically huge ({num_vars} tiles). Skipping to prevent lag.")
            for f in comp_frontiers_list:
                final_probabilities[f] = 0.5
            continue

        current_clue_sums = {clue: 0 for clue in comp_clues}
        unassigned_clue_neighbors = {clue: len([f for f in clue_to_frontier[clue] if f in comp_frontiers_list]) for clue
                                     in comp_clues}

        valid_configs_count = 0
        mine_counts = {f: 0 for f in comp_frontiers_list}
        current_assignment = {}

        def is_valid_partial(f_pos, proposed_val):
            """ Checks if assigning `proposed_val` to `f_pos` violates any clues. """
            for clue in frontier_to_clue[f_pos]:
                if clue not in comp_clues: continue

                new_sum = current_clue_sums[clue] + proposed_val
                unassigned = unassigned_clue_neighbors[clue] - 1
                target = effective_clues[clue]

                if new_sum > target:
                    return False
                if new_sum + unassigned < target:
                    return False
            return True

        def solve_dfs(idx):
            nonlocal valid_configs_count

            if idx == num_vars:
                valid_configs_count += 1
                for f, val in current_assignment.items():
                    if val == 1:
                        mine_counts[f] += 1
                return

            f_pos = comp_frontiers_list[idx]

            if is_valid_partial(f_pos, 0):
                current_assignment[f_pos] = 0
                for clue in frontier_to_clue[f_pos]:
                    unassigned_clue_neighbors[clue] -= 1

                solve_dfs(idx + 1)

                for clue in frontier_to_clue[f_pos]:
                    unassigned_clue_neighbors[clue] += 1
                del current_assignment[f_pos]

            if is_valid_partial(f_pos, 1):
                current_assignment[f_pos] = 1
                for clue in frontier_to_clue[f_pos]:
                    current_clue_sums[clue] += 1
                    unassigned_clue_neighbors[clue] -= 1

                solve_dfs(idx + 1)

                for clue in frontier_to_clue[f_pos]:
                    current_clue_sums[clue] -= 1
                    unassigned_clue_neighbors[clue] += 1
                del current_assignment[f_pos]

        solve_dfs(0)

        if valid_configs_count > 0:
            for f in comp_frontiers_list:
                final_probabilities[f] = round(mine_counts[f] / valid_configs_count, 4)

    return final_probabilities
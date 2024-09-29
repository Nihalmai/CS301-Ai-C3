from collections import deque

def depth_first_search(start_state, goal_state):
    stack = [(start_state, [])]
    visited_states = set()
    while stack:
        state, path = stack.pop()
        if state in visited_states:
            continue
        visited_states.add(state)
        path = path + [state]
        if state == goal_state:
            return path
        for next_state in generate_next_states(state):
            stack.append((next_state, path))
    return None

def generate_next_states(state):
    m, c, boat = state
    direction = -1 if boat == 1 else 1 
    next_states = []
    possible_moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    for move_m, move_c in possible_moves:
        new_state = (m + direction * move_m, c + direction * move_c, 1 - boat)
        if validate_state(new_state):
            next_states.append(new_state)
    return next_states

def validate_state(state):
    m, c, _ = state
    if not (0 <= m <= 3 and 0 <= c <= 3):
        return False
    if (m < c and m > 0) or ((3 - m) < (3 - c) and (3 - m) > 0):
        return False
    return True

initial_state = (3, 3, 1)
target_state = (0, 0, 0)

solution = depth_first_search(initial_state, target_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")

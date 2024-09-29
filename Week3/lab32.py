import random

def generate_k_sat(k, m, n):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            variable = random.randint(1, n)  # Random variable from 1 to n
            negation = random.choice([False, True])  # Randomly decide to negate the variable
            if negation:
                variable = -variable  # Use negative variable
            clause.add(variable)
        clauses.append(clause)
    return clauses

# Example usage:
k = 3  # Number of literals in each clause
m = 5  # Number of clauses
n = 4  # Number of variables
k_sat_problem = generate_k_sat(k, m, n)
print("Generated 3-SAT problem:", k_sat_problem)

def satisfied_count(assignment , k_sat):
    return sum(1 for clause in k_sat if any((var > 0 and assignment[var]) or (var < 0 and not assignment[-var]) for var in clause))

def hill_climbing(k_sat, n, heuristic):
    # Initial random assignment of variables (True/False)
    assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}


    while True:
        current_score = satisfied_count(assignment, k_sat)
        neighbors = []

        for var in assignment:
            # Flip variable and create a neighbor
            neighbor = assignment.copy()
            neighbor[var] = not neighbor[var]
            neighbors.append(neighbor)

        # Evaluate neighbors using the chosen heuristic
        neighbors.sort(key=lambda x: satisfied_count(x), reverse=True)
        best_neighbor = neighbors[0]
        best_score = satisfied_count(best_neighbor)

        if best_score <= current_score:  # No improvement
            break
        assignment = best_neighbor  # Move to the best neighbor

    return assignment, satisfied_count(assignment)

def variable_neighborhood_descent(k_sat, n, neighborhoods):
    # Start with a random assignment
    assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
    current_score = satisfied_count(assignment)

    for neighborhood in neighborhoods:
        while True:
            neighbors = neighborhood(assignment)

            # Evaluate neighbors
            best_neighbor = max(neighbors, key=lambda x: satisfied_count(x))
            best_score = satisfied_count(best_neighbor)

            if best_score <= current_score:
                break
            assignment = best_neighbor
            current_score = best_score

    return assignment, current_score

# Example neighborhood functions for VND
def neighborhood_flip(assignment):
    neighbors = []
    for var in assignment:
        neighbor = assignment.copy()
        neighbor[var] = not neighbor[var]
        neighbors.append(neighbor)
    return neighbors

def neighborhood_swap(assignment):
    neighbors = []
    keys = list(assignment.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            neighbor = assignment.copy()
            neighbor[keys[i]], neighbor[keys[j]] = neighbor[keys[j]], neighbor[keys[i]]
            neighbors.append(neighbor)
    return neighbors

# Add more neighborhoods as needed
def beam_search(k_sat, n, beam_width, heuristic):
    assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
    current_score = satisfied_count(assignment)

    while True:
        neighbors = []

        for var in assignment:
            neighbor = assignment.copy()
            neighbor[var] = not neighbor[var]
            neighbors.append(neighbor)

        # Sort neighbors by the heuristic score
        neighbors.sort(key=lambda x: satisfied_count(x), reverse=True)

        # Keep only the best `beam_width` neighbors
        best_neighbors = neighbors[:beam_width]
        best_scores = [satisfied_count(neighbor) for neighbor in best_neighbors]

        # Check if we have reached a local maximum
        if max(best_scores) <= current_score:
            break

        # Move to the best neighbor
        best_neighbor = best_neighbors[0]
        assignment = best_neighbor
        current_score = satisfied_count(best_neighbor)

    return assignment, satisfied_count(assignment)


def run_experiments(k, m_values, n_values):
    results = []
    
    for n in n_values:
        for m in m_values:
            k_sat = generate_k_sat(k, m, n)
            print(f"Running experiments for m={m}, n={n}")
            
            # Hill Climbing
            hc_result = hill_climbing(k_sat, n, heuristic=1)
            print("Hill Climbing:", hc_result)
            
            # Beam Search with different widths
            bs_result_3 = beam_search(k_sat, n, beam_width=3, heuristic=1)
            print("Beam Search (width=3):", bs_result_3)
            
            bs_result_4 = beam_search(k_sat, n, beam_width=4, heuristic=1)
            print("Beam Search (width=4):", bs_result_4)
            
            # Variable Neighborhood Descent
            neighborhoods = [neighborhood_flip, neighborhood_swap]  # Add more as needed
            vnd_result = variable_neighborhood_descent(k_sat, n, neighborhoods)
            print("Variable Neighborhood Descent:", vnd_result)

            # Store results for further analysis
            results.append((m, n, hc_result, bs_result_3, bs_result_4, vnd_result))

    return results

# Example usage
k = 3  # For 3-SAT
m_values = [5, 10, 15]  # Number of clauses
n_values = [5, 10, 15]  # Number of variables
results = run_experiments(k, m_values, n_values)

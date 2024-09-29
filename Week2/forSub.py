import heapq
import re
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

# Sentence tokenization and preprocessing: clean up text by removing punctuation and lowercasing
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())  # Normalize text
    return sent_tokenize(text)  # Split into sentences

# Function to compute Levenshtein Distance between two strings
def compute_edit_distance(str1, str2):
    rows, cols = len(str1), len(str2)
    dp_table = [[0] * (cols + 1) for _ in range(rows + 1)]

    for row in range(rows + 1):
        dp_table[row][0] = row
    for col in range(cols + 1):
        dp_table[0][col] = col

    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            if str1[row - 1] == str2[col - 1]:
                dp_table[row][col] = dp_table[row - 1][col - 1]
            else:
                dp_table[row][col] = 1 + min(dp_table[row - 1][col], dp_table[row][col - 1], dp_table[row - 1][col - 1])

    return dp_table[rows][cols]

# A* heuristic: estimates future cost based on sentence similarity
def estimate_cost(doc1, doc2, idx1, idx2):
    total_cost = 0
    for s1, s2 in zip(range(idx1, len(doc1)), range(idx2, len(doc2))):
        total_cost += compute_edit_distance(doc1[s1], doc2[s2])
    return total_cost

# A* algorithm to align sentences from two documents
def align_sentences(doc1, doc2):
    initial_state = (0, 0, 0)  # (index in doc1, index in doc2, cost so far)
    target_state = (len(doc1), len(doc2))

    # Priority queue for A* search
    queue = []
    heapq.heappush(queue, (0, initial_state))

    # Track visited states
    explored = set()

    while queue:
        current_f, (i, j, g_cost) = heapq.heappop(queue)

        if (i, j) in explored:
            continue

        explored.add((i, j))

        # If both documents are fully processed
        if (i, j) == target_state:
            return g_cost  # Return total cost

        # Explore possible actions: align sentences or skip one
        if i < len(doc1) and j < len(doc2):
            cost = compute_edit_distance(doc1[i], doc2[j])
            next_state = (i + 1, j + 1, g_cost + cost)
            heapq.heappush(queue, (next_state[2] + estimate_cost(doc1, doc2, i + 1, j + 1), next_state))

        if i < len(doc1):
            next_state = (i + 1, j, g_cost + 1)
            heapq.heappush(queue, (next_state[2] + estimate_cost(doc1, doc2, i + 1, j), next_state))

        if j < len(doc2):
            next_state = (i, j + 1, g_cost + 1)
            heapq.heappush(queue, (next_state[2] + estimate_cost(doc1, doc2, i, j + 1), next_state))

    return float('inf')

# Main plagiarism detection function
def check_plagiarism(text1, text2):
    # Clean and preprocess both texts
    doc1 = clean_text(text1)
    doc2 = clean_text(text2)

    # Perform A* search to align the sentences
    final_cost = align_sentences(doc1, doc2)

    # Set a threshold for detecting plagiarism (customizable)
    threshold = 10

    # Output the result based on the alignment cost
    if final_cost <= threshold:
        print(f"Potential plagiarism detected with a cost of: {final_cost}")
    else:
        print(f"No significant plagiarism detected. Alignment cost: {final_cost}")

# Test cases to evaluate the plagiarism detection system
# Test cases to evaluate the plagiarism detection system
def execute_tests():
    # Test 1: Identical sentences but in different contexts
    doc1 = "Artificial intelligence is transforming industries. It is the future of technology."
    doc2 = "Artificial intelligence is transforming industries. It is the future of technology."
    check_plagiarism(doc1, doc2)

    # Test 2: Synonyms and rephrasing in sentences
    doc1 = "Machine learning is a branch of artificial intelligence. It allows computers to learn from data."
    doc2 = "Machine learning is a subfield of AI. It enables machines to gain knowledge from data."
    check_plagiarism(doc1, doc2)

    # Test 3: Short paragraphs with little overlap
    doc1 = "Quantum computing is an emerging field. It has the potential to solve complex problems faster."
    doc2 = "Quantum computers can tackle complex calculations quickly. Traditional computers cannot match their speed."
    check_plagiarism(doc1, doc2)

    # Test 4: Complete overlap in certain sentences, but different structure
    doc1 = "Blockchain technology ensures secure transactions. It is a distributed ledger system."
    doc2 = "Blockchain is a decentralized ledger. Blockchain technology ensures secure transactions."
    check_plagiarism(doc1, doc2)

    # Test 5: Different topics with no overlap
    doc1 = "Climate change is one of the biggest challenges. We need to reduce carbon emissions to save the planet."
    doc2 = "Software development requires understanding algorithms and data structures. Efficient code is crucial."
    check_plagiarism(doc1, doc2)

# Execute the new test cases
execute_tests()


# Execute the test cases
execute_tests()
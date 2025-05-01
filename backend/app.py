from flask import Flask, request, jsonify, Response
from backend import CryptarithmeticSolver
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route("/solve", methods=["POST"])
def solve_puzzle():
    data = request.json
    print("Received data:", data)  # Log the received data
    word1 = data.get("word1", "")
    word2 = data.get("word2", "")
    word3 = data.get("word3", "")

    # Validate input
    if not word1 or not word2 or not word3:
        return jsonify({"success": False, "error": "All words must be provided."}), 400

    solver = CryptarithmeticSolver(word1, word2, word3)

    # Generate equations
    equations = solver.equationGeneration()
    print("Generated Equations:")
    for eq in equations:
        print(eq)

    steps = []
    domains = []
    decision_path = []

    def log_step(letter, value):
        decision_path.append(f"{letter}={value}")
        domains.append(solver.domains.copy())
        steps.append({"assign": letter, "value": value, "current": solver.assignments.copy()})

    # Inject hook in your solver to collect visualization info
    def wrapped_forward_checking():
        if len(solver.assignments) == len(solver.uniqueLetters):
            return solver.isSolutionValid()
        
        selectedLetter = solver.mrv()
        if not selectedLetter:
            print("No more letters to assign.")  # Debugging statement
            return False

        print("Selected letter:", selectedLetter)  # Debugging statement
        relatedEquations = [eq for eq in solver.Equations if selectedLetter in eq]
        print("Related equations:", relatedEquations)  # Debugging statement

        for equation in relatedEquations:
            equation = equation.replace('=', '==', 1)
            valid_combos = solver.findValidCombinations(equation)
            print("Valid combinations for equation:", valid_combos)  # Debugging statement
            
            if not valid_combos:
                print("No valid combinations found for", selectedLetter)  # Debugging statement
                return False
            
            filtered = solver.applyAllDiffForLetters(valid_combos)
            if not filtered:
                print("Filtered combinations are empty.")  # Debugging statement
                return False

            sortedValues = solver.lcv(selectedLetter, filtered)
            print("Sorted values for", selectedLetter, ":", sortedValues)  # Debugging statement
            
            for value in sortedValues:
                if solver.isConsistent(selectedLetter, value):
                    solver.assignments[selectedLetter] = value
                    solver.removeFromDomain(selectedLetter, value)
                    log_step(selectedLetter, value)
                    if wrapped_forward_checking():
                        return True
                    del solver.assignments[selectedLetter]
                    solver.restoreDomain(selectedLetter, value)
        return False

    # Solve the puzzle
    print("\nSolving...")
    success = wrapped_forward_checking()
        # Display result
    if success:
        print("\nSolution Found:")
        for letter, digit in solver.assignments.items():
            print(f"{letter} = {digit}")
    else:
        print("\nNo solution found.")

    # Final response
    return jsonify({
        "success": success,
        "assignments": solver.assignments,
        "steps": steps,
        "domains": domains,
        "decision_tree": decision_path,
        "equations": equations  # Include equations in the response
    })

if __name__ == "__main__":
    app.run(debug=True)

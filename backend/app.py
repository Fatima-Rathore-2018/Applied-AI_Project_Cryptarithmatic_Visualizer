#LASTEST VERSION OF CODE.
from flask import Flask, request, jsonify, Response, stream_with_context
from backend import CryptarithmeticSolver
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

@app.route("/solve", methods=["GET", "POST"])
def solve_puzzle():
    if request.method == "POST":
        data = request.json or {}
        word1 = data.get("word1", "")
        word2 = data.get("word2", "")
        word3 = data.get("word3", "")
    else:  # GET for SSE
        word1 = request.args.get("word1", "")
        word2 = request.args.get("word2", "")
        word3 = request.args.get("word3", "")

    # Validate input
    if not word1 or not word2 or not word3:
        return jsonify({"success": False, "error": "All words must be provided."}), 400

    solver = CryptarithmeticSolver(word1, word2, word3)
    equations = solver.equationGeneration()

    def event_stream():
        # Send all equations in the first message
        yield f"data: {json.dumps({'equations': solver.Equations})}\n\n"
        def wrapped_forward_checking():
            if len(solver.assignments) == len(solver.uniqueLetters):
                return solver.isSolutionValid()
            selectedLetter = solver.mrv()
            if not selectedLetter:
                return False
            relatedEquations = [eq for eq in solver.Equations if selectedLetter in eq]
            for eq_idx, equation in enumerate(solver.Equations):
                if selectedLetter not in equation:
                    continue
                equation_eval = equation.replace('=', '==', 1)
                valid_combos = solver.findValidCombinations(equation_eval)
                if not valid_combos:
                    continue
                filtered = solver.applyAllDiffForLetters(valid_combos)
                if not filtered:
                    continue
                sortedValues = solver.lcv(selectedLetter, filtered)
                for value in sortedValues:
                    if solver.isConsistent(selectedLetter, value):
                        solver.assignments[selectedLetter] = value
                        solver.removeFromDomain(selectedLetter, value)
                        step = {
                            "stepType": "assign",
                            "message": f"Assign {selectedLetter} = {value}",
                            "mapping": solver.assignments.copy(),
                            "domains": {k: v.copy() for k, v in solver.domains.items()},
                            "currentLetter": selectedLetter,
                            "currentValue": value,
                            "equationsUsed": [eq_idx],
                        }
                        yield f"data: {json.dumps(step)}\n\n"
                        if (yield from wrapped_forward_checking()):
                            return True
                        # Backtrack
                        del solver.assignments[selectedLetter]
                        solver.restoreDomain(selectedLetter, value)
                        step = {
                            "stepType": "backtrack",
                            "message": f"Backtrack on {selectedLetter} = {value}",
                            "mapping": solver.assignments.copy(),
                            "domains": {k: v.copy() for k, v in solver.domains.items()},
                            "currentLetter": selectedLetter,
                            "currentValue": value,
                            "equationsUsed": [eq_idx],
                        }
                        yield f"data: {json.dumps(step)}\n\n"
            return False
        yield from wrapped_forward_checking()
        yield f"data: {json.dumps({'done': True, 'assignments': solver.assignments})}\n\n"

    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)

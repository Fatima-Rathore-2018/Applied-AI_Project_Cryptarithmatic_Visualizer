from backend import CryptarithmeticSolver
import re

# Test function for findValidCombinations

def main():
    # Example: C2 + 2*T = O + 10*C3, with C3 assigned to 1
    word1 = 'TWO'
    word2 = 'TWO'
    word3 = 'FOUR'
    solver = CryptarithmeticSolver(word1, word2, word3)

    # Assign C3 = 1
    solver.assignments['C3'] = 1
    # Set custom domains for this test
    solver.domains['C2'] = [0, 1]
    solver.domains['T'] = [2, 3, 4, 5, 6, 7, 8, 9]
    solver.domains['O'] = [2, 3, 4, 5, 6, 7, 8, 9]

    equation = "C2 + 2*T == O + 10*C3"
    # solver.findValidCombinations(equation)
    valid_combos = solver.findValidCombinations(equation)
    print("Valid combinations:")
    for combo in valid_combos:
         print(combo)

if __name__ == "__main__":
    main()

# from backend import CryptarithmeticSolver

# def main():
#     # Example: SEND + MORE = MONEY
#     word1 = 'TWO'
#     word2 = 'TWO'
#     word3 = 'FOUR'
    
#     # Create solver instance
#     solver = CryptarithmeticSolver(word1, word2, word3)
    
#     # Generate and print equations
#     equations = solver.equationGeneration()
#     print("\nGenerated Equations:")
#     print("-------------------")
#     for eq in equations:
#         print(eq)

# if __name__ == "__main__":
#     main()

# C2_domain = [0, 1]
# T_domain = [2, 3, 4, 5, 6, 7, 8, 9]
# O_domain = [2, 3, 4, 5, 6, 7, 8, 9]

# valid_combos = []

# for C2 in C2_domain:
#     for T in T_domain:
#         O = C2 + 2*T - 10
#         if O in O_domain:
#             valid_combos.append((C2, T, O))

# print(valid_combos)

# import itertools

# C2_domain = [0, 1]
# T_domain = [2, 3, 4, 5, 6, 7, 8, 9]
# O_domain = [2, 3, 4, 5, 6, 7, 8, 9]
# C3 = 1

# equations = [
#     "C2 + 2*T == O + 10*C3"
# ]

# valid_combos = []
# for C2, T, O in itertools.product(C2_domain, T_domain, O_domain):
#     assignments = {'C2': C2, 'T': T, 'O': O, 'C3': C3}
#     if all(eval(eq, {}, assignments) for eq in equations):
#         valid_combos.append((C2, T, O))

# print(valid_combos)

from backend import CryptarithmeticSolver

def main():
    # Example: SEND + MORE = MONEY
    word1 = 'TWO'
    word2 = 'TWO'
    word3 = 'FOUR'
    
    # Create solver instance
    solver = CryptarithmeticSolver(word1, word2, word3)
    
    # Generate and print equations
    equations = solver.equationGeneration()
    print("\nGenerated Equations:")
    print("-------------------")
    for eq in equations:
        print(eq)

if __name__ == "__main__":
    main()
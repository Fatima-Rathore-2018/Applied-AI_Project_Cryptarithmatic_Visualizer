import re
import itertools

class CryptarithmeticSolver:
    def __init__(self, word1, word2, word3):
        # Storing the three words in uppercase.
        self.word1 = word1.upper()
        self.word2 = word2.upper()
        self.word3 = word3.upper()

        # Number of carry variables (length of word3).
        self.numberOfCarryVariables = len(word3)

        self.wordList = [word1, word2, word3]

        self.uniqueLetters = set(''.join(self.wordList))

        # Initialize the domains for each letter.
        self.domains = {}
        for letter in self.uniqueLetters:
            self.domains[letter] = list(range(10))

        # First letter of each word cannot be zero.
        self.domains[self.word1[0]] = list(range(1, 10))
        self.domains[self.word2[0]] = list(range(1, 10))
        self.domains[self.word3[0]] = list(range(1, 10))

        # Carry variables and their domain.
        self.carryVariables = [f'C{i}' for i in range(len(self.word3) + 1)]
        self.carryDomain = {}
        for carry in self.carryVariables:
            self.carryDomain[carry] = list(range(2))

        # Equations.
        self.Equations = []

        # Assignments dictionary.
        self.assignments = dict()

    # Function for finding the Equations.
    def equationGeneration(self):
        for i in range(len(self.word3)):
            sumOfColumn = []
            leftHandSide = []
            
            # Reading letters from left to right.
            # Letters from the current column - Operands
            if i < len(self.word1):
                sumOfColumn.append(self.word1[-(i+1)])

            if i < len(self.word2):
                sumOfColumn.append(self.word2[-(i+1)])
            # Letters of the result
            result = self.word3[-(i+1)]

            # Formulating Equation:
            # Add the carry if not at the first column.
            # Left Hand Side = Operand1 + Operand2 + Carry.
            if i > 0:
                leftHandSide.append(f"C{i}")
            
            leftHandSide.extend(sumOfColumn)
            leftHandSide = ' + '.join(leftHandSide)

            # Right Hand Side = result + 10*Next Carry
            if i < len(self.word3) - 1:
                rightHandSide = f"{result} + 10*C{i + 1}"
            else:# If the first column then just the result.
                rightHandSide = f"{result}"

            self.Equations.append(f"{leftHandSide} = {rightHandSide}")
        
        return self.Equations

    # Function for MRV (Minimum Remaning Value).
    def mrv(self):
        unassignedVariables = []
        for variable in self.domains:
            if variable not in self.assignments:
                unassignedVariables.append(variable)

        # Return 0 if all variables have been assigned.
        if len(unassignedVariables) == 0:
            return 0
        
        # Search for the variable with least domain size.
        smallestDomainLetter = unassignedVariables[0]
        for variable in unassignedVariables:
            if len(self.domains[variable]) < len(self.domains[smallestDomainLetter]):
                smallestDomainLetter = variable

        return smallestDomainLetter
        
    def lcv(self, letterByMRV, comboList):
        possibleValues = self.domains[letterByMRV]
        valueConstraints = []

        for value in possibleValues:
            constrainedCount = 0

            for combo in comboList:
                if letterByMRV in combo:
                    if combo[letterByMRV] == value:
                        constrainedCount += 1

            # Store how many times this value constrains others.
            valueConstraints.append((constrainedCount, value))

        # Sort the values so that the list is sorted by least to most constraining value.
        valueConstraints.sort()

        # Return just the values in sorted order.
        sortedValues = []
        for count, value in valueConstraints:
            sortedValues.append(value)

        return sortedValues
    
    def isConsistent(self, letter, value):
        # Check if value is already assigned to another variable (AllDiff constraint).
        for assignedLetter in self.assignments:
            if self.assignments[assignedLetter] == value:
                return False
        return True
    
    # Function to remove a value from a letter variables' domain if it exists.
    # {R: [0,1,2,3,]}
    def removeFromDomain(self, letter, value):
        if value in self.domains[letter]:
            self.domains[letter].remove(value)

    # Function to restore the letter's domain (used in backtracking).
    def restoreDomain(self, letter, value):
        if value not in self.domains[letter]:
            self.domains[letter].append(value)

    # Function for forward checking.
    # assignments:   {A: 1, B: 2}
    # def forwardChecking(self):
    #     # 1. Start from last equation - Assign that letter 1 and its carry variable is also 1.
    #     # 2. Go to second last equation. 
    #         # - Use MRV to choose which letter to assign value to next.
    #         # - Store all combinations of values.
    #         # - Assign value to that chosen letter using LCV and update domain.
    #     # 3. Go to third last equation and repeat.
    #     # 4. In case no value satisfies equations, backtrack.

    #     i = 1
    #     #j = len(self.Equations)
    #     for equation in reversed(self.Equations):
    #         # Special assignment for last equation.
    #         if i == 1:
    #             self.carryVariables[-1] = 1
    #             self.assignments[self.word3[0]] = 1
    #             self.removeFromDomain(self.word3[0], 1)

    #         else:
    #             selectedLetter = self.mrv()

    #         # Noor's function will return this list.
    #         valid_combos = self.findValidCombinations(equation)

    #         # Get filtered combo list and apply LCV.
    #         filteredCombinations = self.applyAllDiffForLetters(valid_combos)
    #         sortedValues = self.lcv(selectedLetter, filteredCombinations)

    def forwardChecking(self):
        # Base case: if all letters are assigned, we are done
        if len(self.assignments) == len(self.uniqueLetters):
            return self.isSolutionValid()

        # MRV: get the next variable to assign
        selectedLetter = self.mrv()
        if not selectedLetter:
            return False

        # Get all equations (constraints) that include this letter
        relatedEquations = [eq for eq in self.Equations if selectedLetter in eq]

        for equation in relatedEquations:
            # Find all valid combinations that satisfy the equation
            
            equation = equation.replace('=', '==', 1)
            valid_combos = self.findValidCombinations(equation)
            if not valid_combos:
                return False

            # Filter valid combos by AllDiff constraint
            filteredCombinations = self.applyAllDiffForLetters(valid_combos)
            if not filteredCombinations:
                return False

            # Get sorted values for selectedLetter using LCV
            sortedValues = self.lcv(selectedLetter, filteredCombinations)
            # Try values one by one
            for value in sortedValues:
                if self.isConsistent(selectedLetter, value):
                    self.assignments[selectedLetter] = value
                    self.removeFromDomain(selectedLetter, value)

                    if self.forwardChecking():
                        return True

                    # Backtrack
                    del self.assignments[selectedLetter]
                    self.restoreDomain(selectedLetter, value)

        return False

    def isSolutionValid(self):
        w1 = int(''.join(str(self.assignments[c]) for c in self.word1))
        w2 = int(''.join(str(self.assignments[c]) for c in self.word2))
        w3 = int(''.join(str(self.assignments[c]) for c in self.word3))
        return w1 + w2 == w3

    def extractLettersFromEquations(self, equation):
        return set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', equation))

    # Function to find the possible combinations.
    def findValidCombinations(self, equation):
        # Get all the letters in the equation.
        variables = self.extractLettersFromEquations(equation)

        assignedLetters = {}
        unassignedLetters = []

        for v in variables:
            if v in self.assignments:
                assignedLetters[v] = self.assignments[v]
            else:
                unassignedLetters.append(v)

        updatedEquation = equation
        for var, val in assignedLetters.items():
            #print(var)
            #print(val)
            updatedEquation = updatedEquation.replace(var, str(val))

        #print(updatedEquation)

        domainOfUnassignedLetter = {}
        for letters in unassignedLetters:
            # domainOfUnassignedLetter[letters] = self.domains[letters]
            if letters in self.domains:
                domainOfUnassignedLetter[letters] = self.domains[letters]
            elif letters in self.carryDomain:
                domainOfUnassignedLetter[letters] = self.carryDomain[letters]

        # Finding all possible combinations:
        validCombos = []

        print(domainOfUnassignedLetter)
        for values in itertools.product(*domainOfUnassignedLetter.values()):
            #print(values)
            assignments = dict(zip(unassignedLetters, values))
            #print(assignments)
            if eval(updatedEquation, {}, assignments):
                validCombos.append(assignments)
        
        #print(valid_combos)
        return validCombos
    
    def applyAllDiffForLetters(self, valid_combos):
        filteredCombinations = []

        for combo in valid_combos:
            # Extract letters (exclude carry variables).
            letterValues = []
            carryValues = []

            # Iterate over each key-value pair in the combo dictionary.
            for key, value in combo.items():

                if not key.startswith('C') and len(key) == 1:  
                    letterValues.append(value) 
                elif key.startswith('C') and len(key) > 1:  
                    carryValues.append(value)   
                
            # Check if all letters have unique digits.
            if len(letterValues) == len(set(letterValues)):  
                filteredCombinations.append(combo)  

        return filteredCombinations

def test():
    # Create a solver instance
    solver = CryptarithmeticSolver("TWO", "TWO", "FOUR")

    # Generate equations
    equations = solver.equationGeneration()
    print("Generated Equations:")
    for eq in equations:
        print(eq)

    # Solve the puzzle
    print("\nSolving...")
    result = solver.forwardChecking()

    # Display result
    if result:
        print("\nSolution Found:")
        for letter, digit in solver.assignments.items():
            print(f"{letter} = {digit}")
    else:
        print("\nNo solution found.")

    print(solver.assignments)

if __name__ == "__main__":
    test()



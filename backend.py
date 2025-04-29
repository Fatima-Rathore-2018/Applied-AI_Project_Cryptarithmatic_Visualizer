
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
            if len(self.domains[variable]) < len(self.domains[smallestDomainVar]):
                smallestDomainVar = variable

        return smallestDomainLetter
        
    # Function for LCV (Least Constraining Value).
    def lcv(self, letter):
        # List of all possible values for this letter.
        possibleValues = self.domains[letter]

        # List to check how many other letters each value of the current letter affect.
        valueConstraints = []

        # Count the number of other letters affected by a specific value of this letter.
        count = 0
        for value in possibleValues:
            for otherLetter in self.domains:
                if otherLetter != letter:
                    if value in self.domains[otherLetter]:
                        count += 1

            # Store the value with its count in valueConstraints list.
            valueConstraints.append((count, value))

        # Sort the values so they are from least to most constraining.
        valueConstraints.sort()

        # Store the values in a list and return it.
        sortedValues = []
        for (count, value) in valueConstraints:
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
            for otherLetter in self.uniqueLetters:
                if otherLetter != letter:
                    if value in self.domains[otherLetter]:
                        self.domains[otherLetter].remove(value)

    # Function to restore the letter's domain (used in backtracking).
    def restoreDomain(self, letter):
       for otherLetter in self.domains:
           self.domains[otherLetter].append(self.assignments[letter])

    # Function for forward checking.
    # assignments:   {A: 1, B: 2}
    def forwardChecking(self):
        # 1. Start from last equation - Assign that letter 1 and its carry variable is also 1.
        # 2. Go to second last equation. 
            # - Use MRV to choose which letter to assign value to next.
            # - Store all combinations of values.
            # - Assign value to that chosen letter using LCV and update domain.
        # 3. Go to third last equation and repeat.
        # 4. In case no value satisfies equations, backtrack.

        i = 1
        #j = len(self.Equations)
        for equation in reversed(self.Equations):
            # Special assignment for last equation.
            if i == 1:
                self.carryVariables[-1] = 1
                self.assignments[self.word3[0]] = 1
                self.removeFromDomain(self.word3[0], 1)

            else:
                selectedLetter = self.mrv()
                



            


    

           





        





        




class CryptarithmeticSolver:
    def __init__(self, word1, word2, word3):
        # Storing the three words in uppercase.
        self.word1 = word1.upper()
        self.word2 = word2.upper()
        self.word3 = word3.upper()

        # Number of carry variables (length of word3).
        self.numberOfCarryVariables = len(word3)

        self.wordList = [word1, word2, word3]

        self.uniqueLetters = set(''.join(self.words))

        # Initialize the domains for each letter.
        self.domains = {}
        for letter in self.uniqueLetters:
            self.domains[letter] = list(range(10))

        # First letter of each word cannot be zero.
        self.domains[self.word1[0]] = list(range(1, 10))
        self.domains[self.word2[0]] = list(range(1, 10))
        self.domains[self.word3[0]] = list(range(1, 10))

        # Carry variables and their domain.
        self.carryVariables = []
        self.carryDomain = {}
        for carry in self.carryVariables:
            self.carryDomain[carry] = list(range(2))

        # Equations.

        # Assignments list.
        self.assignments = {}

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
        
        # Function for LCV (least constraining value).
        # def lcv():




        





        



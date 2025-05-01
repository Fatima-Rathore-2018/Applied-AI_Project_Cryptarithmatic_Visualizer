
import re
import itertools

class CryptarithmeticSolver:
    def __init__(self, word1, word2, word3):
        self.word1 = word1.upper()
        self.word2 = word2.upper()
        self.word3 = word3.upper()
        self.numberOfCarryVariables = len(word3)
        self.wordList = [word1, word2, word3]
        self.uniqueLetters = set(''.join(self.wordList))
        self.domains = {letter: list(range(10)) for letter in self.uniqueLetters}

        for w in (self.word1, self.word2, self.word3):
            self.domains[w[0]] = list(range(1, 10))

        self.carryVariables = [f'C{i}' for i in range(len(self.word3) + 1)]
        self.carryDomain = {carry: list(range(2)) for carry in self.carryVariables}

        self.Equations = []
        self.assignments = {}

    def equationGeneration(self):
        for i in range(len(self.word3)):
            sumOfColumn = []
            leftHandSide = []
            if i < len(self.word1):
                sumOfColumn.append(self.word1[-(i+1)])
            if i < len(self.word2):
                sumOfColumn.append(self.word2[-(i+1)])
            result = self.word3[-(i+1)]
            if i > 0:
                leftHandSide.append(f"C{i}")
            leftHandSide.extend(sumOfColumn)
            lhs = ' + '.join(leftHandSide)
            rhs = f"{result} + 10*C{i+1}" if i < len(self.word3) - 1 else result
            self.Equations.append(f"{lhs} = {rhs}")
        return self.Equations

    def mrv(self):
        unassigned = [v for v in self.domains if v not in self.assignments]
        return min(unassigned, key=lambda v: len(self.domains[v]), default=None)

    def lcv(self, variable, comboList):
        counts = []
        for value in self.domains[variable]:
            conflict = sum(1 for combo in comboList if combo.get(variable) == value)
            counts.append((conflict, value))
        return [v for _, v in sorted(counts)]

    def isConsistent(self, variable, value):
        return value not in self.assignments.values()

    def removeFromDomain(self, var, val):
        if val in self.domains[var]:
            self.domains[var].remove(val)

    def restoreDomain(self, var, val):
        if val not in self.domains[var]:
            self.domains[var].append(val)

    def isSolutionValid(self):
        try:
            w1 = int(''.join(str(self.assignments[c]) for c in self.word1))
            w2 = int(''.join(str(self.assignments[c]) for c in self.word2))
            w3 = int(''.join(str(self.assignments[c]) for c in self.word3))
            return w1 + w2 == w3
        except:
            return False

    def extractLettersFromEquations(self, equation):
        return set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', equation))

    def findValidCombinations(self, equation):
        variables = self.extractLettersFromEquations(equation)
        assigned = {v: self.assignments[v] for v in variables if v in self.assignments}
        unassigned = [v for v in variables if v not in assigned]

        expr = equation
        for var, val in assigned.items():
            expr = expr.replace(var, str(val))

        domains = {v: (self.domains.get(v) or self.carryDomain.get(v)) for v in unassigned}
        validCombos = []
        for values in itertools.product(*domains.values()):
            trial = dict(zip(unassigned, values))
            try:
                if eval(expr, {}, trial):
                    validCombos.append(trial)
            except:
                continue
        return validCombos

    def applyAllDiffForLetters(self, combos):
        result = []
        for combo in combos:
            letters = [v for k, v in combo.items() if not k.startswith('C')]
            if len(letters) == len(set(letters)):
                result.append(combo)
        return result

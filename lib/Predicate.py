from lib.Literal import Literal

# A predicate has:
# name - function name
# negated - a flag to see if this predicate is negated or not
# values - either False or an ordered dictionary of values, can be a Literal object (variable or constant) or again a Predicate
# size - how many values are there

class Predicate(object):

    def __init__(self, name, negated, values):
        self.name = name
        self.negated = negated
        self.values = values
        self.size = len(self.values.keys())

    # change every literalName inside predicate with newValue
    def changeLiteralTo(self, literalName, newValue):
        if self.name == literalName:
            self.name = newValue

        for i in self.values.keys():
            value = self.values[i]

            if isinstance(value, Literal) and value.name == literalName:
                negatedBefore = value.negated
                newLiteral = Literal(newValue, negatedBefore)
                self.values[i] = newLiteral

            elif isinstance(value, Predicate):
                value.changeLiteralTo(literalName, newValue)

    # returns a string representation of the predicate object
    def printPredicate(self, showNegated=True):
        res = self.name + "("
        if showNegated and self.negated:
            res = "~" + self.name + "("
        count = 0
        keys = self.values.keys()
        for i in keys:
            count = count + 1
            v = self.values[i]

            if isinstance(v, Predicate):
                res = res + v.printPredicate()
            else:
                res = res + v.printLiteral()

            if count < self.size:
                res = res + ","

        res = res + ")"
        return res

    # checks if a predicate is equal to predicate object at hand
    def isEqual(self, aPredicate):
        notSameSize = (self.size != aPredicate.size)
        notSameName = (self.name != aPredicate.name)
        notSameNegated = (self.negated != aPredicate.negated)
        if notSameSize or notSameName or notSameNegated:
            return False

        keys = self.values.keys()
        for i in keys:
            element1 = self.values[i]
            if not aPredicate.values.has_key(i):
                return False
            element2 = aPredicate.values[i]
            if type(element1) == type(element2):
                if not element1.isEqual(element2):
                    return False
            else:
                return False

        return True

    def negatePredicate(self):
        self.negated = (not self.negated)
        return self

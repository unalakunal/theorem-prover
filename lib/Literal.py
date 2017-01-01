from string import ascii_uppercase

# A Literal object is an atom, where it can be a variable or a constant

class Literal(object):

    def __init__(self, name, negated):
        self.name = name
        self.negated = negated
        if name in ascii_uppercase:
            self.isConstant = True
        else:
            self.isConstant = False

    # returns a string representation of the predicate object
    def printLiteral(self):
        return self.name

    # checks if a literal is equal to literal object at hand
    def isEqual(self, aLiteral):
        return (self.name == aLiteral.name) and (self.negated == aLiteral.negated)

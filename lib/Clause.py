from lib.Predicate import Predicate

# Clause has predicates as an ordered dictionary where its keys are full string names, and values are objects
# If a clause is a result of a resolution, we need their parents to
# backtrack print it

class Clause(object):

    def __init__(self, clauseElements, parent1=None, parent2=None):
        self.clauseElements = clauseElements
        self.size = len(self.clauseElements.keys())
        self.parent1 = parent1
        self.parent2 = parent2

    # returns string representation of clause in order
    def printClause(self, returnString=False):
        res = ""
        keys = self.clauseElements.keys()
        for i in keys:
            element = self.clauseElements[i]
            if isinstance(element, Predicate):
                res = res + element.printPredicate(True) + ","
            else:
                res = res + element.printLiteral()

        res = res[0:len(res) - 1]
        if returnString:
            return res

    # checks if a clause is equal to clause object at hand
    def isEqual(self, aClause):
        if self.size != aClause.size:
            return False

        keys = self.clauseElements.keys()
        for i in keys:
            element1 = self.clauseElements[i]
            if not aClause.clauseElements.has_key(i):
                return False
            element2 = aClause.clauseElements[i]
            if type(element1) == type(element2):
                if not element1.isEqual(element2):
                    return False
            else:
                return False

        return True

    # return array of clause elements
    def getClauseElements(self):
        res = []
        keys = self.clauseElements.keys()
        for i in keys:
            res.append(self.clauseElements[i])
        return res

    # return string representation of the parents of clause
    def printParents(self):
        if self.parent1:
            self.parent1.printClause()
            self.parent2.printClause()
        else:
            return "None"

    # only works if there is one predicate, otherwise CNF form will not be
    # held in negation
    def negateClause(self):
        try:
            keys = self.clauseElements.keys()
            if len(keys) > 1:
                print "Can not negate the goal, violates the CNF form"
                return
            g = self.clauseElements[keys[0]]
            g.negatePredicate()
            return self

        except Exception as e:
            print "Goal set can no be found"

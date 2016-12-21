# TODO: Unifier
# TODO: Resolution algorithm altogether

from copy import copy, deepcopy
from string import ascii_uppercase

# Clause has predicates as a dictionary
class Clause(object):

    def __init__(self, clauseElements):
        self.clauseElements = clauseElements
        self.size = len(self.clauseElements.keys())

    def printClause(self):
        print ""
        print "clauseElements are:"
        for i in self.clauseElements.keys():
            element = self.clauseElements[i]
            if isinstance(element, Predicate):
                print "clause has predicate: ", element.printPredicate(), " and it's negated = ", element.negated
            else:
                print "clause has term :", element.printTerm(), " and it's negated = ", element.negated

        print ""

    def isEqual(self, aClause):
        if self.size != aClause.size:
            return False

        for i in self.clauseElements.keys():
            element1 = self.clauseElements[i]
            element2 = aClause.clauseElements[i]
            if type(element1) == type(element2):
                if not element1.isEqual(element2):
                    return False
            else:
                return False

        return True

    def getClauseElements(self):
        res = []
        for i in self.clauseElements.keys():
            res.append(self.clauseElements[i])
        return res

# A predicate has:
# a name - function name that is definitive
# negated - a flag to see if this predicate is negated or not
# values - either False or a dictionary of values, can be a term (variable or constant) or again a predicate
# size - how many values are there
class Predicate(object):

    def __init__(self, name, negated, values):
        self.name = name
        self.negated = negated
        self.values = values
        self.size = len(self.values.keys())

    def setValue(self, key, value):
        self.values[key] = value
        self.size = self.size + 1

    def getValues(self):
        res = []
        for i in self.values.keys():
            res.append(self.values[i])
        return res

    def changeName(self, newName):
        self.name = newName

    # newValue might be a predicate or 
    def changeTermTo(self, term, newValue):
        for i in self.values.keys():
            value = self.values[i]

            if isinstance(value, Term) and value.name == term.name:
                negatedBefore = value.negated
                newValue.negated = negatedBefore
                self.values[i] = newValue

            elif isinstance(value, Predicate):
                value.changeTermTo(term, newValue)


    def printPredicate(self):
        res = self.name + "("
        count = 0
        for i in self.values.keys():
            count = count + 1
            v = self.values[i]

            if isinstance(v, Predicate):
                res = res + v.printPredicate()
            else:
                res = res + v.printTerm()

            if count < self.size:
                res = res + ", "

        res = res + ")"
        return res

    def isEqual(self, aPredicate):
        notSameSize = (self.size != aPredicate.size)
        notSameName =(self.name != aPredicate.name)
        notSameNegated = (self.negated != aPredicate.negated)
        if notSameSize or notSameName or notSameNegated:
            return False

        for i in self.values.keys():
            element1 = self.values[i]
            element2 = aPredicate.values[i]            
            if type(element1) == type(element2):
                if not element1.isEqual(element2):
                    return False
            else:
                return False

        return True

    def termOccurs(self, term):
        print "see if ", term, " occurs in ", self.printPredicate()
        if self.name == term.name:
            print "True"
            return True

        else:
            for i in self.values.keys():
                if self.values[i].occurs(term):
                    print "True"            
                    return True
        
        print "False"
        return False

class Term(object):
    
    def __init__(self, name, negated):
        self.name = name
        self.negated = negated
        if name in ascii_uppercase:
            self.isConstant = True
        else:
            self.isConstant = False

    def replaceName(self, newName):
        self.name = newName

    def printTerm(self):
        return self.name

    def isEqual(self, aTerm):
        return (self.name == aTerm.name) and (self.negated == aTerm.negated)

    def termOccurs(self, term):
        return (self.name == aTerm.name)

# elements are tuple of literals
def unify(element1, element2):
    #print "elements ", element1, element2
    len1 = len(element1)
    len2 = len(element2)    

    if len1 > 1 and len2 > 1 and element1[0] != element2[0]:
        return None

    if  len1 != len2:
        return None
    
    if len1 == 1:
        if element1 == element2:
            return []
        if not (element1[0] in ascii_uppercase):
            if element1[0] in element2:
                return None
            else:
                return [[element1[0], element2[0]]]
        if not (element2[0] in ascii_uppercase):
            return [[element2[0], element1[0]]]

    if len2 == 1:
        if element2 == element1:
            return []
        if not (element2 in ascii_uppercase):
            if element2[0] in element1:
                return None
            else:
                return [[element2[0], element1[0]]]
        if not (element1[0] in ascii_uppercase):
            return [[element1[0], element2[0]]]

    f1, t1 = [element1[0]], element1[1:]
    f2, t2 = [element2[0]], element2[1:]

    z1 = unify(f1, f2)
    #print "z1 is", z1

    if z1 == None:
        return None

    g1 = apply(z1, t1)
    g2 = apply(z1, t2)

    #print "g1 ", g1, "g2 ", g2

    z2 = unify(g1, g2)

    if not z2:
        return None

    #print "z1", z1, "z2", z2

    return z1 + z2

# unifyList is a list of tuples that contains unifiers
# tupleToApply is a tuple that if it contains values to be unified, is going to be updated
def apply(unifyList, tupleToApply):
    #print "in apply ", tupleToApply, unifyList
    if len(tupleToApply) == 0:
        return tupleToApply
    for u in unifyList:
        for j in tupleToApply:
            if j == u[0]:
                j = u[1]

    return tupleToApply

def resolution(kbAndGoals, goals):
    print "---in resolution---"
    print "############# kbAndGoals ##################"
    for i in range(0, len(kbAndGoals)):
        kbAndGoals[i].printClause()

    print "############# goals ####################"
    for i in goals:
        i.printClause()

    print ""

    for i in kbAndGoals:
        for p1 in i.getClauseElements():
            for j in goals:
                for p2 in j.getClauseElements():
                    e1 = unifyMiddleware(p1)
                    e2 = unifyMiddleware(p2)
                    res = unify(e1, e2)
                    print "result from unifying", e1, "and", e2, "is", res

    #print "unification"
    #print unify(("r", "A"), ("r", "y"))
    #print unify(("p", "y"), ("p", ("f", "x")))


# TODO: fix
def unifyMiddleware(predicate):
    values = predicate.values
    e = [predicate.name]
    for i in predicate.values.keys():
        if isinstance(values[i], Term):
            e.append(values[i].name)
        else:
            e.append(unifyMiddleware(values[i]))
    return e


#TODO: length is always 1 more than it should be
def inputHandler(clause, start, end, kbAndGoals, isGoal=False, goals=False):
    length = end - start
    negated = False
    i = start
    #print "length is", length
    clauseElements = {}
    while i < end:
        #print "i is: ", i
        if clause[i] == "~":
            #print "hit '~' in ", i, "th element"
            negated = True
            i = i + 1

        elif clause[i] == "," or clause[i] == "(" or clause[i] == " ":
            #print "hit ',' in ", i, "th element"
            i = i+1
            continue

        elif (i+1 < length) and (clause[i+1] == "(") :
            #print "hit '(' in ", i + 1, "th element"
            neededClosed = 1
            newStart = i
            newEnd = i + 1
            k = i + 2
            while(k < length and neededClosed > 0):
                #print "k is :", k
                if (clause[k] == "("):
                    neededClosed = neededClosed + 1

                elif (clause[k] == ")"):
                    neededClosed = neededClosed -1
                    #print "hit ')', neededClosed is: ", neededClosed
                    if neededClosed == 0:
                        i = k
                        #print "hit ')' to close the predicate in ", k, "th element"
                        newEnd = k + 1
                        p = getPredicate(newStart, newEnd, clause, negated)
                        clauseElements[p.name] = p
                        negated = False
                        break
                k = k + 1

            i = i + 1

        else:
            t = getTerm(clause[i], negated)
            clauseElements[t.name] = t
            negated = False
            i = i +1

    

    c = Clause(clauseElements)

    kbAndGoals.append(c)

    if isGoal:
        print "appended to goals"
        goals.append(c)
    

# start inclusive, end exclusive
def getPredicate(start, end, clause, negated):
    name = clause[start]
    print "getPredicate called with: ", clause[start:end], "its name is: ", name
    start = start + 1
    values = {}
    i = start
    newNegated = False
    while i < end:
        #print "clause[i] is: ", clause[i], "clause[i+1] is: ", clause[i+1]
        if clause[i] == "~":
            #print "hit '~' in ", i, "th element"
            newNegated = True
            i = i + 1

        elif clause[i] == "," or clause[i] == "(" or clause[i] == " " or clause[i] == ")":
            #print "hit ',' in ", i, "th element"
            i = i+1
            continue

        elif (i+1 < end) and (clause[i+1] == "(") :
            #print "hit '(' in ", i + 1, "th element"
            neededClosed = 1
            newStart = i
            newEnd = i + 1
            k = i + 2
            while(k < end and neededClosed > 0):
                #print "k is :", k
                if (clause[k] == "("):
                    neededClosed = neededClosed + 1

                elif (clause[k] == ")"):
                    neededClosed = neededClosed -1
                    #print "hit ')', neededClosed is: ", neededClosed
                    if neededClosed == 0:
                        i = k
                        #print "hit ')' to close the predicate in ", k, "th element"
                        newEnd = k + 1
                        p = getPredicate(newStart, newEnd, clause, negated)
                        values[p.name] = p
                        newNegated = False
                        break
                k = k + 1

            i = i + 1

        else:
            t = getTerm(clause[i], newNegated)
            values[t.name] = t
            newNegated = False
            i = i +1

    predicate = Predicate(name, negated, values)

    return predicate


def getTerm(name, negated):
    print "getTerm called with ", name
    return Term(name, negated)


def main():
    inp = open('input_book.txt', 'r')
    NUMBER_OF_TESTS = int(inp.readline().split("/n")[0])
    numOfClauses, numOfGoals = (inp.readline().split("/n")[0]).split(" ")
    numOfClauses = int(numOfClauses)
    numOfGoals = int(numOfGoals)    
    print "numOfClauses ", numOfClauses
    print "numOfGoals ", numOfGoals    

    for testCaseCount in range(0, NUMBER_OF_TESTS):
        kbAndGoals = []
        goals = []
        for clauseCount in range(0, numOfClauses):
            clause = str(inp.readline().split("/n")[0])
            inputHandler(clause, 0, len(clause) - 1, kbAndGoals)
        for clauseCount in range(0, numOfGoals):
            clause = str(inp.readline().split("/n")[0])
            inputHandler(clause, 0, len(clause) - 1, kbAndGoals, True, goals)
        resolution(kbAndGoals, goals)

main()
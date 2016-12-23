from copy import copy, deepcopy
from string import ascii_uppercase
from collections import OrderedDict

# Clause has predicates as an ordered dictionary where its keys are full string names, and values are objects
# If a clause is a result of a resolution, we need their parents to backtrack print it
class Clause(object):
    def __init__(self, clauseElements, parent1=None, parent2=None):
        self.clauseElements = clauseElements
        self.size = len(self.clauseElements.keys())
        self.parent1 = parent1
        self.parent2 = parent2

    def printClause(self, returnString=False):      # returns string representation of clause in order
        res = ""
        keys = self.clauseElements.keys()
        for i in keys:
            element = self.clauseElements[i]
            if isinstance(element, Predicate):
                res = res + element.printPredicate(True) + ","
            else:
                res = res + element.printTerm()

        res = res[0:len(res)-1]
        if returnString:
            return res

    def isEqual(self, aClause):                     # checks if a clause is equal to clause object at hand
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

    def getClauseElements(self):                    # return array of clause elements
        res = []
        keys = self.clauseElements.keys()
        for i in keys:
            res.append(self.clauseElements[i])
        return res

    def printParents(self):                         # return string representation of the parents of clause
        if self.parent1:
            self.parent1.printClause()
            self.parent2.printClause()            
        else:
            return "None"

# A predicate has:
# name - function name
# negated - a flag to see if this predicate is negated or not
# values - either False or an ordered dictionary of values, can be a Term object (variable or constant) or again a Predicate
# size - how many values are there
class Predicate(object):

    def __init__(self, name, negated, values):
        self.name = name
        self.negated = negated
        self.values = values
        self.size = len(self.values.keys())

    def changeTermTo(self, termName, newValue):                 # change every termName inside predicate with newValue
        if self.name == termName:
            self.name = newValue

        for i in self.values.keys():
            value = self.values[i]

            if isinstance(value, Term) and value.name == termName:
                negatedBefore = value.negated
                newTerm = Term(newValue, negatedBefore)
                self.values[i] = newTerm

            elif isinstance(value, Predicate):
                value.changeTermTo(termName, newValue)


    def printPredicate(self, showNegated=True):                 # returns a string representation of the predicate object
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
                res = res + v.printTerm()

            if count < self.size:
                res = res + ","

        res = res + ")"
        return res

    def isEqual(self, aPredicate):                              # checks if a predicate is equal to predicate object at hand
        notSameSize = (self.size != aPredicate.size)
        notSameName =(self.name != aPredicate.name)
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

# A Term object is an atom, where it can be a variable or a constant
class Term(object):
    
    def __init__(self, name, negated):
        self.name = name
        self.negated = negated
        if name in ascii_uppercase:
            self.isConstant = True
        else:
            self.isConstant = False

    def printTerm(self):                                    # returns a string representation of the predicate object
        return self.name

    def isEqual(self, aTerm):                               # checks if a term is equal to term object at hand
        return (self.name == aTerm.name) and (self.negated == aTerm.negated)

# elements are list of atoms
def unify(element1, element2):
    len1 = len(element1)
    len2 = len(element2)    

    if  len1 != len2:
        return None
    elif element1 == element2:
        return []

    # for cases like [["f"]]
    if len1 == 1 and len2 == 1:
        if isinstance(element1[0], list):
            element1 = element1[0]
            len1 = len(element1)    
        if isinstance(element2[0], list):
            element2 = element2[0]
            len2 = len(element2)

    # for cases like ["A"] ["A"]
    if (isinstance(element1[0], str) and (element1[0] in ascii_uppercase) and len1 == 1) and (isinstance(element2[0], str) and(element2[0] in ascii_uppercase) and len2 == 1):
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
        if not (element2[0] in ascii_uppercase):
            if element2[0] in element1:
                return None
            else:
                return [[element2[0], element1[0]]]
        if not (element1[0] in ascii_uppercase):
            return [[element1[0], element2[0]]]

    f1, t1 = [element1[0]], element1[1:]
    f2, t2 = [element2[0]], element2[1:]

    z1 = unify(f1, f2)
    if z1 == None:
        return None

    g1 = apply(z1, t1)
    g2 = apply(z1, t2)

    z2 = unify(g1, g2)
    if z2 == None:
        return None

    return z1 + z2

# unifyList is a list of tuples that contains unifiers
# tupleToApply is a tuple that if it contains values to be unified, is going to be updated
def apply(unifyList, tupleToApply):
    if len(tupleToApply) == 0:
        return tupleToApply
    for u in unifyList:
        for j in tupleToApply:
            if j == u[0]:
                j = u[1]

    return tupleToApply

def substituteSingleClause(c, unification, changedPredicate1, changedPredicate2, newElements):
    if len(unification) == 0:
        keys = c.clauseElements.keys()
        for i in keys:
            if c.clauseElements[i]:
                if (not c.clauseElements[i].isEqual(changedPredicate1)) and (not c.clauseElements[i].isEqual(changedPredicate2)):
                    newElements[c.clauseElements[i].printPredicate()] = c.clauseElements[i]
    else:
        keys = c.clauseElements.keys()
        for i in keys:
            newPred = deepcopy(c.clauseElements[i])
            if (not newPred.isEqual(changedPredicate1)) and (not newPred.isEqual(changedPredicate2)):
                for unifier in unification:
                    newPred.changeTermTo(unifier[0], unifier[1])
                newElements[newPred.printPredicate()] = newPred


# substitute two clauses given the unification and the mutual predicate used for unification
def substitute(c1, c2, unification, changedPredicate1, changedPredicate2):
    if len(c1.getClauseElements()) == 1 and len(c2.getClauseElements()) == 1:
        return "contradiction"
    newElements = OrderedDict()
    
    substituteSingleClause(c1, unification, changedPredicate1, changedPredicate2, newElements)
    substituteSingleClause(c2, unification, changedPredicate1, changedPredicate2, newElements)

    newClause = Clause(newElements, c1, c2)

    return newClause 

def safeAppend(arr, clause):
    for i in arr:
        if clause.isEqual(i):
            return
    arr.append(clause)

def resolution(kbAndGoals, goals):
    resolvents = []
    for j in goals:
        for p2 in j.getClauseElements():
            for i in kbAndGoals:
                for p1 in i.getClauseElements():
                    if p1.name == p2.name and p1.negated != p2.negated:
                        e1 = unifyMiddleware(p1)
                        e2 = unifyMiddleware(p2)
                        res = unify(e1, e2)
                        if res != None:
                            copy1 = deepcopy(j)
                            copy2 = deepcopy(i)
                            newClause = substitute(copy1, copy2, res, p1, p2)
                            if newClause == "contradiction":
                                printResult(copy1, copy2)
                                return None
                            safeAppend(kbAndGoals, newClause)
                            safeAppend(goals, newClause)
                            newClause.printParents()
                            resolvents.append((j, i, newClause))
    print "no"

def printResult(lastClause1, lastClause2):
    print "yes"
    stack = [lastClause1, lastClause2]
    res = [printResolution(lastClause1, lastClause2, "empty_clause")]

    while len(stack) > 0:
        a = deepcopy(stack[len(stack)-1])
        del stack[len(stack)-1]
        if a.parent1 != None and a.parent2 != None:
            stack.append(a.parent1)
            stack.append(a.parent2)
            tempRes = printResolution(a.parent1, a.parent2, a)
            res.append(tempRes)
        
    for i in res[::-1]:
        print i


def printResolution(r0 ,r1, r2):
    if r2 == "empty_clause":
        res = r0.printClause(True) + "$" + r1.printClause(True) + "$" + "empty_clause"
    else:
        res = r0.printClause(True) + "$" + r1.printClause(True) + "$" + r2.printClause(True)

    return res

# Converts predicates to list of atoms in order for unifier to process them. i.e. p(A, f(x)) returns ['p', 'A',  ['f', 'x']]
def unifyMiddleware(predicate):
    values = predicate.values
    e = [predicate.name]
    keys = predicate.values.keys()
    for i in keys:
        if isinstance(values[i], Term):
            e.append(values[i].name)
        else:
            e.append(unifyMiddleware(values[i]))
    return e


def inputHandler(clause, start, end, kbAndGoals, isGoal=False, goals=False):
    length = end - start
    negated = False
    i = start
    clauseElements = OrderedDict()
    while i < end:
        if clause[i] == "~":
            negated = True
            i = i + 1

        elif clause[i] == "," or clause[i] == "(" or clause[i] == " ":
            i = i+1
            continue

        elif (i+1 < length) and (clause[i+1] == "(") :
            if (i-1 >= 0):
                if (clause[i-1] != "~"):
                    negated = False
                elif (clause[i-1] == "~"):
                    negated = True

            else:
                negated = False

            neededClosed = 1
            newStart = i
            newEnd = i + 1
            k = i + 2
            while(k < length and neededClosed > 0):
                if (clause[k] == "("):
                    neededClosed = neededClosed + 1

                elif (clause[k] == ")"):
                    neededClosed = neededClosed -1
                    if neededClosed == 0:
                        i = k
                        newEnd = k + 1
                        p = getPredicate(newStart, newEnd, clause, negated)
                        clauseElements[p.printPredicate()] = p
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
        goals.append(c)
    

# start inclusive, end exclusive
def getPredicate(start, end, clause, negated):
    name = clause[start]
    start = start + 1
    values = OrderedDict()
    i = start
    newNegated = negated
    while i < end:
        if clause[i] == "~":
            newNegated = True
            i = i + 1

        elif clause[i] == "," or clause[i] == "(" or clause[i] == " " or clause[i] == ")":
            i = i+1
            continue

        elif (i+1 < end) and (clause[i+1] == "(") :
            neededClosed = 1
            newStart = i
            newEnd = i + 1
            k = i + 2
            while(k < end and neededClosed > 0):
                if (clause[k] == "("):
                    neededClosed = neededClosed + 1

                elif (clause[k] == ")"):
                    neededClosed = neededClosed -1
                    if neededClosed == 0:
                        i = k
                        newEnd = k + 1
                        p = getPredicate(newStart, newEnd, clause, newNegated)
                        values[p.name] = p
                        break
                k = k + 1

            i = i + 1

        else:
            t = getTerm(clause[i], newNegated)
            values[t.name] = t
            i = i +1

    ifNegated = start - 2
    if clause[ifNegated] == "~":
        newNegated = True
    else:
        newNegated = False        
    predicate = Predicate(name, newNegated, values)

    return predicate


def getTerm(name, negated):
    return Term(name, negated)


def main():
    inp = open('input.txt', 'r')
    NUMBER_OF_TESTS = int(inp.readline().split("/n")[0])

    for testCaseCount in range(0, NUMBER_OF_TESTS):
        numOfClauses, numOfGoals = (inp.readline().split("/n")[0]).split(" ")
        numOfClauses = int(numOfClauses)
        numOfGoals = int(numOfGoals)    

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
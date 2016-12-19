# TODO: Unifier
# TODO: Set of Support structure
# TODO: Resolution algorithm altogether

# Clause has predicates as a dictionary
class Clause(object):

    def __init__(self, clauseElements):
        self.clauseElements = clauseElements

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

# A predicate has:
# a name - function name that is definitive
# negated - a flag to see if this predicate is negated or not
# values - either False or a dictionary of values, can be a term (variable or constant) or again a predicate
# numOfValues - how many values are there
class Predicate(object):

    def __init__(self, name, negated, values):
        self.name = name
        self.negated = negated
        self.values = values
        self.numOfValues = len(self.values.keys())

    def setValue(self, key, value):
        self.values[key] = value
        self.numOfValues = self.numOfValues + 1

    # For unification. It changes all the x terms inside this predicate to y
    # If found, recursively checks the predicates inside values too
    # TODO: write this method
    def changeTerms(self, x, y):
        pass

    def changeName(self, newName):
        self.name = newName

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

            if count < self.numOfValues:
                res = res + ", "

        res = res + ")"
        return res

class Term(object):

    def __init__(self, name, negated, isConstant):
        self.name = name
        self.negated = negated
        self.isConstant = isConstant

    def changeName(self, newName):
        self.name = newName

    def printTerm(self):
        return self.name


def unifier(clause1, clause2):
    pass

def resolution(kbAndGoals, goals):
    print "---in resolution---"
    print "kbAndGoals: "
    for i in kbAndGoals:
        i.printClause()
    print "goals: "
    for i in goals:
        i.printClause()

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
    #TODO: check if it's constant or not
    print "getTerm called with ", name
    return Term(name, negated, False)

def main():
    inp = open('input.txt', 'r')
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
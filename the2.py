# TODO: Inputs
# TODO: Unifier
# TODO: Set of Support structure
# TODO: Resolution algorithm altogether

# Clause has predicates as a dictionary
class Clause(object):

    def __init__(self, values):
        self.clauseElements = {}


# A predicate has:
# a name - function name that is definitive
# isNegated - a flag to see if this predicate is negated or not
# values - either False or a dictionary of values, can be a term (variable or constant) or again a predicate
# numOfValues - how many values are there
class Predicate(object):

    def __init__(self, name, isNegated, values):
        self.name = name
        self.isNegated = isNegated
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

    def __init__(self, name, isNegated, isConstant):
        self.name = name
        self.isNegated = isNegated
        self.isConstant = isConstant

    def changeName(self, newName):
        self.name = newName

    def printTerm(self):
        return self.name


def unifier(clause1, clause2):
    pass

def resolution(kbAndGoals, goals):
    pass

#TODO: length is always 1 more than it should be
def inputHandler(clause, start, end):
    print "clause is: ", clause
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

    print ""
    print "clauseElements are: "
    for i in clauseElements.keys():
        element = clauseElements[i]
        if isinstance(element, Predicate):
            print "clause has predicate: ", element.printPredicate()
        else:
            print "clause has term :", element.printTerm()
    

# start inclusive, end exclusive
def getPredicate(start, end, clause, negated):
    name = clause[start]
    print "getPredicate called with: ", clause[start:end], "its name is: ", name, "and it is negated=", negated, "start: ", start, "end: ", end
    start = start + 1
    length = end - start
    values = {}
    i = start
    while i < end:
        #print "i is: ", i
        if clause[i] == "~":
            #print "hit '~' in ", i, "th element"
            negated = True
            i = i + 1

        elif clause[i] == "," or clause[i] == "(" or clause[i] == " " or clause[i] == ")":
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
                        values[p.name] = p
                        negated = False
                        break
                k = k + 1

            i = i + 1

        else:
            t = getTerm(clause[i], negated)
            values[t.name] = t
            negated = False
            i = i +1

    predicate = Predicate(name, negated, values)

    return predicate


def getTerm(name, negated):
    #TODO: check if it's constant or not
    print "getTerm called with ", name, "and it is negated=", negated
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
        for clauseCount in range(0, numOfClauses):
            clause = str(inp.readline().split("/n")[0])
            inputHandler(clause, 0, len(clause) - 1)

main()
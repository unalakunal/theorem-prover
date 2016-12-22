#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: What if there are two predicates with the same name in the clause, or recursive predicates?
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: What if there exists a unification like x/p(y)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: What if I add an existing clause after substituting
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: change clause and predicate dictionaries to arrays, for cases like k(J,T), k(C,T    )

from copy import copy, deepcopy
from string import ascii_uppercase
import sys

# Clause has predicates as a dictionary where its keys are full string names, and values are objects
class Clause(object):
    def __init__(self, clauseElements):
        self.clauseElements = clauseElements
        self.size = len(self.clauseElements.keys())

    def printClause(self, returnString=False):
        res = ""
        keys = self.clauseElements.keys()
        for i in keys:
            element = self.clauseElements[i]
            if isinstance(element, Predicate):
                res = res + element.printPredicate(True) + ","
            else:
                res = res + element.printTerm(True)

        res = res[0:len(res)-1]
        if returnString:
            return res
        else:
            print res

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

    def getClauseElements(self):
        res = []
        keys = self.clauseElements.keys()
        for i in keys:
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

    def changeTermTo(self, termName, newValue):
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
                res = res + v.printTerm()

            if count < self.size:
                res = res + ","

        res = res + ")"
        return res

    def isEqual(self, aPredicate):
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

    def termOccurs(self, term):
        #print "see if ", term, " occurs in ", self.printPredicate()
        if self.name == term.name:
            print "True"
            return True

        else:
            keys = self.values.keys()
            for i in keys:
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

# elements are list of atoms
def unify(element1, element2):
    #print "inside unify: ", element1, element2
    len1 = len(element1)
    len2 = len(element2)    

    if  len1 != len2:
        #print "returned 191"
        return None
    elif element1 == element2:
        #print "returned 194"        
        return []

    # added for cases like [["f"]]
    if len1 == 1 and len2 == 1:
        if isinstance(element1[0], list):
            element1 = element1[0]
            len1 = len(element1)    
        if isinstance(element2[0], list):
            element2 = element2[0]
            len2 = len(element2)

    # added for cases like ["A"] ["A"]
    if (isinstance(element1[0], str) and (element1[0] in ascii_uppercase) and len1 == 1) and (isinstance(element2[0], str) and(element2[0] in ascii_uppercase) and len2 == 1):
        #print "returned 208"
        return None

    #if len1 > 1 and len2 > 1 and element1[0] != element2[0]:
    #    return None

    if len1 == 1:
        if element1 == element2:
            #print "returned 216"                    
            return []
        if not (element1[0] in ascii_uppercase):
            if element1[0] in element2:
                #print "returned None in 220"                
                return None
            else:
                #print "returned 223"        
                return [[element1[0], element2[0]]]
        if not (element2[0] in ascii_uppercase):
            #print "returned 226"                
            return [[element2[0], element1[0]]]

    if len2 == 1:
        if element2 == element1:
            #print "returned 231"
            return []
        if not (element2[0] in ascii_uppercase):
            if element2[0] in element1:
                #print "returned 235"                                
                return None
            else:
                #print "returned 238"        
                return [[element2[0], element1[0]]]
        if not (element1[0] in ascii_uppercase):
            #print "returned 241"
            return [[element1[0], element2[0]]]

    f1, t1 = [element1[0]], element1[1:]
    f2, t2 = [element2[0]], element2[1:]

    z1 = unify(f1, f2)
    #print "z1 is", z1

    if z1 == None:
        #print "returned 251"        
        return None

    g1 = apply(z1, t1)
    g2 = apply(z1, t2)

    #print "g1 ", g1, "g2 ", g2

    z2 = unify(g1, g2)

    if z2 == None:
        #print "returned 262"
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

def substituteSingleClause(c, unification, changedPredicate1, changedPredicate2, newElements):
    if len(unification) == 0:
        #print "unification returned empty list"
        keys = c.clauseElements.keys()
        for i in keys:
            if c.clauseElements[i]:
                if (not c.clauseElements[i].isEqual(changedPredicate1)) and (not c.clauseElements[i].isEqual(changedPredicate2)):
         #           print "and has a chance to be in newElements where changedPredicate1",changedPredicate1.printPredicate(), "changedPredicate2", changedPredicate2.printPredicate()
                    newElements[c.clauseElements[i].printPredicate()] = c.clauseElements[i]
    else:
        keys = c.clauseElements.keys()
        for i in keys:
            # TODO: unify to predicate
            newPred = deepcopy(c.clauseElements[i])
          #  print "newPred is ", newPred.printPredicate()
            if (not newPred.isEqual(changedPredicate1)) and (not newPred.isEqual(changedPredicate2)):
                for unifier in unification:
                    newPred.changeTermTo(unifier[0], unifier[1])
           #     print "and has a chance to be in newElements where changedPredicate1",changedPredicate1.printPredicate(), "changedPredicate2", changedPredicate2.printPredicate()
                newElements[newPred.printPredicate()] = newPred


# substitute two clauses given the unification and the mutual predicate used for unification
def substitute(c1, c2, unification, changedPredicate1, changedPredicate2):
    #print "in substitute with", changedPredicate1.printPredicate(), changedPredicate2.printPredicate(), "where unification is: ", unification 
    if len(c1.getClauseElements()) == 1 and len(c2.getClauseElements()) == 1:
     #   print "got contradiction where c1 is", c1.printClause(), "c2 is ", c2.printClause()
        return "contradiction"
    newElements = {}
    #print "substituting", c1.printClause(), "and", c2.printClause()
    
    substituteSingleClause(c1, unification, changedPredicate1, changedPredicate2, newElements)
    substituteSingleClause(c2, unification, changedPredicate1, changedPredicate2, newElements)

    print "returning newElements as", newElements
    newClause = Clause(newElements)

    return newClause 

def safeAppend(arr, clause):
    for i in arr:
        if clause.isEqual(i):
            return
    arr.append(clause)
    

def resolution(kbAndGoals, goals):
    print "############# kbAndGoals ##################"
    for i in range(0, len(kbAndGoals)):
        kbAndGoals[i].printClause()

    print "############# goals ####################"
    for i in goals:
        i.printClause()

    print ""
    print "------------fun begins------------"    

    count = 1
    resolvents = []
    for j in goals:
        print "selected goal element is", j.printClause()
        for p2 in j.getClauseElements():
            print "selected predicate from goal is", p2.printPredicate()    
            for i in kbAndGoals:
                print "selected kbAndGoals element is", i.printClause()
                for p1 in i.getClauseElements():
                    if p1.name == p2.name and p1.negated != p2.negated:
                        print "p1 and p2 are unifiable where p1:", p1.printPredicate(True), "p2:", p2.printPredicate(True)
                        e1 = unifyMiddleware(p1)
                        e2 = unifyMiddleware(p2)
                        res = unify(e1, e2)
                        print "result of unification", res
                        if res != None:
                            copy1 = deepcopy(i)
                            copy2 = deepcopy(j)
                            print "copy1 is", copy1.printClause(), "copy2 is ", copy2.printClause()
                            newClause = substitute(copy1, copy2, res, p1, p2)
                            if newClause == "contradiction":
                                print "reached contradiction from", copy1.printClause(), copy2.printClause()
                                resolvents.append(("yes", j, i))
                                printResolvents(resolvents)
                                return None
                            print "newClause", count, newClause.printClause()
                            count = count + 1
                            print "before appending", len(kbAndGoals), len(goals)
                            safeAppend(kbAndGoals, newClause)
                            safeAppend(goals, newClause)
                            print "after appending", len(kbAndGoals), len(goals)                            
                            resolvents.append((j, i, newClause))

    print "no"

def printResolvents(res):
    print "yes"
    for i in range(0, len(res)):
        if isinstance(res[i][0], Clause):
            sys.stdout.write(res[i][0].printClause(True))
            sys.stdout.write("$")
            sys.stdout.write(res[i][1].printClause(True))
            sys.stdout.write("$")            
            sys.stdout.write(res[i][2].printClause(True))        
            sys.stdout.write("\n")
        else:
            sys.stdout.write(res[i][1].printClause(True))
            sys.stdout.write("$")
            sys.stdout.write(res[i][2].printClause(True))            
            sys.stdout.write("$")
            sys.stdout.write("empty_clause")
            sys.stdout.write("\n")            


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
            if (i-1 >= 0):
                if (clause[i-1] != "~"):
                    negated = False
                elif (clause[i-1] == "~"):
                    negated = True

            else:
                negated = False

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
        print "appended to goals"
        goals.append(c)
    

# start inclusive, end exclusive
def getPredicate(start, end, clause, negated):
    name = clause[start]
    start = start + 1
    values = {}
    i = start
    newNegated = negated
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
    #print "getTerm called with ", name
    return Term(name, negated)


def main():
    inp = open('input_book.txt', 'r')
    NUMBER_OF_TESTS = int(inp.readline().split("/n")[0])
    numOfClauses, numOfGoals = (inp.readline().split("/n")[0]).split(" ")
    numOfClauses = int(numOfClauses)
    numOfGoals = int(numOfGoals)    
    #print "numOfClauses ", numOfClauses
    #print "numOfGoals ", numOfGoals    

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
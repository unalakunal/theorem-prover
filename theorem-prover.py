#!/usr/bin/env python

######################################################
#
# theorem-prover - theorem prover for predicate logic
# written by Unal Akunal (unal.akunal@gmail.com)
#
######################################################

from copy import deepcopy
from string import ascii_uppercase
from collections import OrderedDict
import argparse
from lib.Clause import Clause
from lib.Predicate import Predicate
from lib.Literal import Literal

def unify(element1, element2):
    len1 = len(element1)
    len2 = len(element2)

    if len1 != len2:
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
        if not element1[0] in ascii_uppercase:
            if element1[0] in element2:
                return None
            else:
                return [[element1[0], element2[0]]]
        if not element2[0] in ascii_uppercase:
            return [[element2[0], element1[0]]]

    if len2 == 1:
        if element2 == element1:
            return []
        if not element2[0] in ascii_uppercase:
            if element2[0] in element1:
                return None
            else:
                return [[element2[0], element1[0]]]
        if not element1[0] in ascii_uppercase:
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
# tupleToApply is a tuple that if it contains values to be unified, is
# going to be updated

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
                    newElements[c.clauseElements[i].printPredicate()] = c.clauseElements[
                        i]
    else:
        keys = c.clauseElements.keys()
        for i in keys:
            newPred = deepcopy(c.clauseElements[i])
            if (not newPred.isEqual(changedPredicate1)) and (not newPred.isEqual(changedPredicate2)):
                for unifier in unification:
                    newPred.changeLiteralTo(unifier[0], unifier[1])
                newElements[newPred.printPredicate()] = newPred

# substitute two clauses given the unification and the mutual predicate
# used for unification

def substitute(c1, c2, unification, changedPredicate1, changedPredicate2):
    if len(c1.getClauseElements()) == 1 and len(c2.getClauseElements()) == 1:
        return "contradiction"
    newElements = OrderedDict()

    substituteSingleClause(
        c1, unification, changedPredicate1, changedPredicate2, newElements)
    substituteSingleClause(
        c2, unification, changedPredicate1, changedPredicate2, newElements)

    newClause = Clause(newElements, c1, c2)

    return newClause


def safeAppend(arr, clause):
    for i in arr:
        if clause.isEqual(i):
            return False
    arr.append(clause)
    return True


def resolution(args, kbAndGoals, goals):
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
                            check1 = safeAppend(kbAndGoals, newClause)
                            check2 = safeAppend(goals, newClause)
                            if check1 and check2 and args['all']:
                                s = copy1.printClause(
                                    True) + "$" + copy2.printClause(True) + "$" + newClause.printClause(True)
                                print s

    print "Goal set can not be derived from the knowledge base set"


def printResult(lastClause1, lastClause2):
    print "\nGoals can be inferred from the knowledge base with the following refutation steps:"
    stack = [lastClause1, lastClause2]
    res = [printResolution(lastClause1, lastClause2, "empty_clause")]

    while len(stack) > 0:
        a = deepcopy(stack[len(stack) - 1])
        del stack[len(stack) - 1]
        if a.parent1 != None and a.parent2 != None:
            stack.append(a.parent1)
            stack.append(a.parent2)
            tempRes = printResolution(a.parent1, a.parent2, a)
            res.append(tempRes)

    for i in res[::-1]:
        print i


def printResolution(r0, r1, r2):
    if r2 == "empty_clause":
        res = r0.printClause(True) + "$" + \
            r1.printClause(True) + "$" + "empty_clause"
    else:
        res = r0.printClause(True) + "$" + \
            r1.printClause(True) + "$" + r2.printClause(True)

    return res

# Converts predicates to list of atoms in order for unifier to process
# them. i.e. p(A, f(x)) returns ['p', 'A',  ['f', 'x']]


def unifyMiddleware(predicate):
    values = predicate.values
    e = [predicate.name]
    keys = predicate.values.keys()
    for i in keys:
        if isinstance(values[i], Literal):
            e.append(values[i].name)
        else:
            e.append(unifyMiddleware(values[i]))
    return e


def searchThroughLoop(start, end, clause, newNegated):
    elements = OrderedDict()
    i = start
    while i < end:
        if clause[i] == "~":
            newNegated = True
            i = i + 1

        elif clause[i] == "," or clause[i] == "(" or clause[i] == " " or clause[i] == ")":
            i = i + 1
            continue

        elif (i + 1 < end) and (clause[i + 1] == "("):
            neededClosed = 1
            newStart = i
            newEnd = i + 1
            k = i + 2
            while k < end and neededClosed > 0:
                if clause[k] == "(":
                    neededClosed = neededClosed + 1
                elif clause[k] == ")":
                    neededClosed = neededClosed - 1
                    if neededClosed == 0:
                        i = k
                        newEnd = k + 1
                        p = getPredicate(newStart, newEnd, clause, newNegated)
                        elements[p.printPredicate()] = p
                        newNegated = False
                        break
                k = k + 1
            i = i + 1

        else:
            t = Literal(clause[i], newNegated)
            elements[t.name] = t
            i = i + 1

    return elements


def inputHandler(args, clause, start, end, kbAndGoals, isGoal=False, goals=[]):
    length = end - start
    newNegated = False

    elements = searchThroughLoop(start, end, clause, newNegated)

    c = Clause(elements)
    if args['negated']:
        c.negateClause()

    kbAndGoals.append(c)
    if isGoal:
        goals.append(c)


def getPredicate(start, end, clause, negated):
    name = clause[start]
    start = start + 1
    newNegated = negated

    elements = searchThroughLoop(start, end, clause, newNegated)

    ifNegated = start - 2
    if clause[ifNegated] == "~":
        newNegated = True
    else:
        newNegated = False
    predicate = Predicate(name, newNegated, elements)

    return predicate


def readSingleFile(args):
    inp = args['input'][0]
    NUMBER_OF_TESTS = int(inp.readline().split("/n")[0])

    for testCaseCount in range(0, NUMBER_OF_TESTS):
        numOfClauses, numOfGoals = (inp.readline().split("/n")[0]).split(" ")
        numOfClauses = int(numOfClauses)
        numOfGoals = int(numOfGoals)

        kbAndGoals = []
        goals = []
        for clauseCount in range(0, numOfClauses):
            clause = str(inp.readline().split("/n")[0])
            inputHandler(args, clause, 0, len(clause) - 1, kbAndGoals)
        for clauseCount in range(0, numOfGoals):
            clause = str(inp.readline().split("/n")[0])
            inputHandler(args, clause, 0, len(clause) -
                         1, kbAndGoals, True, goals)
        resolution(args, kbAndGoals, goals)


def createParser():
    parser = argparse.ArgumentParser(
        description='Theorem prover for first order predicate logic using resolution refutation')
    parser.add_argument('input', type=file, nargs='*',
                        help='the file that contains initial clauses in the knowledge base and the goal set of the theorem')
    parser.add_argument('-a', '--all', help='display all the resolutions of this algorithm',
                        action='store_true')
    # TODO:
    # parser.add_argument('-m', '-multiple', help='work with a single file for multiple iterations',
    #                     action='readMultipleFiles')
    parser.add_argument('-n', '--negated', help='negates the goal if the goal set clauses are not already given in negated form',
                        action='store_true')
    return parser


def runCommandLine():
    parser = createParser()
    args = vars(parser.parse_args())
    if not args['input']:
        parser.print_help()  # default message if not provided any input file
    else:
        readSingleFile(args)

if __name__ == '__main__':
    runCommandLine()

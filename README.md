# Autonomous-Theorem-Prover
A theorem prover for First Order Predicate Logic using resolution refutation technique and set of support strategy.

## What the algorithm does
Briefly,  
1. Parses the knowledge base and goal sets, creates classes accordingly as a clause per line.  
2. Iterating over goal set and (knowledge base + goal) sets, using unification routine, tries to find a new resolution.  
* Explained in detail: http://www-cs.ccny.cuny.edu/~cssjl/AI1Lectures/Lesson10.pdf  
3. Halts when a contradiction is reached. Prints resolutions top to bottom with "$"s.  

Details are nicely explained in this link: https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-825-techniques-in-artificial-intelligence-sma-5504-fall-2002/lecture-notes/Lecture8FinalPart1.pdf

## Usage

    usage: theorem-prover.py [-h] [-a] [-n] [input [input ...]]

    Theorem prover for first order predicate logic using resolution refutation

    positional arguments:
      input          the file that contains initial clauses in the knowledge base
                     and the goal set of the theorem

    optional arguments:
      -h, --help     show this help message and exit
      -a, --all      display all the resolutions of this algorithm
      -n, --negated  negates the goal if the goal set clauses are not already given in negated form

## Input Format
Input is a file with knowledge base and goal clauses. By default, it is assumed that the goal clause(s) are negated; if not, you can use -n flag to specify the program to handle negation itself.

## Output Format
Prints resolutions step by step as:   [clause1]$[clause2]$[newClause]  

## Example
* Input:  

  Knowledge base:  
  ~a(x),s(x)  
  ~c(y),~f(x),a(x)  
  c(F)  
  f(M)  
  Goals (given as negated):  
  ~s(M)  

* Output:  

  ~s(M)$~a(x),s(x)$~a(M)  
  ~a(M)$~c(y),~f(x),a(x)$~c(y),~f(M)  
  ~c(y),~f(M)$c(F)$~f(M)  
  ~f(M)$f(M)$empty_clause  

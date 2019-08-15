#!/usr/bin/env python

"""Usage: pass_test.py  infile passfile [outpath]

Updates test execution failed result to pass in an output XML file (to PASS tests that have been fixed manually).

requires an input file with one test per line, and tab separated info: the long name of the test, the desired status and a comment for auditing 
This is the format of the _Already_Run.txt file
"TestCases.Tests.1.My Test 12	PASS   Manually validated by xyz"

Optional `outpath` specifies where to write processed results. If not given,
results are written over the original file.
"""

import sys
from robot.api import ExecutionResult, ResultVisitor


class pass_test(ResultVisitor):

    def __init__(self, ttopass):
        self.ttopass = ttopass

    def visit_test(self, test):
            if test.status == "FAIL":
                status=""
                comment=""
                t = [i for i in self.ttopass if i.startswith(test.longname)]
                if len(t) <> 0: # current test found in the override list          
                # get Status and comment 
                    fields = t[0].split("\t")
                    if len(fields) >= 2:
                        status=fields[1]
                    if len(fields) >= 3:
                        comment=fields[2]

                if status == 'PASS' and comment<>'':
                    test.status = 'PASS'
                    test.message = comment
                    print ("Updt FAILED Test: " + test.longname + " -> " + status + " -> " + comment) 
                else:
                    print ("Keep FAILED Test: " + test.longname + " -> " + status + " -> " + comment) 


def check_tests(infile, passfile, outpath=None):
    with open(passfile) as f:
        ttopass = f.readlines()
    ttopass = [x.strip() for x in ttopass ]

    result = ExecutionResult(infile)
    result.visit(pass_test(ttopass))
    result.save(outpath)


if __name__ == '__main__':
    try:
        check_tests(*sys.argv[1:])
    except TypeError:
        print __doc__
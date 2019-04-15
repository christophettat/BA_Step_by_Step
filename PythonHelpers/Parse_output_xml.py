"""Usage: check_test_times.py seconds inpath [outpath]

Reads test execution result from an output XML file and checks that no test
took longer than given amount of seconds to execute.

Optional `outpath` specifies where to write processed results. If not given,
results are written over the original file.
"""

import sys
from robot.api import ExecutionResult, ResultVisitor


class MyVisitor(ResultVisitor):

    def __init__(self, SuitePath, logger):
        self.SuitePath = SuitePath
        self.logger=logger

    def visit_suite(self, suite):
        for t in suite.tests:
            m = self.SuitePath + "/" + suite.name + "/" + t.name
            for tag in t.tags:
                if tag.startswith("scheduler_"):
                    # translate the tag to an execution time for next step


                    m = m + "\t" + tag
            print m
            self.logger.logln(m)
        suite.suites.visit(MyVisitor(self.SuitePath + "/" +  suite.name, self.logger))


class my_logger():
    def __init__(self, filename):
        self.f=open(filename,"w+")

    def logln(self, line):
        self.f.write(line + "\n")
    def close(self):
        self.f.close()

def check_tests(inpath, outpath):
    result = ExecutionResult(inpath)
    l=my_logger(outpath)
    result.visit(MyVisitor("", l))
    l.close()
    print "All Done"

if __name__ == '__main__':
    try:
        check_tests(*sys.argv[1:])
    except TypeError:
        print __doc__
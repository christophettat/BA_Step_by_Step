"""Parses an output.xml file to generate a list of all executed tests, with their tag matching next_at.... pattern
   the output of this utility will be used to skip those tests in a next execution
"""

import sys
from robot.api import ExecutionResult, ResultVisitor
import re


class my_scanner():
    def __init__(self, xml):
        self.result = ExecutionResult(xml)

    def test_in_suite(self, path):
        return self.crawl_suites(self.result.suite,path)
    
    def crawl_suites(self,suite,path):
        tests=None
        for s in suite.suites:
            if path == s.longname: # we found the test folder, lets return tests
                tests= s.tests
                break 
            if path.startswith(s.longname): # we are on the good path, go down
                tests = self.crawl_suites(s,path)
                break
        return tests


def check_tests(inpath,O):
    l=my_scanner(inpath)
    a=l.test_in_suite('TestCases.Tests.1')
    print ("All Done")

if __name__ == '__main__':
    try:
        check_tests(*sys.argv[1:])
    except TypeError:
        print (__doc__)
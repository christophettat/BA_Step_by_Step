"""Pre-run modifier that:
- excludes first tests already executed in a suite (based on input file)
- keeps the next test in suite for execution (if matching scheduling information)
- excludes all subsequent tests in suite

This is used in test patterns trying to resolve the problem of asynchronous system testing with (large) delays between steps.
Each test in a suite is considered a step, to be executed at the right time.

"""

from robot.api import SuiteVisitor
from robot.utils import Matcher
import re



class suite_tests_filter(SuiteVisitor):

    def __init__(self, fname):
        # load the tests already executed
        with open(fname) as f:
            self.tests = f.readlines()
        self.tests = [x.strip() for x in self.tests ]
        #remove leading / if any
        self.tests = [x.strip('/') for x in self.tests]

    def start_suite(self, suite):

        #suite.suites = [s for s in suite.suites if self._to_keep(s)]
        found_test = False #will be set to true once a test will have been selected for running in this suite
        run_at = ""
        test_to_keep = []
        for t in suite.tests:
            if self._to_drop(t):
                # skipping tests already executed
                #Tag = self._get_tag(t)
                print "already executed " + t.name
            elif not found_test:
                # run this test if time is okay (according to Tag)
                test_to_keep.append(t)
                found_test = True
                print "to execute now " + t.name
            else:
                #drop all subsequent tests from this run
                print "to execute later " + t.name
        suite.tests = test_to_keep




    def _to_drop(self, test):

        testname = self._full_path(test)
        result = [i for i in self.tests if i.startswith(testname)]

        if len(result) <>0:
            print(testname + "----- was already executed and to drop")
            return True
        else:
            print(testname + "----- was not executed and to consider for running")
            return False


    def _full_path(self, test):
        """Returns the full path and name of the current test"""
        fpath=test.name
        parent = test.parent
        while not parent is None:
            fpath=parent.name + '/' + fpath
            parent = parent.parent
        return fpath


    def end_suite(self, suite):
        """Remove suites that are empty after removing tests."""
        suite.suites = [s for s in suite.suites if s.test_count > 0]

    def visit_test(self, test):
        """Avoid visiting tests and their keywords to save a little time."""
        pass

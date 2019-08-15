"""Pre-run modifier that:
- excludes first tests already executed in a suite (based on input file)
- keeps the next test in suite for execution (if matching scheduling information)
- excludes all subsequent tests in suite

This is used in test patterns trying to resolve the problem of asynchronous system testing with (large) delays between steps.
Each test in a suite is considered a step, to be executed at the right time.

"""

from robot.api import SuiteVisitor
from robot.utils import Matcher
from datetime import datetime
import re



class suite_tests_filter(SuiteVisitor):

    def __init__(self, donefile, pendingfile):
        # load the tests already executed
        with open(donefile) as f:
            self.tests = f.readlines()
        self.tests = [x.strip() for x in self.tests ]

        #open a file to list pending tests 
        self.pendingfile = open(pendingfile,"w")

    def start_suite(self, suite):

        #suite.suites = [s for s in suite.suites if self._to_keep(s)]
        found_test = False #will be set to true once a test will have been selected for running in this suite
        laststatus=""
        self.next_at = "" # will contain the latest time constraint set in the tests
        test_to_keep = []
        for t in suite.tests:
            prevresult = [i for i in self.tests if i.startswith(t.longname)]
            if len(prevresult) <> 0: # skipping tests already executed                
                # get status and tags of run 
                fields = prevresult[0].split("\t")
                print (fields[1] + " - " + t.longname)  # this is status (PASS FAIL)
                if len(fields)>2:
                    self.next_at = fields[2]            # this is date/time part of tag next_at_YYYYMMDDHHMMSS 
                if fields[1] == "FAIL":                 # do not consider tests after a a failed one
                    found_test = True  
                    laststatus = "FAIL"
                    
            elif not found_test:  # run this test if time is okay (according to time constraints)
                found_test = True
                #waitfor = datetime.strptime( self.next_at, '%Y%m%d%H%M%S')
                if self.next_at == "": # no constraints, let"s run it
                    test_to_keep.append(t)
                    print ("EXEC - " + t.longname)
                elif datetime.strptime( self.next_at, '%Y%m%d%H%M%S') <= datetime.now():  # time to run it
                    test_to_keep.append(t)
                    print ("EXEC - " + t.longname)
                else:
                    print ("WAIT - " + t.longname)
                    self.pendingfile.write("WAIT - " + t.longname + "\n")
            else:
                #drop all subsequent tests from this run
                if not laststatus == "FAIL":
                    print ("TODO - " + t.longname )
                    self.pendingfile.write("TODO - " + t.longname + "\n")
                else:
                    print ("FAIL - " + t.longname )
                    self.pendingfile.write("FAIL - " + t.longname + "\n")

        suite.tests = test_to_keep


    def end_suite(self, suite):
        """Remove suites that are empty after removing tests."""
        suite.suites = [s for s in suite.suites if s.test_count > 0]


    def visit_test(self, test):
        """Avoid visiting tests and their keywords to save a little time."""
        pass

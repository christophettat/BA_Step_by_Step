"""Pre-run modifier that:
- excludes first tests already executed in a suite (based on input file)
- keeps the next test in suite for execution (if matching scheduling information)
- excludes all subsequent tests in suite

This is used in test patterns trying to resolve the problem of asynchronous system testing with (large) delays between steps.
Each test in a suite is considered a step, to be executed at the right time.

"""

from robot.api import SuiteVisitor
from robot.api import ExecutionResult
from robot.utils import Matcher
from datetime import datetime
import re
import os.path

class my_output_xml_parser():
    def __init__(self, xml):
        if os.path.isfile(xml):
            self.xmlfile=True
            self.result = ExecutionResult(xml)
        else:
            self.xmlfile=False

    def test_in_suite(self, path):
        if self.xmlfile:
            return self.crawl_suites(self.result.suite,path)
        else:
            return []

    def crawl_suites(self,suite,path):
        tests=[]
        for s in suite.suites:
            if path == s.longname: # we found the test folder, lets return tests
                tests= s.tests
                break 
            if path.startswith(s.longname): # we are on the good path, go down
                tests = self.crawl_suites(s,path)
                break
        return tests



class suite_tests_filter_V2(SuiteVisitor):

    def __init__(self, output_xml_file, StateSummary):
        # load the tests already executed
        SS=os.path.splitext(StateSummary)[0]
        
        try:
            os.remove(ss + '.log')
            os.remove(ss.run)
        except OSError:
            pass
        
        self.StateSummary = open(SS +'.log','w')
        self.parser= my_output_xml_parser(output_xml_file)
        

    def mylogger(self,msg):
        print(msg)
        self.StateSummary.write(msg + "\n")

    def start_suite(self, suite):
        run_tests=self.parser.test_in_suite(suite.longname) # get the list of already executed tests in this suite
        found_test = False #will be set to true once a test will have been selected for running in this suite
        laststatus=""
        self.next_at = "" # will contain the latest time constraint set in the tests
        test_to_keep = [] 
        for t in suite.tests:
            prevresult = [i for i in run_tests if i.longname.startswith(t.longname)]
            if len(prevresult) !=  0: # skipping tests already executed                
                # get status and tags of previous run 
                self.mylogger (prevresult[0].status + " - " + t.longname)  # this is status (PASS FAIL)
                # now look for a Tag with special meaning (tagging a test will influence behaviour of the next test in the suite like wait for a timer to expire)
                for tag in prevresult[0].tags:
                    matchTag = re.match( r'^next_at_([0-9]{14})$', tag)
                    if matchTag:
                        m = m + "\t" + matchTag.group(1)
                        self.mylogger ("next@: " + m)                
                        self.mylogger ("next@: " + m)                
                        self.next_at = m            # this is date/time part of tag next_at_YYYYMMDDHHMMSS 
                if prevresult[0].status == "FAIL":                 # do not consider tests after a a failed one
                    found_test = True  
                    laststatus = "FAIL"
                    
            elif not found_test:  # run this test if time is okay (according to time constraints)
                found_test = True
                #waitfor = datetime.strptime( self.next_at, '%Y%m%d%H%M%S')
                if self.next_at == "": # no constraints, let"s run it
                    test_to_keep.append(t)
                    self.mylogger ("EXEC - " + t.longname)
                elif datetime.strptime( self.next_at, '%Y%m%d%H%M%S') <= datetime.now():  # time to run it
                    test_to_keep.append(t)
                    self.mylogger ("EXEC - " + t.longname)
                else:
                    self.mylogger ("WAIT - " + t.longname)
            else:
                #drop all subsequent tests from this run
                if not laststatus == "FAIL":
                    self.mylogger ("TODO - " + t.longname )
                else:
                    self.mylogger ("FAIL - " + t.longname )

        suite.tests = test_to_keep


    def end_suite(self, suite):
        """Remove suites that are empty after removing tests."""
        suite.suites = [s for s in suite.suites if s.test_count > 0]


    def visit_test(self, test):
        """Avoid visiting tests and their keywords to save a little time."""
        pass

import os
import time
from robot.libraries.BuiltIn import BuiltIn
import json
import hashlib


class Variables_Saver(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, subdir='./RunState'):
        self.UID = ""
        self.subdir=subdir

    def start_suite(self, data, result):
            UID=hashlib.md5(data.longname).hexdigest()
            self.varfile= os.path.join(self.subdir, UID + ".json")
            print "Variable file is :", self.varfile

    def start_test(self, data, result):
        #print "************* Starting test exect\n"
        if os.path.isfile(self.varfile):
            load_vars(self.varfile)

    def end_test(self, data, result):
        #print "************* TEST COMPLETE \n"
        save_vars(self.varfile)
        
def save_vars(vfile):
		d = BuiltIn().get_variables()
		#remove all system and object variables
		unwanted= ['${TEST_MESSAGE}', '${TEST_STATUS}', '${/}','${:}',"${\\n}",'${DEBUG_FILE}','${EXECDIR}','${False}','${LOG_FILE}','${LOG_LEVEL}','${None}','${null}','${OUTPUT_DIR}','${OUTPUT_FILE}','${PREV_TEST_MESSAGE}','${PREV_TEST_NAME}','${PREV_TEST_STATUS}','${REPORT_FILE}','${SPACE}','${SUITE_DOCUMENTATION}','${SUITE_NAME}','${SUITE_SOURCE}','${TEMPDIR}','${TEST_DOCUMENTATION}','${TEST_NAME}','${True}','&{SUITE_METADATA}','@{TEST_TAGS}']
		vars=dict()
		keys= d.keys()
		for k in keys:
			if not (k[0:2] == '__') and not (k in unwanted):
				vars[k]= d[k]
				#print (k, ' * ', vars[k], type(vars[k]), "\n")
                
        #print(json.dumps(vars, sort_keys=True, indent=4))
		a=open(vfile,'w')
		print(json.dump(vars,a, sort_keys=True, indent=4))
		#print ('********')
		a.close()

def load_vars(vfile):
    vars = json.load(open(vfile))
    keys= vars.keys()
    for k in keys:
        BuiltIn().set_test_variable( k, vars[k])


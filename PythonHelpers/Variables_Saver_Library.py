import os
import time
from uuid import UUID
from robot.libraries.BuiltIn import BuiltIn
import json
import hashlib
import redis

class Variables_Saver_Library(object):
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self, host='localhost', port='6379'):
        self.redis = redis.Redis( host= host, port= port)

    def save_vars(self):
        """This keywords saves all variables from current test in a redis structure:
        -- identified by a hash of the testsuite name (TODO a better hash in case of multibranch runs) 
        -- associated and ordered via time of logging"""
        now=time.time()    

        SuiteName=BuiltIn().get_variable_value('${SUITE_NAME}')
        UID=hashlib.md5(SuiteName.encode('utf-8')).hexdigest()

        d = BuiltIn().get_variables()
        #remove all system and object variables
        unwanted= ['${TEST_MESSAGE}', '${TEST_STATUS}', '${/}','${:}',"${\\n}",'${DEBUG_FILE}','${EXECDIR}','${False}','${LOG_FILE}','${LOG_LEVEL}','${None}','${null}','${OUTPUT_DIR}','${OUTPUT_FILE}','${PREV_TEST_MESSAGE}','${PREV_TEST_NAME}','${PREV_TEST_STATUS}','${REPORT_FILE}','${SPACE}','${SUITE_DOCUMENTATION}','${SUITE_NAME}','${SUITE_SOURCE}','${TEMPDIR}','${TEST_DOCUMENTATION}','${TEST_NAME}','${True}','&{SUITE_METADATA}','@{TEST_TAGS}']
        vars=dict()
        keys= d.keys()
        for k in keys:
            if not (k[0:2] == '__') and not (k in unwanted):
                vars[k]= d[k]
                #print (k, ' * ', vars[k], type(vars[k]), "\n")

        jsonvars = json.dumps( vars )        
        
        self.redis.zadd(UID, {jsonvars : now})
        InStock=self.redis.zcard(UID)
        print(InStock)

    def load_vars(self, LastXMinutes=60):
        """This keywords loads the variables from the oldest test found in a redis structure:
        -- identified by a hash of the testsuite name - must the the same signature as previous keywords (TODO a better hash in case of multibranch runs) 
        -- older than x minutes (x is passed as optional argument defauls it 60 Mins)
        -- the keyword can be run mutliple times, it returns true if variables have been set, false if no more tests was found in range"""
        TimeRangeStart=time.time()-60*LastXMinutes

        SuiteName=BuiltIn().get_variable_value('${SUITE_NAME}')
        UID=hashlib.md5(SuiteName.encode('utf-8')).hexdigest()

        InStock=self.redis.zcard(UID)
        contexts=self.redis.zrangebyscore(UID, 0, TimeRangeStart)
        
        if len(contexts)>0:
            firstContext=contexts[0]
            self.redis.zrem(UID, firstContext)
            vars = json.loads(firstContext)
            keys= vars.keys()
            for k in keys:
                BuiltIn().set_test_variable( k, vars[k])
            return True
        else:
            return False


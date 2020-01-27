   echo "******************** Determine tests that have run" 
    REM create an exclusion file for what was executed
 python ./PythonHelpers/Parse_output_xml.py ./Results/output.xml ./RunState/_Already_Run.txt
    echo "******************** Run"
    REM run tests with filter (should execute first step not yet executed of each suite)
    robot  --argumentfile ./params.txt
    echo "******************** Rebot"
    rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
    del %~dp0Results\output.xml
    ren %~dp0Results\out.xml output.xml




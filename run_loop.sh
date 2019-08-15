   echo "******************** Determine tests that have run" 
    # create an exclusion file for what was executed
    /usr/bin/python ./PythonHelpers/Parse_output_xml.py ./Results/output.xml ./RunState/_Already_Run.txt
    echo "******************** Run"
    # run tests with filter (should execute first step not yet executed of each suite)
    robot  --argumentfile ./params.txt
    echo "******************** Rebot"
    rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
    mv ./Results/out.xml ./Results/output.xml

while [[ $(grep -v '^FAIL' ./RunState/_To_Run.txt | wc -l ) -ge 1 ]]
do 
    echo "******************** Sleep 30 secs"
    sleep 30
    echo "******************** Determine tests that have run" 
    # create an exclusion file for what was executed
    /usr/bin/python ./PythonHelpers/Parse_output_xml.py ./Results/output.xml ./RunState/_Already_Run.txt
    echo "******************** Run"
    # run tests with filter (should execute first step not yet executed of each suite)
    robot  --argumentfile ./params.txt
    echo "******************** Rebot"

    rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
    mv ./Results/out.xml ./Results/output.xml


done


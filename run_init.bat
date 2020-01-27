REM empty  the list of executed tests 
del -r ./Results/*
del -r ./RunState/*
echo. 2> ./RunState/_Already_Run.txt


REM run tests with empty filter (should execute first step of each suite only)
echo "******************** Run #1"
robot  --argumentfile ./params.txt
echo "******************** Rebot #1"
rebot --report NONE --log NONE --output ./Results/output.xml --merge ./Results/output_current.xml

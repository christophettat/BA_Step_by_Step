# empty  the list of executed tests 
rm -r ./Results/*
rm -r ./RunState/*
cat /dev/null > ./RunState/_Already_Run.txt
cat "BOOSTRAP STRING" > ./RunState/_To_Run.txt


while [[ $(wc -l <./RunState/_To_Run.txt) -ge 2 ]]
do 
# run tests with empty filter (should execute first step of each suite only)
echo "******************** Run #1"
robot  --argumentfile ./params.txt
echo "******************** Rebot #1"
rebot --report NONE --log NONE --output ./Results/output.xml --merge ./Results/output_current.xml
echo "******************** Parsing #1"
# create an exclusion file for what was executed
/usr/bin/python ./PythonHelpers/Parse_output_xml.py ./Results/output.xml ./RunState/_Already_Run.txt

done

echo "******************** Run #2"
# run tests with filter (should execute first step not yet executed of each suite)
robot  --argumentfile ./params.txt
echo "******************** Rebot #2"

rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
mv ./Results/out.xml ./Results/output.xml

# create an exclusion file for what was executed
/usr/bin/python ./PythonHelpers/Parse_output_xml.py ./Results/output.xml ./RunState/_Already_Run.txt
echo "******************** Run #3"
# run tests with filter (should execute first step not yet executed of each suite)
robot  --argumentfile ./params.txt
echo "******************** Rebot #3"

rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
mv ./Results/out.xml ./Results/output.xml

# create an exclusion file for what was executed
/usr/bin/python ./PythonHelpers/Parse_output_xml.py ./Results/output.xml ./RunState/_Already_Run.txt
echo "******************** Run #3"
# run tests with filter (should execute first step not yet executed of each suite)
robot  --argumentfile ./params.txt
echo "******************** Rebot #3"

rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
mv ./Results/out.xml ./Results/output.xml



#produce log and report
rebot --outputdir ./Results/ ./Results/output.xml
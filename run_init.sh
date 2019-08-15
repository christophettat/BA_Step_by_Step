# empty  the list of executed tests 
rm -r ./Results/*
rm -r ./RunState/*
cat /dev/null > ./RunState/_Already_Run.txt


# run tests with empty filter (should execute first step of each suite only)
echo "******************** Run #1"
robot  --argumentfile ./params.txt
echo "******************** Rebot #1"
rebot --report NONE --log NONE --output ./Results/output.xml --merge ./Results/output_current.xml



@ECHO OFF

REM Prep work, let's clean-up previous results 
del /Q .\Results\*.*
del /Q .\RunState\*.*

SET LookForFile=".\RunState\StateSummary.run"

robot  --argumentfile ./params.txt
rebot --report NONE --log NONE --output ./Results/output.xml --merge ./Results/output_current.xml

PAUSE


:CheckForFile
IF NOT EXIST %LookForFile% GOTO Finished
robot  --argumentfile ./params.txt
rebot --report NONE --log NONE --output ./Results/out.xml --merge ./Results/output.xml ./Results/output_current.xml
del %~dp0Results\output.xml
ren %~dp0Results\out.xml output.xml

REM Wait before next iteration
REM TIMEOUT /T 30 >nul
PAUSE plese press a key to continue

GOTO CheckForFile


:Finished
rebot --outputdir ./Results ./Results/output.xml 

ECHO The Run is Donem Thank You
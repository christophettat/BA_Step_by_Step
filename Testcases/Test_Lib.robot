***Settings***
Library  ./PythonHelpers/Variables_Saver_Library.py  127.0.0.1  6379

*** Test Cases ***
My Test - Generator
   ${myvar}=   set variable  a
   Log  ${myvar}
   save_vars
   ${myvar}=   set variable  will not exist
   

My Test - consumer
   load_vars  0
   ${myvar}=   catenate   ${myvar}  _  b
   Log  ${myvar}



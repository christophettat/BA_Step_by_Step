***Settings***
Library  DateTime

*** Test Cases ***
My Test 11
   ${myvar}=   set variable  a
   Log  ${myvar}

My Test 12
   ${myvar}=   catenate   ${myvar}  _  b
   Log  ${myvar}
   fail  this is a failed test



My Test 13 
   ${myvar}=   catenate   ${myvar}  _  c
   Log  ${myvar}

My Test 14 
   ${myvar}=   catenate   ${myvar}  _  d
   Log  ${myvar}
***Settings***
Library  DateTime

*** Test Cases ***
My Test 1
   ${myvar}=   set variable  a
   Log  ${myvar}

My Test 2
   ${myvar}=   catenate   ${myvar}  _  b
   Log  ${myvar}
   ${date}=	 Get Current Date	  increment=00:02:00  result_format=%Y%m%d%H%M%S
   ${tag}=   catenate  SEPARATOR=  next_at_  ${date}
   Set Tags  ${tag}

My Test 3 
   ${myvar}=   catenate   ${myvar}  _  c
   Log  ${myvar}

My Test 4 
   ${myvar}=   catenate   ${myvar}  _  d
   Log  ${myvar}
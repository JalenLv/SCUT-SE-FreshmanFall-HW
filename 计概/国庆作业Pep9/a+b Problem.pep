         BR      main        ;branch to main
a:       .WORD   0           ;define a to store the 1st num
b:       .WORD   0           ;define b to store the 2nd num
c:       .WORD   0           ;define c to store the sum
;
main:    DECI    a,d         ;input a
         DECI    b,d         ;input b
         LDWA    a,d         ;A <- a
         ADDA    b,d         ;perform a+b
         STWA    c,d         ;store the sum in c
         DECO    c,d         ;output the sum
         STOP                
         .END                  

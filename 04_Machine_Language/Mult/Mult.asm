// File name: projects/4/Mult.asm
// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

@R0
D=M
@COUNT
M=D // Value of R0 Goes into memory of count
@SUM
M=0

(LOOP)
@COUNT
D=M
D=D-1
D;JLT // if D<0, jump
@R1
D=M
@SUM
D=D+M
M=D

@COUNT
M=M-1

//goto LOOP
@LOOP
0;JMP // jump

(COUNT)
@SUM
D=M
@R2
M=D
@END
0;JMP

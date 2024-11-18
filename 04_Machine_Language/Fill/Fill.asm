// File name: projects/4/Fill.asm
// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

@KBD            
D=A
@end_address
M=D

// Main Loop
(LOOP)
    @KBD
    D=M           

    @BLACK
    D;JNE         // Jump to BLACK if a key is pressed (D != 0)
    
    @WHITE
    0;JMP         // If no key is pressed, jump to WHITE

// Black the screen
(BLACK)
    @SCREEN
    D=A
    @address
    M=D           

(FILL_B)
    @address
    A=M           
    M=-1          

    @address
    M=M+1         

    @end_address
    D=M
    @address
    D=D-M         
    @FILL_B
    D;JGT        // if D>0, jump  

    @LOOP         // Return to the main loop
    0;JMP

// Clear the screen
(WHITE)
    @SCREEN
    D=A
    @address
    M=D           

(FILL_W)
    @address
    A=M           
    M=0          

    @address
    M=M+1         

    @end_address
    D=M
    @address
    D=D-M         
    @FILL_W    
    D;JGT          // if D>0, jump  

    @LOOP          // Return to the main loop
    0;JMP

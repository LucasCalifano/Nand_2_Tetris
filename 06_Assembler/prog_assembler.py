#Nand2Tetris Project 6
lines = []  
binarySequence = [] 
aAddress = 16

# Store label to line number mappings
label_table = {}

# Track consecutive empty Enter presses
empty_press_count = 0

# First pass: Gather labels and store their line numbers
while True:
    line = input().strip() 
    
    if not line:  # Empty line
        empty_press_count += 1 
        if empty_press_count == 2:  # Exit after 3 consecutive empty presses
            break
    else:
        empty_press_count = 0  # Reset counter if line is not empty
    
    if line.startswith("("):
        label = line[1:-1].strip()  # Remove parentheses
        label_table[label] = len(lines)  
    elif not line.startswith("//"):  # Only non-comment lines
        lines.append(line)

# Second pass: Process the actual instructions (A and C)
for line in lines:
    # Ignore empty lines and comments
    if not line or line.startswith("//"):
        continue
    
    # A-Instructions
    if line.startswith("@"):
        aInst = line.split("@")[1].strip()
        
        if aInst.isdigit():
            n = int(aInst)  # Direct number, no need for symbol resolution
        elif aInst in label_table:
            n = label_table[aInst]  # Label: replace with line number from label table
        else:
            # Handle predefined symbols or new variables
            symbol_table = {
                "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
                "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
                "SCREEN": 16384, "KBD": 24576, "ITSR0": 10
            }
            if aInst in symbol_table:
                n = symbol_table[aInst]
            else:
                n = aAddress
                aAddress += 1
                symbol_table[aInst] = n
        
        # Convert n to 16-bit binary and append to binarySequence
        binarySequence.append(format(n, '016b'))
        
    else:
        # C-Instructions
        c = "0000000"  
        d = "000"  
        j = "000"  
        
        # Section 1: Handle destination (before '=' if present)
        if "=" in line:
            dest_part = line.split("=")[0].strip()
            comp_part = line.split("=")[1].split(";")[0].strip() if ";" in line else line.split("=")[1].strip()
        else:
            dest_part = ""
            comp_part = line.split(";")[0].strip()

        # Convert dest part to binary
        if "M" in dest_part:
            d = "001"
        if "D" in dest_part:
            d = "010"
        if "MD" in dest_part:
            d = "011"
        if "A" in dest_part:
            d = "100"
        if "AM" in dest_part:
            d = "101"
        if "AD" in dest_part:
            d = "110"
        if "AMD" in dest_part:
            d = "111"

        # Section 2: Handle computation part (comp)
        if comp_part == "0":
            c = "0101010"
        elif comp_part == "1":
            c = "0111111"
        elif comp_part == "-1":
            c = "0111010"
        elif comp_part == "D":
            c = "0001100"
        elif comp_part == "A":
            c = "0110000"
        elif comp_part == "!D":
            c = "0001101"
        elif comp_part == "!A":
            c = "0110001"
        elif comp_part == "-D":
            c = "0001111"
        elif comp_part == "-A":
            c = "0110011"
        elif comp_part == "D+1":
            c = "0011111"
        elif comp_part == "A+1":
            c = "0110111"
        elif comp_part == "D-1":
            c = "0001110"
        elif comp_part == "A-1":
            c = "0110010"
        elif comp_part == "D+A":
            c = "0000010"
        elif comp_part == "D-A":
            c = "0010011"
        elif comp_part == "A-D":
            c = "0000111"
        elif comp_part == "D&A":
            c = "0000000"
        elif comp_part == "D|A":
            c = "0010101"
        elif comp_part == "M":
            c = "1110000"
        elif comp_part == "!M":
            c = "1110001"
        elif comp_part == "-M":
            c = "1110011"
        elif comp_part == "M+1":
            c = "1110111"
        elif comp_part == "M-1":
            c = "1110010"
        elif comp_part == "D+M":
            c = "1000010"
        elif comp_part == "D-M":
            c = "1010011"
        elif comp_part == "M-D":
            c = "1000111"
        elif comp_part == "D&M":
            c = "1000000"
        elif comp_part == "D|M":
            c = "1010101"

        # Section 3: Handle jump (after ';' if present)
        if ";" in line:
            jump_part = line.split(";")[1].strip()
            if jump_part == "JGT":
                j = "001"
            elif jump_part == "JEQ":
                j = "010"
            elif jump_part == "JGE":
                j = "011"
            elif jump_part == "JLT":
                j = "100"
            elif jump_part == "JNE":
                j = "101"
            elif jump_part == "JLE":
                j = "110"
            elif jump_part == "JMP":
                j = "111"
        
        # Append the combined binary instruction for C-instruction
        binarySequence.append("111" + c + d + j)

# Ensure the last instruction (`@END 0;JMP`) is added if not already present
if "(END)" in lines:
    binarySequence.append("1110000000000000")  # Ensure this instruction is added correctly

# Print the binary sequence
print("\n".join(binarySequence))

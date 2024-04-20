
Intial = 4194304    # Intial value of PC
opcodes={
        'add': '000000',
        'addi': '001000',
        'beq': '000100',
        'bne': '000101',        # Creating a dictionary for opcodes
        'sub': '000000',
        'lw': '100011',
        'slt': '000000',
        'j':'000010',
        'sw': '101011',
        'sll': '000000'
    }

funct = {
    'add': '100000',
    'sub': '100010',            # Creating a dictionary for function field of R-type instructions
    'sll': '000000',
    'slt': '101010',
    'sll': '000000'
}

reg = {
    '$t0':'01000',
    '$t1':'01001',
    '$t2':'01010',
    '$t3':'01011',
    '$t4':'01100',
    '$t5':'01101',
    '$t6':'01110',              # Dictionary for numbers associated with registetrs
    '$t7':'01111',
    '$s0':'10000',
    '$s1':'10001',
    '$s2':'10010',
    '$s3':'10011',
    '$s4':'10100',
    '$s5':'10101',
    '$s6':'10110',
    '$s7':'10111',
    '$0' : '00000',
    '$t8': '11000',
    '$t9': '11001'

}

labels = {
    'skiploop': '0000000000011011',     # Contains 16-bit immediate values for beq,bne instructions
    'done': '0000000000010111',
    'innerloopdone': '0000000000001010',
    'swap': '0000000000000011',
    'innerloop': '00000100000000000000001001',  # Contains 26-bit jump address for j-type instructions
    'return_from_swap': '00000100000000000000001110',
    'outerfor': '00000100000000000000000100',
    'stop': '00000100000000000000100001'  
}

def flipbits(bit):
    if(bit == '1'):     # This function is useful for flipping bits while calculating one's complement. It takes a string input '0' or '1' and returns the flipped bit.
        ans = '0'
    else:
        ans = '1'
    return ans

def Convert_to_Binary(num,x):   # Takes two inputs num and x, num is a string representaion of a positive or a negative number whose binary equivalent should be found. x is the length of the binary string the function should return.
    if(num[0] != '-'):
        n = int(num)
    else:
        s1 = num[1: ]
        n = int(s1)
    bn = ""
    if(n == 0):
        for i in range(0,int(x)):
            bn += '0'
        return bn
    while(n != 0):
        bn += str(n%2)
        n = n//2
    bnl1 = len(bn)
    binary = bn[bnl1: :-1]
    binary = '0' + binary   # Calculates 2's complement representaion of |n|.
    bnl = len(binary)
    if(num[0] == '-'):  # If n is negative we calculate 2's complement of |n|.
        ones = ""
        twos = ""
        for i in range(0,bnl):
            ones += flipbits(binary[i])
        ones = list(ones.strip(" "))
        twos = list(ones)
        for j in range(bnl-1,-1,-1):
            if(ones[j] == '1'):
                twos[j] = '0'
            else:
                twos[j] = '1'
                break
        j = j-1
        if(j == -1 and ones[j+1] == '1'):
            twos.insert(0, '1')
        binary = "".join(twos)
    l = len(binary)
    x = int(x)
    if(l < x):      # Sign extend for the immediate value.
        diff = x-l
        ex = binary[0]
        extend = ""
        for i in range(0,diff):
            extend += ex
        binary = extend + binary
    return binary


PC = Intial #Intialize PC to the starting address.
f = open('assignment1.txt','r')  # File input.
code = f.read()
instructions = code.split('\n') # Split the code into list of instructions.
for instruction in instructions:
    ele = instruction.split()   # Split instruction by space.
    if(len(ele) == 0):      # Consition to check if its the end of the code.
        break
    op = ele[0] #instruction
    if(len(ele) == 1):  # Skip the line if its a label
        continue
    comp = ele[1].split(',')  #comp will contain list of regs and immediate value.
    output = "" # output will give us the machine code of each instruction.
    # Using if-elif to check which instruction and accordingly concatinating strings to the output based on the respective instruction. At the end of each conditional statement we are printing the hexadeciaml value of the PC and the corresponding machine code of the instruction.
    if(op == "add"):
        output += opcodes['add'] + reg[comp[1]] + reg[comp[2]] + reg[comp[0]] + '00000' + funct['add']
        print(hex(PC) + " " + output)
    elif(op == 'addi'):
        output += opcodes['addi'] + reg[comp[1]] + reg[comp[0]] + Convert_to_Binary(comp[2],16)
        print(hex(PC) + " " + output)
    elif(op == 'beq'):
        output += opcodes['beq'] + reg[comp[0]] + reg[comp[1]] + labels[comp[2]]
        print(hex(PC) + " " + output)
    elif(op == 'bne'):
        output += opcodes['bne'] + reg[comp[0]] + reg[comp[1]] + labels[comp[2]]
        print(hex(PC) + " " + output)
    elif(op == "sub"):
        output += opcodes['sub'] + reg[comp[1]] + reg[comp[2]] + reg[comp[0]] + '00000' + funct['sub']
        print(hex(PC) + " " + output)
    elif(op == "lw"):
        if(comp[1][0] != '-'):
            im = comp[1][0]
            regs = comp[1][2:len(comp[1])-1]
        else:
            im = comp[1][1]
            regs = comp[1][3:len(comp[1])-1]
        output += opcodes['lw'] + reg[regs] + reg[comp[0]] + Convert_to_Binary(im,16)
        print(hex(PC) + " " + output)
    elif(op == "sw"):
        im = comp[1][0]
        regs = comp[1][2:len(comp[1])-1]
        output += opcodes['sw'] + reg[regs] + reg[comp[0]] + Convert_to_Binary(im,16)
        print(hex(PC) + " " + output)
    elif(op == "slt"):
        output += opcodes['slt'] + reg[comp[1]] + reg[comp[2]] + reg[comp[0]] + '00000' + funct['slt']
        print(hex(PC) + " " + output)
    elif(op == 'sll'):
        output += opcodes['sll'] + '00000' + reg[comp[1]] + reg[comp[0]] + Convert_to_Binary(comp[2],5) + funct['sll']
        print(hex(PC) + " " + output)
    elif(op == 'j'):
        output += opcodes['j'] + labels[comp[0]]
        print(hex(PC) + " " + output)
    PC += 4 # Incrementing the PC value by 4.

        
    








"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0, 0, 0, 0, 0, 0, 0, []]
        self.pc = 0
        self.ram = [0] * 256
        self.var = input("Do you have your own program? ")
        if self.var.lower() == "yes":
            self.var = input("What program would you like to run? ")
        else:
            self.var = "no"
        self.FL = [0, 0, 0, 0, 0, 0, 0, 0] #00000LGE if FL[7] == 1, regA == regB


    def load(self):
        """Load a program into memory."""
        address = 0

        if self.var == "no":
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        else:
            program = []
            try:
                with open(f'{self.var}') as f:
                    for line in f:
                        line = line.strip()

                        if line == '' or line [0]=="#":
                            continue
                            
                        try:
                            str_value = line.split("#")[0]
                            value = int(str_value, 2)
                            program.append(value)

                        except ValueError:
                            print(f"Invalid number: {str_value}")
            
            except FileNotFoundError:
                print(f"File not found: {self.var}")

        for instruction in program:
            self.ram[address] = instruction
            address += 1    

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = self.pc
        halted = False

        while not halted:
            instruction = self.ram[IR]

            if instruction == 0b10100111: # CMP
                reg_1 = self.ram[IR+1]
                reg_2 = self.ram[IR+2]
                val_1 = self.reg[reg_1]
                val_2 = self.reg[reg_2]
                if val_1 == val_2:
                    self.FL[7] = 1
                IR += 3

            elif instruction == 0b01010100: # JMP
                reg_num = self.ram[IR+1]  
                value = self.reg[reg_num]
                IR = value            

            elif instruction == 0b01010101: # JEQ 
                if self.FL[7] == 1:
                    reg_num = self.ram[IR+1]  
                    value = self.reg[reg_num]
                    IR = value  
                else:
                    IR += 2                    

            elif instruction == 0b01010110: # JNE
                if self.FL[7] == 0:
                    reg_num = self.ram[IR+1]  
                    value = self.reg[reg_num]
                    IR = value  
                else:
                    IR += 2  

            elif instruction == 0b10000010: # LDI
                reg_num = self.ram[IR+1]
                value = self.ram[IR+2]
                self.reg[reg_num] = value
                IR += 3

            elif instruction == 0b01000111: # PRN
                reg_num = self.ram[IR+1]
                print(self.reg[reg_num])
                IR += 2

            elif instruction == 0b10100010: # MUL
                reg_1 = self.ram[IR+1]
                reg_2 = self.ram[IR+2]
                val_1 = self.reg[reg_1]
                val_2 = self.reg[reg_2]
                product = val_1 * val_2
                self.reg[reg_1] = product
                IR += 3

            elif instruction == 0b01000101: # PUSH
                reg_1 = self.ram[IR+1]
                val_1 = self.reg[reg_1]
                self.reg[7].append(val_1)
                IR += 2
            
            elif instruction == 0b01000110: # POP
                reg_1 = self.ram[IR+1]
                self.reg[reg_1] = self.reg[7].pop()
                IR += 2

            elif instruction == 0b00000001: # HLT
                halted = True
                IR += 1
            
            else:
                print(f"unknown instruction {instruction} at address {IR}")
                sys.exit(1)
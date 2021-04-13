
import sys


class computer:
    def __init__(self):
        self.indexed_regs = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.regs = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}
        self.ip = 0x0

YELLOW=u"\u001b[33m"
RESET=u"\u001b[0m"

DEBUG = True
DEBUG_FILE = True

if sys.platform == 'win32':
    YELLOW=""
    RESET=""

if DEBUG_FILE == True:
    import datetime
    log = open("emulator.log", "a")
    now = datetime.datetime.now()
    log.write(now.strftime("%d-%m-%Y %H:%M") + "\n")
    log.close()


def log(message, ip):
    if DEBUG and DEBUG_FILE != True:
        print(f"[{YELLOW}{hex(ip)}{RESET}] ~ " + message)
    elif DEBUG and DEBUG_FILE:
        log = open("emulator.log", "a")
        log.write(f"{message}  ~ [{hex(ip)}]: \n")
        log.close()

def exec_binary_program(mcp, program):
    while True:
        try:
            opcode = program[mcp.ip]
        except IndexError:
            print("Break. List of opcodes ended..")
            break
        command = opcode & 0xF000
        
        value = opcode & 0x0FFF

        subvalue = ( opcode & 0x0F00 ) >> 8

        subvalue2 = ( opcode & 0x00F0 ) >> 4
        if command == 0x0 and value == 0x999:
            # break the program ( HALT )
            break 
        if command == 0x1000:
            # change ip( GOTO ) 
            mcp.ip = value
            continue
        elif command == 0x2000:
            # add value of register `subvalue` to `subvalue2` ( ADD )
            try:
                mcp.indexed_regs[subvalue] = mcp.indexed_regs[subvalue] + mcp.indexed_regs[subvalue2]
            except KeyError:
                print("Use correct register")
                break
        elif command == 0x3000:
            # basic realization of "if". Skip next opcode, if `subvalue` ==
            # `subvalue1`
            try:
                mcp.indexed

        print(hex(value))
        print(hex(command))
        mcp.ip += 1


program = ["push", "C", 5,  "move", "A", "B", "push", "A", 5, "add", "B", "A",
        "equal", "A", "C", "goto", 10, "put", "Value from register A: ", "put",
        "A", "put", "move", "halt"]

binary_program = ["", 0x2111, 0x2200]

mcp = computer()

exec_binary_program(mcp, binary_program)
# exec_program(mcp, program)


def exec_program(comp, program):
    ip = 0x0
    try:
        while True:
            if ip < 0:
                print("Value can't be negative")
                return
            try:
                command = program[ip]
            except IndexError:
                print("Error: HALT not find")
                break

            if command == "halt":
                log("halt the program", ip)
                break
            elif command == "push":
                log(f"pushing {program[ip+2]} to register {program[ip+1]}", ip)
                comp.regs[program[ip+0x01]] = program[ip+0x02]
            elif command == "pop":
                popped = comp.regs[program[ip+0x01]]
                comp.regs[program[ip+0x01]] = 0
                log(f"Pop the value {popped} of register {program[ip+1]}", ip)

            elif command == "add":
                first = comp.regs[program[ip+0x01]]
                second = comp.regs[program[ip+0x02]]
                comp.regs[program[ip+0x01]] = 0
                comp.regs[program[ip+0x01]] = 0 
                result = first + second
                log(f"add {first} to {second} and push it to register {program[ip+2]}", ip)
                comp.regs[program[ip+0x02]] = result
           
            elif command == "goto":
                ip = program[ip+0x01]
                log(f"We now at {hex(ip)}", ip)
                continue
            elif command == "equal":
                first = comp.regs[program[ip+0x01]]
                second = comp.regs[program[ip+0x02]]
                if first == second:
                    ip += 0x03
                    log(f"{first} equal to {second}", ip)
                else:
                    log(f"{first} from register {program[ip+0x01]} don't equal to {second} from register {program[ip+0x02]}", ip)

            elif command == "not_equal":
                first = comp.regs[program[ip+0x01]]
                second = comp.regs[program[ip+0x02]]
                if first != second:
                    log(f"{first} don't equal to {second}", ip)
                    ip += 0x03
                else:
                    log(f"{first} from register {program[ip+0x01]} equal to {second} from register {program[ip+0x02]}", ip)

            elif command == "move":
                first = comp.regs[program[ip+0x01]]
                comp.regs[program[ip+0x02]] = first
                log(f"moving {first} to {program[ip+0x02]}", ip)

            elif command == "put":
                message = program[ip + 0x01]
                output = ""
                if message in list(comp.regs):
                    output = comp.regs[message]
                    log(f"putting {output} from {message}\n", ip)
                else:
                    output = program[ip+0x01]

                sys.stdout.write(str(output))
                log(f"putting {output}\n", ip)
            ip += 0x01        
    except KeyError:
        print("\nNo required value")
        


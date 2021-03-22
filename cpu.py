
import sys


YELLOW=u"\u001b[33m"
RESET=u"\u001b[0m"

DEBUG = True
DEBUG_FILE = False

if DEBUG_FILE == True:
    import datetime
    log = open("emulator.log", "a")
    now = datetime.datetime.now()
    log.write(now.strftime("%d-%m-%Y %H:%M") + "\n")
    log.close()


def log(message, ip):
    if DEBUG and DEBUG_FILE != True:
        print(f"[{YELLOW}{hex(ip)}{RESET}]: " + message)
    elif DEBUG and DEBUG_FILE:
        log = open("emulator.log", "a")
        log.write(f"[{hex(ip)}]: {message}\n")
        log.close()

def exec_program(comp, program):
    ip = 0x0
    while True:
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
                log(f"putting {output}\n", ip)

            sys.stdout.write(str(output))
        ip += 0x01        



class computer:
    def __init__(self):
        self.regs = {"A":0, "B":0, "C":0, "D":0, "E":0}


class api:
    """
    api for programming in this cpu.
    """

    def __init__(self, pc):
        self.program = []
    def put(self, message : str):
        """
        Message out to stdout(or register)
        """
        self.program.append("put")
        self.program.append(message)
    def move(self, register : str, register2 : str):
        """
        moving value of register1 to register2
        """
        self.program.append("move")
        self.program.append(register)
        self.program.append(register2)
    def equal(self, register1 : str, register2 : str):
        """
        check equal of register1 to register2
        """
        self.program.append("equal")
        self.program.append(register1)
        self.program.append(register2)
    def not_equal(self, register1 : str, register2 : str):
        """
        Check not equal of register1 to register2
        """
        self.program.append("not_equal")
        self.program.append(register1)
        self.program.append(register2)
    def goto(self, ip : hex):
        """
        Goto шз
        """
        self.program.append("goto")
        self.program.append(ip)
    def halt(self):
        self.program.append("halt")
    def push(self, register1 : str, register2 : str):
        self.program.append("push")
        self.program.append(register1)
        self.program.append(register2)
    def pop(self, register : str):
        self.program.append("pop")
        self.program.append(register)
    def add(self, register1 : str, register2 : str):
        self.program.append("add")
        self.program.append(register1)
        self.program.append(register2)




program = ["push", "C", 20,  "move", "A", "B", "push", "A", 5, "add", "B", "A",
        "equal", "A", "C", "goto", 3, "put", "Value from register A: ", "put",
        "A", "put", "\n", "halt"]


mcp = computer()
exec_program(mcp, program)


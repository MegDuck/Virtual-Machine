
import sys




DEBUG = False

def log(message):
    if DEBUG==True:
        print(message)


def exec_program(comp, program):

    ip = 0x00
    while True:
        try:
            command = program[ip]
        except IndexError:
            print("Error: HALT not find")
            break
        if command == "halt":
            log("halt the program")
            break
        elif command == "push":
            log(f"pushing {program[ip+2]} to register {program[ip+1]}")
            comp.regs[program[ip+0x01]] = program[ip+0x02]
        elif command == "pop":
            popped = comp.regs[program[ip+0x01]]
            comp.regs[program[ip+0x01]] = 0
            log(f"Pop the value {popped} of register {program[ip+1]}")

        elif command == "add":
            first = comp.regs[program[ip+0x01]]
            second = comp.regs[program[ip+0x02]]
            comp.regs[program[ip+0x01]] = 0
            comp.regs[program[ip+0x01]] = 0 
            result = first + second
            log(f"Add {first} to {second} and push it to register {program[ip+2]}")
            comp.regs[program[ip+0x02]] = result
            ip += 0x01
        elif command == "goto":
            ip = program[ip+0x01]
            log(f"We now at {ip}")
            continue
        elif command == "equal":
            first = comp.regs[program[ip+0x01]]
            second = comp.regs[program[ip+0x02]]
            if first == second:
                ip += 0x03
        elif command == "not_equal":
            first = comp.regs[program[ip+0x01]]
            second = comp.regs[program[ip+0x02]]
            if first != second:
                ip += 0x03
            ip += 0x02
        elif command == "move":
            first = comp.regs[program[ip+0x01]]
            comp.regs[program[ip+0x02]] = first
            ip += 0x02
        elif command == "put":
            message = program[ip + 0x01]
            output = ""
            if message in list(comp.regs):
                output = comp.regs[message]
                log(f"putting {output} from {message}")
            else:
                output = program[ip+0x01]
                log(f"Putting {output}")

            sys.stdout.write(str(output))
            ip += 0x01
        ip += 0x01
        



class computer:
    def __init__(self):
        self.regs = {"A":0, "B":0, "C":0, "D":0, "E":0}


class api:
    """
    api for programming in this cpu.
    """

    def __init__(self):
        self.program = []
    def put(self, message : str):
        """
        """




program = ["push", "C", 20,  "move", "A", "B", "push", "A", 5, "add", "B", "A",
        "equal", "A", "C", "goto", 3, "put", "Value from register A: ", "put",
        "A", "put", "\n", "halt"]


mcp = computer()
exec_program(mcp, program)


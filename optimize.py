"""An optimizing BF-to-python compiler."""
import sys

from cancel_mines_plus import opt_cancel
from contract import opt_contract
from ClearLoop import opt_clearloop
from exchangeloop import opt_changeloop
from offset import opt_offsetops
from scanloop import opt_scanloop
from Intermediate_Representation import bf_to_ir, ir_to_python

opts = {'cancel': opt_cancel,
        'contract': opt_contract,
        'clearloop': opt_clearloop,
        'changeloop': opt_changeloop,
        'offsetops': opt_offsetops,
        'findzero': opt_scanloop
        }


def check_error(BF_code):
    if not BF_code:
        raise ValueError("No valid BF code provided.")
    if BF_code.count('[') != BF_code.count(']'):
        raise ValueError("Unmatched brackets in code.")
    syntax = ['<', '>', '+', '-', '.', ',', '[', ']', '\n'," ",' ']
    tape = [0] * 10000
    ptr = 0
    code_ptr = 0
    max_steps = 10000
    step_count = 0
    indentation = 0
    idx = 0
    length = len(BF_code)
    repeat_count = 0

    while idx < length:
        command = BF_code[idx]
        if command not in syntax:
            raise ValueError(f"Invalid character '{command}' detected.")

        repeat_count = 1
        step_count += 1
        while idx + 1 < length and BF_code[idx + 1] == command:
            repeat_count += 1
            idx += 1

        if step_count > max_steps:
            raise RuntimeError("Maximum execution steps exceeded. Possible infinite loop.")

        if command == '>':
            ptr += repeat_count
            if ptr >= max_steps:
                raise IndexError("Pointer exceeded tape size (ptr > 10000).")

        elif command == '<':
            ptr -= repeat_count
            if ptr < 0:
                raise IndexError("Pointer moved to negative index (ptr < 0).")
        elif command == '[':
            indentation += 1
        elif command == ']':
            indentation -= 1
            #if indentation < 0:
                #raise ValueError("Unmatched ']' detected.")

        idx += 1
    #if indentation != 0:
        #raise ValueError("Unmatched '[' detected.")


def main():
    with open('sierpinski.bf', 'r') as f:
        BF_code = f.read()
    check_error(BF_code)
    ir = bf_to_ir(BF_code)

    #optimizations = ['cancel', 'clearloop', 'changeloop', 'offsetops', 'contract', 'findzero']
    optimizations = []

    for x in optimizations:
        if x == 'none':
            continue
        ir = opts[x](ir)
    print(ir)
    print(ir_to_python(ir))
    python_code = ir_to_python(ir)
    with open("output.py", 'w') as f:
        f.write(python_code)
    print("output : ")
    exec(python_code)
    return 0


if __name__ == '__main__':
    sys.exit(main())

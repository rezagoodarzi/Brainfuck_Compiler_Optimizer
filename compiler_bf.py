def brainfuck_to_python(brainfuck_code):
    """
    Converts Brainfuck code to equivalent Python code.
    """
    #brainfuck_code = ''.join(filter(lambda x: x in ['<', '>', '+', '-', '.', ',', '[', ']'], brainfuck_code))
    syntax = ['<', '>', '+', '-', '.', ',', '[', ']','\n']

    if not brainfuck_code:
        raise ValueError("No valid Brainfuck code provided.")
    if brainfuck_code.count('[') != brainfuck_code.count(']'):
        raise ValueError("Unmatched brackets in code.")

    python_code = [
        "tape = [0] * 10000",
        "ptr = 0",
        "output = ''",
        "input_buffer = []"
    ]
    tape = [0] * 10000
    ptr = 0
    code_ptr = 0
    max_steps = 10000
    step_count = 0
    indentation = 0
    idx = 0
    length = len(brainfuck_code)
    repeat_count = 0

    while idx < length:
        command = brainfuck_code[idx]
        if command not in syntax:
            raise ValueError(f"Invalid character '{command}' detected.")


        repeat_count = 1
        step_count += 1
        while idx + 1 < length and brainfuck_code[idx + 1] == command:
            repeat_count += 1
            idx += 1

        if step_count > max_steps:
            raise RuntimeError("Maximum execution steps exceeded. Possible infinite loop.")

        if command == '>':
            ptr += repeat_count
            if ptr >= max_steps:
                raise IndexError("Pointer exceeded tape size (ptr > 10000).")

            python_code.append("    " * indentation + f"ptr += {repeat_count}")
        elif command == '<':
            ptr -= repeat_count
            if ptr < 0:
                raise IndexError("Pointer moved to negative index (ptr < 0).")

            python_code.append("    " * indentation + f"ptr -= {repeat_count}")
        elif command == '+':
            python_code.append("    " * indentation + f"tape[ptr] = (tape[ptr] + {repeat_count})")
        elif command == '-':
            python_code.append("    " * indentation + f"tape[ptr] = (tape[ptr] - {repeat_count})")
        elif command == '.':
            python_code.append("    " * indentation + "output += chr(tape[ptr])")
        elif command == ',':
            python_code.append(
                "    " * indentation + "if not input_buffer: input_buffer.append(input('Enter a single character: ')[0])")
            python_code.append("    " * indentation + "tape[ptr] = ord(input_buffer.pop(0))")
        elif command == '[':
            python_code.append("    " * indentation + "while tape[ptr] != 0:")
            indentation += 1
        elif command == ']':
            indentation -= 1
            if indentation < 0:
                raise ValueError("Unmatched ']' detected.")

        idx += 1
    if indentation != 0:
        raise ValueError("Unmatched '[' detected.")

    python_code.append("print(output)")
    return '\n'.join(python_code)


def execute_brainfuck_file(file_path):
    """
    Reads Brainfuck code from a file, compiles it to Python code, and executes it.
    """
    with open(file_path, 'r') as f:
        brainfuck_code = f.read()

    try:
        python_code = brainfuck_to_python(brainfuck_code)
        with open("output.py", 'w') as f:
            f.write(python_code)
        #exec(python_code)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    file_path = "program.bf"
    execute_brainfuck_file(file_path)
